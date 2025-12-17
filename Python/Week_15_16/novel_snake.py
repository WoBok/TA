import json
import os
import random
import sys

import pygame


"""
新玩法贪吃蛇：赛博朋克版 + 技能系统

玩法说明：
1. 基本操作
   - 方向：↑ ↓ ← → 或 WASD
   - 空格：如果有能量，开启 / 关闭 幽灵模式（持续时间有限）
   - Tab：暂停并查看排行榜
   - ESC：退出游戏

2. 食物类型
   - 品红圆形：普通食物，每吃一个 +1 长度，+1 分，触发品红刷光特效
   - 黄色菱形：能量食物，增加一次"幽灵能量"（energy），触发黄色刷光特效

3. 幽灵模式（Ghost Mode）
   - 按空格消耗 1 点能量，进入幽灵模式 5 秒
   - 幽灵模式下可以穿过自己的身体、穿过荆棘障碍、穿墙传送
   - 是最强大的技能，可以无视一切障碍

4. 动态荆棘障碍
   - 每吃满 5 个普通食物，地图上随机生成一个新的荆棘障碍
   - 荆棘是永久的，非幽灵模式下碰到会死亡
   - 幽灵模式下可以穿过荆棘

5. 游戏结束
   - 非幽灵模式下：撞到边界、荆棘、或撞到自己，都会 Game Over
   - 幽灵模式下：无敌，可以穿过一切

6. 赛博朋克特效
   - 霓虹发光效果：蛇身、食物、障碍都有发光层
   - 粒子爆炸：吃到食物时触发粒子特效
   - 刷光效果：吃到食物时身体从头到尾闪过一道光

7. 依赖
   - pip install pygame
"""


# -------------------- 基本配置 --------------------
CELL_SIZE = 25
GRID_WIDTH = 24   # 网格宽度
GRID_HEIGHT = 20  # 网格高度

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT

RENDER_FPS = 60             # 渲染帧率，保证输入跟手
STEP_INTERVAL_MS = 120       # 蛇移动间隔（毫秒），决定实际速度

# -------------------- 赛博朋克配色 --------------------
# 主色调：霓虹紫红、青蓝、亮黄
SNAKE_COLOR = (0, 255, 255)         # 青色霓虹
SNAKE_HEAD_COLOR = (255, 0, 255)    # 品红霓虹
SNAKE_GLOW = (0, 200, 255)          # 发光效果
FOOD_COLOR = (255, 0, 127)          # 品红食物
FOOD_GLOW = (255, 50, 150)          # 食物发光
ENERGY_FOOD_COLOR = (255, 255, 0)   # 黄色能量食物
ENERGY_GLOW = (255, 200, 0)         # 能量发光
BG_COLOR = (10, 5, 20)              # 深紫黑背景
GRID_COLOR = (50, 20, 80)           # 紫色网格
TEXT_COLOR = (0, 255, 255)          # 青色文字
TEXT_GLOW = (0, 200, 255)           # 文字发光
OBSTACLE_COLOR = (200, 0, 255)      # 紫红障碍
OBSTACLE_GLOW = (150, 0, 200)       # 障碍发光

GHOST_DURATION = 5_000  # 幽灵模式持续时间（毫秒）
FOOD_PER_OBSTACLE = 5   # 每吃多少普通食物生成一个障碍
LEADERBOARD_FILE = "snake_leaderboard.json"  # 排行榜文件
MAX_LEADERBOARD_ENTRIES = 10  # 排行榜最多保留多少条


# -------------------- 粒子特效类 --------------------
class Particle:
    """单个粒子"""
    def __init__(self, x, y, color, vx, vy, life):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.size = random.randint(3, 8)
    
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        # 添加重力和速度衰减
        self.vy += 0.2
        self.vx *= 0.98
    
    def is_alive(self):
        return self.life > 0
    
    def draw(self, surface):
        # 根据剩余生命调整透明度
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (*self.color, alpha)
        size = int(self.size * (self.life / self.max_life))
        if size > 0:
            # 绘制带发光效果的粒子
            s = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
            pygame.draw.circle(s, color_with_alpha, (size, size), size)
            surface.blit(s, (int(self.x - size), int(self.y - size)))


class ParticleSystem:
    """粒子系统管理器"""
    def __init__(self):
        self.particles = []
    
    def emit(self, x, y, color, count=20):
        """在指定位置发射粒子"""
        for _ in range(count):
            angle = random.uniform(0, 2 * 3.14159)
            speed = random.uniform(2, 8)
            vx = speed * random.uniform(-1, 1)
            vy = speed * random.uniform(-3, 0)  # 向上喷射
            life = random.randint(20, 40)
            self.particles.append(Particle(x, y, color, vx, vy, life))
    
    def update(self):
        """更新所有粒子"""
        self.particles = [p for p in self.particles if p.is_alive()]
        for p in self.particles:
            p.update()
    
    def draw(self, surface):
        """绘制所有粒子"""
        for p in self.particles:
            p.draw(surface)


class SnakeGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("技能贪吃蛇 - 幽灵模式 + 动态障碍")

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        # 使用支持中文的字体列表，前面优先中文，后面兜底英文
        font_candidates = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "consolas"]
        self.font_small = pygame.font.SysFont(font_candidates, 18)
        self.font_big = pygame.font.SysFont(font_candidates, 36, bold=True)

        # 渲染帧率（固定）
        self.fps = RENDER_FPS

        # 排行榜相关
        self.leaderboard = self.load_leaderboard()
        self.show_leaderboard = False  # 是否显示排行榜界面
        self.entering_name = False     # 是否正在输入名字
        self.player_name_input = ""    # 输入的名字
        self.paused = False            # 游戏是否暂停

        # 粒子系统
        self.particle_system = ParticleSystem()

        self.reset(start_with_intro=True)

    # -------------------- 游戏状态初始化 --------------------
    def reset(self, start_with_intro: bool = False):
        # start_with_intro=True 表示回到启动界面，仅首次进入使用；
        # 复盘（按 R）时使用 start_with_intro=False，直接开新局。
        self.started = not start_with_intro
        self.last_move_time = pygame.time.get_ticks()
        self.step_interval_ms = STEP_INTERVAL_MS
        center = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        self.snake = [
            center,
            (center[0] - 1, center[1]),
            (center[0] - 2, center[1]),
        ]
        self.direction = (1, 0)  # 初始向右
        self.next_direction = self.direction

        self.score = 0
        self.normal_food_eaten = 0

        self.obstacles = set()

        self.food_pos = None
        self.energy_food_pos = None

        self.energy = 1  # 初始给一点能量试试新玩法
        self.ghost_mode = False
        self.ghost_end_time = 0

        # 刷光效果
        self.glow_effect_active = False
        self.glow_effect_start = 0
        self.glow_effect_color = None
        self.glow_effect_duration = 500  # 刷光持续时间（毫秒）

        self.spawn_food()

        self.game_over = False
        self.game_over_reason = ""
        self.paused = False
        self.show_leaderboard = False

    # -------------------- 排行榜相关 --------------------
    def load_leaderboard(self):
        """从文件加载排行榜，格式：[{"name": "玩家名", "score": 分数}, ...]"""
        if not os.path.exists(LEADERBOARD_FILE):
            return []
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []

    def save_leaderboard(self):
        """保存排行榜到文件"""
        try:
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
                json.dump(self.leaderboard, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存排行榜失败: {e}")

    def is_high_score(self, score):
        """判断分数是否能进入排行榜"""
        if len(self.leaderboard) < MAX_LEADERBOARD_ENTRIES:
            return True
        return score > self.leaderboard[-1]["score"]

    def add_to_leaderboard(self, name, score):
        """添加记录到排行榜并排序"""
        self.leaderboard.append({"name": name, "score": score})
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.leaderboard = self.leaderboard[:MAX_LEADERBOARD_ENTRIES]
        self.save_leaderboard()

    # -------------------- 工具函数 --------------------
    def random_empty_cell(self):
        """从空白位置里随机挑一个网格坐标"""
        occupied = set(self.snake) | self.obstacles
        if self.food_pos:
            occupied.add(self.food_pos)
        if self.energy_food_pos:
            occupied.add(self.energy_food_pos)

        all_cells = [
            (x, y)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x, y) not in occupied
        ]
        if not all_cells:
            return None
        return random.choice(all_cells)

    def spawn_food(self):
        """生成普通食物和（有概率）能量食物"""
        self.food_pos = self.random_empty_cell()
        # 30% 概率生成能量食物（如果当前没有）
        if self.energy_food_pos is None and random.random() < 0.3:
            self.energy_food_pos = self.random_empty_cell()

    def spawn_obstacle(self):
        cell = self.random_empty_cell()
        if cell is not None:
            self.obstacles.add(cell)

    # -------------------- 输入处理 --------------------
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # 如果正在输入名字
                if self.entering_name:
                    if event.key == pygame.K_RETURN:
                        # 回车确认，添加到排行榜
                        if self.player_name_input.strip():
                            self.add_to_leaderboard(self.player_name_input.strip(), self.score)
                        self.entering_name = False
                        self.player_name_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        # 退格删除
                        self.player_name_input = self.player_name_input[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        # ESC 取消输入
                        self.entering_name = False
                        self.player_name_input = ""
                    else:
                        # 输入字符（限制长度）
                        if len(self.player_name_input) < 15:
                            self.player_name_input += event.unicode
                    return

                # 查看排行榜（Tab 键切换，同时暂停/恢复游戏）
                if event.key == pygame.K_TAB:
                    self.show_leaderboard = not self.show_leaderboard
                    # 显示排行榜时暂停，关闭时恢复
                    if self.show_leaderboard:
                        self.paused = True
                    else:
                        self.paused = False
                    return

                # 启动画面：按空格键开始（ESC 直接退出）
                if not self.started:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_SPACE:
                        self.started = True
                    return

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # 方向键 / WASD
                elif event.key in (pygame.K_UP, pygame.K_w):
                    if self.direction != (0, 1):
                        self.next_direction = (0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if self.direction != (0, -1):
                        self.next_direction = (0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if self.direction != (1, 0):
                        self.next_direction = (-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if self.direction != (-1, 0):
                        self.next_direction = (1, 0)
                # 幽灵模式开关
                elif event.key == pygame.K_SPACE:
                    self.toggle_ghost_mode()


    def toggle_ghost_mode(self):
        now = pygame.time.get_ticks()
        # 已在幽灵模式：直接关闭
        if self.ghost_mode:
            self.ghost_mode = False
            self.ghost_end_time = now
            return

        # 还没开启，且有能量：开启
        if self.energy > 0 and not self.ghost_mode:
            self.energy -= 1
            self.ghost_mode = True
            self.ghost_end_time = now + GHOST_DURATION

    def trigger_game_over(self, reason):
        """触发游戏结束，判断是否进入排行榜"""
        self.game_over = True
        self.game_over_reason = reason
        # 判断是否进入排行榜
        if self.score > 0 and self.is_high_score(self.score):
            self.entering_name = True
            self.player_name_input = ""
    
    def trigger_glow_effect(self, color):
        """触发身体刷光效果"""
        self.glow_effect_active = True
        self.glow_effect_start = pygame.time.get_ticks()
        self.glow_effect_color = color

    # -------------------- 游戏更新逻辑 --------------------
    def update(self):
        if self.game_over:
            return

        now = pygame.time.get_ticks()

        # 幽灵模式计时即使在未移动时也需要更新
        if self.ghost_mode and now >= self.ghost_end_time:
            self.ghost_mode = False

        # 移动节奏控制：未到间隔则不移动
        if now - self.last_move_time < self.step_interval_ms:
            return
        self.last_move_time = now

        # 更新方向
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        # 边界检测：幽灵模式允许穿墙（从另一侧出来）；正常模式死亡
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            if self.ghost_mode:
                new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
            else:
                self.trigger_game_over("撞到边界了！")
                return

        # 障碍检测：幽灵模式可以穿过障碍
        if new_head in self.obstacles:
            if not self.ghost_mode:
                self.trigger_game_over("撞到荆棘了！")
                return

        # 自身碰撞（根据幽灵模式判断是否死亡）
        if new_head in self.snake:
            if not self.ghost_mode:
                self.trigger_game_over("撞到自己了！")
                return
            # 幽灵模式下可以穿过身体：尾部仍然会移动

        # 移动：在前面加新头
        self.snake.insert(0, new_head)

        ate_food = False
        # 吃普通食物
        if self.food_pos and new_head == self.food_pos:
            ate_food = True
            self.score += 1
            self.normal_food_eaten += 1
            # 触发粒子特效
            food_screen_x = self.food_pos[0] * CELL_SIZE + CELL_SIZE // 2
            food_screen_y = self.food_pos[1] * CELL_SIZE + CELL_SIZE // 2
            self.particle_system.emit(food_screen_x, food_screen_y, FOOD_COLOR, count=25)
            # 触发身体刷光效果
            self.trigger_glow_effect(FOOD_COLOR)
            self.food_pos = None

            # 吃够一定数量普通食物后，生成障碍
            if self.normal_food_eaten % FOOD_PER_OBSTACLE == 0:
                self.spawn_obstacle()

        # 吃能量食物
        if self.energy_food_pos and new_head == self.energy_food_pos:
            # 触发能量食物粒子特效（黄色）
            energy_screen_x = self.energy_food_pos[0] * CELL_SIZE + CELL_SIZE // 2
            energy_screen_y = self.energy_food_pos[1] * CELL_SIZE + CELL_SIZE // 2
            self.particle_system.emit(energy_screen_x, energy_screen_y, ENERGY_FOOD_COLOR, count=30)
            # 触发身体刷光效果
            self.trigger_glow_effect(ENERGY_FOOD_COLOR)
            self.energy_food_pos = None
            self.energy += 1

        # 如果没有吃普通食物，尾巴要前进（去掉最后一个块）
        if not ate_food:
            self.snake.pop()

        # 如果食物被吃掉了，就重新生成
        if self.food_pos is None:
            self.spawn_food()

    # -------------------- 绘制相关 --------------------
    def draw_text_with_glow(self, text, font, color, pos, center=False):
        """绘制带发光效果的文字"""
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect()
        if center:
            text_rect.center = pos
        else:
            text_rect.topleft = pos
        
        # 绘制发光层
        glow_color = tuple(max(0, c - 50) for c in color)
        for offset in [(2,2), (-2,2), (2,-2), (-2,-2), (0,2), (0,-2), (2,0), (-2,0)]:
            glow_surf = font.render(text, True, glow_color)
            glow_pos = (text_rect.x + offset[0], text_rect.y + offset[1])
            self.screen.blit(glow_surf, glow_pos)
        
        # 绘制主文字
        self.screen.blit(text_surf, text_rect)
        return text_rect
    
    def draw_grid(self):
        """绘制赛博朋克风格的网格"""
        # 主网格线
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        # 每隔5格绘制高亮线
        bright_grid = (80, 40, 120)
        for x in range(0, SCREEN_WIDTH, CELL_SIZE * 5):
            pygame.draw.line(self.screen, bright_grid, (x, 0), (x, SCREEN_HEIGHT), 2)
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE * 5):
            pygame.draw.line(self.screen, bright_grid, (0, y), (SCREEN_WIDTH, y), 2)

    def draw_snake(self):
        """绘制蛇（带霓虹发光效果和刷光效果）"""
        # 计算刷光效果进度
        glow_progress = -1  # -1表示无效，0-1表示从头到尾的进度
        if self.glow_effect_active:
            elapsed = pygame.time.get_ticks() - self.glow_effect_start
            if elapsed < self.glow_effect_duration:
                glow_progress = elapsed / self.glow_effect_duration
            else:
                self.glow_effect_active = False
        
        snake_length = len(self.snake)
        
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if i == 0:
                color = SNAKE_HEAD_COLOR
                glow_color = SNAKE_HEAD_COLOR
            else:
                color = SNAKE_COLOR
                glow_color = SNAKE_GLOW

            # 刷光效果：检查当前节点是否应该被刷光点亮
            is_glowing = False
            if glow_progress >= 0 and snake_length > 0:
                # 计算刷光应该到达的节点索引（带点宽度，让刷光更明显）
                glow_position = glow_progress * snake_length
                glow_width = 3  # 刷光的宽度（几个节点同时亮）
                if abs(i - glow_position) < glow_width:
                    is_glowing = True
                    # 根据距离计算亮度
                    distance_factor = 1.0 - abs(i - glow_position) / glow_width
                    # 替换颜色为刷光颜色
                    blend_factor = distance_factor * 0.8
                    color = tuple(
                        int(color[j] * (1 - blend_factor) + self.glow_effect_color[j] * blend_factor)
                        for j in range(3)
                    )
                    glow_color = self.glow_effect_color

            if self.ghost_mode:
                # 幽灵模式下半透明效果
                shade = 60
                color = (
                    min(color[0] + shade, 255),
                    min(color[1] + shade, 255),
                    min(color[2] + shade, 255),
                )
            
            # 绘制发光层（多层，越外越淡）
            glow_intensity = 6 if is_glowing else 4  # 刷光时加强发光
            for offset in range(glow_intensity, 0, -1):
                glow_rect = pygame.Rect(
                    x * CELL_SIZE - offset,
                    y * CELL_SIZE - offset,
                    CELL_SIZE + offset * 2,
                    CELL_SIZE + offset * 2
                )
                alpha_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                alpha = (40 if is_glowing else 30) // offset
                pygame.draw.rect(alpha_surf, (*glow_color, alpha), alpha_surf.get_rect(), border_radius=3)
                self.screen.blit(alpha_surf, glow_rect)
            
            # 绘制实体
            pygame.draw.rect(self.screen, color, rect, border_radius=2)
            # 内部高光
            inner_rect = pygame.Rect(x * CELL_SIZE + 2, y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            if is_glowing:
                # 刷光时内部更亮
                lighter = tuple(min(c + 100, 255) for c in color)
            else:
                lighter = tuple(min(c + 50, 255) for c in color)
            pygame.draw.rect(self.screen, lighter, inner_rect, border_radius=1)

    def draw_foods(self):
        """绘制食物（带霓虹发光和脉冲效果）"""
        pulse = abs((pygame.time.get_ticks() % 1000) / 500 - 1)  # 0-1-0 脉冲
        
        if self.food_pos:
            x, y = self.food_pos
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = y * CELL_SIZE + CELL_SIZE // 2
            
            # 发光层（脉冲效果）
            glow_radius = int(CELL_SIZE * 0.8 + pulse * 8)
            for r in range(glow_radius, CELL_SIZE // 2, -2):
                alpha = int(60 * (1 - (glow_radius - r) / glow_radius))
                s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*FOOD_GLOW, alpha), (r, r), r)
                self.screen.blit(s, (cx - r, cy - r))
            
            # 实体
            pygame.draw.circle(self.screen, FOOD_COLOR, (cx, cy), CELL_SIZE // 2 - 2)
            # 高光
            pygame.draw.circle(self.screen, (255, 150, 200), (cx - 3, cy - 3), CELL_SIZE // 4)

        if self.energy_food_pos:
            x, y = self.energy_food_pos
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            
            # 发光层（脉冲效果）
            glow_size = int(pulse * 6)
            for offset in range(6, 0, -1):
                glow_rect = pygame.Rect(
                    x * CELL_SIZE - offset - glow_size,
                    y * CELL_SIZE - offset - glow_size,
                    CELL_SIZE + (offset + glow_size) * 2,
                    CELL_SIZE + (offset + glow_size) * 2
                )
                alpha_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                alpha = 40 // offset
                pygame.draw.rect(alpha_surf, (*ENERGY_GLOW, alpha), alpha_surf.get_rect(), border_radius=10)
                self.screen.blit(alpha_surf, glow_rect)
            
            # 实体（菱形）
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            points = [
                (center_x, center_y - CELL_SIZE // 2 + 2),
                (center_x + CELL_SIZE // 2 - 2, center_y),
                (center_x, center_y + CELL_SIZE // 2 - 2),
                (center_x - CELL_SIZE // 2 + 2, center_y)
            ]
            pygame.draw.polygon(self.screen, ENERGY_FOOD_COLOR, points)
            # 内部高光
            inner_points = [
                (center_x, center_y - CELL_SIZE // 4),
                (center_x + CELL_SIZE // 4, center_y),
                (center_x, center_y + CELL_SIZE // 4),
                (center_x - CELL_SIZE // 4, center_y)
            ]
            pygame.draw.polygon(self.screen, (255, 255, 150), inner_points)

    def draw_obstacles(self):
        """绘制荆棘障碍（赛博朋克风格）"""
        for x, y in self.obstacles:
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = y * CELL_SIZE + CELL_SIZE // 2
            
            # 发光层（圆形扩散）
            for r in range(18, 8, -2):
                alpha = int(60 * (18 - r) / 18)
                s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*OBSTACLE_GLOW, alpha), (r, r), r)
                self.screen.blit(s, (center_x - r, center_y - r))
            
            # 中心危险标志（X形）
            danger_color = OBSTACLE_COLOR
            line_width = 3
            offset = CELL_SIZE // 3
            
            # X 的两条线
            pygame.draw.line(
                self.screen, danger_color,
                (center_x - offset, center_y - offset),
                (center_x + offset, center_y + offset),
                line_width
            )
            pygame.draw.line(
                self.screen, danger_color,
                (center_x + offset, center_y - offset),
                (center_x - offset, center_y + offset),
                line_width
            )
            
            # 四个方向的尖刺
            spike_length = CELL_SIZE // 2 - 2
            spike_width = 6
            
            # 上尖刺
            spike_top = [
                (center_x, center_y - spike_length),
                (center_x - spike_width, center_y),
                (center_x + spike_width, center_y)
            ]
            pygame.draw.polygon(self.screen, danger_color, spike_top)
            pygame.draw.polygon(self.screen, (255, 100, 255), spike_top, 2)
            
            # 下尖刺
            spike_bottom = [
                (center_x, center_y + spike_length),
                (center_x - spike_width, center_y),
                (center_x + spike_width, center_y)
            ]
            pygame.draw.polygon(self.screen, danger_color, spike_bottom)
            pygame.draw.polygon(self.screen, (255, 100, 255), spike_bottom, 2)
            
            # 左尖刺
            spike_left = [
                (center_x - spike_length, center_y),
                (center_x, center_y - spike_width),
                (center_x, center_y + spike_width)
            ]
            pygame.draw.polygon(self.screen, danger_color, spike_left)
            pygame.draw.polygon(self.screen, (255, 100, 255), spike_left, 2)
            
            # 右尖刺
            spike_right = [
                (center_x + spike_length, center_y),
                (center_x, center_y - spike_width),
                (center_x, center_y + spike_width)
            ]
            pygame.draw.polygon(self.screen, danger_color, spike_right)
            pygame.draw.polygon(self.screen, (255, 100, 255), spike_right, 2)
            
            # 中心圆点
            pygame.draw.circle(self.screen, (255, 0, 200), (center_x, center_y), 4)
            pygame.draw.circle(self.screen, (255, 150, 255), (center_x, center_y), 2)

    def draw_hud(self):
        """绘制HUD（赛博朋克风格）"""
        # 左上角：分数 / 能量 / 幽灵剩余时间
        time_left = 0
        if self.ghost_mode:
            time_left = max(0, (self.ghost_end_time - pygame.time.get_ticks()) // 1000)

        text = f"Score: {self.score}   Energy: {self.energy}   "
        if self.ghost_mode:
            text += f"Ghost: {time_left}s"
        else:
            text += "Ghost: OFF"

        self.draw_text_with_glow(text, self.font_small, TEXT_COLOR, (8, 4))

        # 右上角显示最高分
        if self.leaderboard:
            high_score_text = f"最高分: {self.leaderboard[0]['score']}"
            self.draw_text_with_glow(high_score_text, self.font_small, (255, 215, 0), (SCREEN_WIDTH - 120, 4))

        hint_text = "方向键/WASD 移动，空格 幽灵模式，Tab 排行榜，ESC 退出"
        hint_color = (150, 150, 200)
        self.draw_text_with_glow(hint_text, self.font_small, hint_color, (8, SCREEN_HEIGHT - 24))

    def draw_game_over(self):
        """绘制Game Over界面（赛博朋克风格）"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((10, 5, 20))
        self.screen.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        # 标题带闪烁效果
        blink = (pygame.time.get_ticks() // 500) % 2
        title_color = (255, 0, 127) if blink else (255, 50, 150)
        self.draw_text_with_glow("GAME OVER", self.font_big, title_color, (center_x, center_y - 60), center=True)
        
        self.draw_text_with_glow(self.game_over_reason, self.font_small, TEXT_COLOR, (center_x, center_y - 10), center=True)
        self.draw_text_with_glow(f"最终得分: {self.score}", self.font_small, (255, 255, 0), (center_x, center_y + 20), center=True)
        
        # 显示最高分
        if self.leaderboard:
            high_score_text = f"最高分: {self.leaderboard[0]['score']} ({self.leaderboard[0]['name']})"
            self.draw_text_with_glow(high_score_text, self.font_small, (255, 215, 0), (center_x, center_y + 50), center=True)
        else:
            self.draw_text_with_glow("暂无最高分", self.font_small, (150, 150, 150), (center_x, center_y + 50), center=True)
        
        self.draw_text_with_glow("按 R 重新开始，Tab 查看排行榜，ESC 退出", self.font_small, (200, 200, 220), (center_x, center_y + 80), center=True)

    def draw_start_screen(self):
        """绘制开始界面（赛博朋克风格）"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(210)
        overlay.fill((10, 5, 20))
        self.screen.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        # 标题带脉冲效果
        pulse = abs((pygame.time.get_ticks() % 2000) / 1000 - 1)
        title_color = (
            int(255),
            int(100 + pulse * 100),
            int(200 + pulse * 55)
        )
        self.draw_text_with_glow("技能贪吃蛇", self.font_big, title_color, (center_x, center_y - 60), center=True)
        self.draw_text_with_glow("幽灵模式 + 动态障碍", self.font_small, TEXT_COLOR, (center_x, center_y - 20), center=True)
        
        # 显示最高分
        if self.leaderboard:
            high_score_text = f"最高分: {self.leaderboard[0]['score']} ({self.leaderboard[0]['name']})"
            self.draw_text_with_glow(high_score_text, self.font_small, (255, 215, 0), (center_x, center_y + 10), center=True)
        else:
            self.draw_text_with_glow("暂无记录", self.font_small, (150, 150, 150), (center_x, center_y + 10), center=True)
        
        # 提示文字带闪烁
        blink = (pygame.time.get_ticks() // 800) % 2
        tip_alpha = 220 if blink else 150
        tip_color = (tip_alpha, tip_alpha, 255)
        self.draw_text_with_glow("按空格键开始 (Tab 查看排行榜，ESC 退出)", self.font_small, tip_color, (center_x, center_y + 50), center=True)
        self.draw_text_with_glow("方向键/WASD 移动；空格开启幽灵模式；Tab 暂停并查看排行榜", self.font_small, (190, 190, 210), (center_x, center_y + 80), center=True)

    def draw_leaderboard(self):
        """绘制排行榜界面（赛博朋克风格）"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((10, 5, 20))
        self.screen.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2
        self.draw_text_with_glow("排行榜 TOP 10", self.font_big, (255, 215, 0), (center_x, 40), center=True)
        
        # 只在游戏进行中时显示暂停提示
        if self.started and not self.game_over:
            self.draw_text_with_glow("(游戏已暂停)", self.font_small, (180, 180, 210), (center_x, 75), center=True)
            y_start = 110
        else:
            y_start = 90

        if not self.leaderboard:
            self.draw_text_with_glow("暂无记录", self.font_small, TEXT_COLOR, (center_x, y_start + 40), center=True)
        else:
            y_offset = y_start
            for i, entry in enumerate(self.leaderboard[:MAX_LEADERBOARD_ENTRIES]):
                rank_text = f"{i+1}. {entry['name']}"
                score_text = f"{entry['score']}"
                
                # 前三名用不同颜色（赛博朋克配色）
                if i == 0:
                    color = (255, 215, 0)  # 金色
                elif i == 1:
                    color = (0, 255, 255)  # 青色
                elif i == 2:
                    color = (255, 0, 255)  # 品红
                else:
                    color = TEXT_COLOR

                self.draw_text_with_glow(rank_text, self.font_small, color, (center_x - 150, y_offset))
                self.draw_text_with_glow(score_text, self.font_small, color, (center_x + 100, y_offset))
                y_offset += 30

        self.draw_text_with_glow("按 Tab 返回", self.font_small, (200, 200, 220), (center_x, SCREEN_HEIGHT - 40), center=True)

    def draw_name_input(self):
        """绘制输入名字界面（赛博朋克风格）"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((10, 5, 20))
        self.screen.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        # 恭喜文字带闪烁
        blink = (pygame.time.get_ticks() // 300) % 2
        congrats_color = (255, 215, 0) if blink else (255, 255, 0)
        self.draw_text_with_glow("新纪录！", self.font_big, congrats_color, (center_x, center_y - 80), center=True)
        self.draw_text_with_glow("请输入你的名字：", self.font_small, TEXT_COLOR, (center_x, center_y - 30), center=True)
        
        # 输入框（霓虹边框）
        input_box_width = 300
        input_box_height = 40
        input_box = pygame.Rect(center_x - input_box_width//2, center_y, input_box_width, input_box_height)
        
        # 绘制发光边框
        for offset in range(3, 0, -1):
            glow_rect = input_box.inflate(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, (0, 100, 200, 80 // offset), glow_rect, 2, border_radius=5)
        
        pygame.draw.rect(self.screen, (30, 20, 50), input_box, border_radius=3)
        pygame.draw.rect(self.screen, (0, 255, 255), input_box, 2, border_radius=3)
        
        # 显示输入的文字
        cursor_blink = "_" if (pygame.time.get_ticks() // 500) % 2 else " "
        self.draw_text_with_glow(self.player_name_input + cursor_blink, self.font_small, (255, 255, 255), (input_box.x + 10, input_box.y + 10))

        self.draw_text_with_glow("回车确认，ESC 跳过", self.font_small, (200, 200, 220), (center_x, center_y + 60), center=True)

    # -------------------- 主循环 --------------------
    def run(self):
        while True:
            self.handle_input()

            # 启动画面：未开始时仅渲染，不更新逻辑
            if not self.started:
                self.screen.fill(BG_COLOR)
                self.draw_grid()
                self.draw_obstacles()
                self.draw_foods()
                self.draw_snake()
                self.draw_hud()
                self.draw_start_screen()
                
                # 启动画面也可以查看排行榜
                if self.show_leaderboard:
                    self.draw_leaderboard()
                
                pygame.display.flip()
                self.clock.tick(self.fps)
                continue

            # Game Over 状态下单独处理 R / ESC（但不在输入名字时）
            if self.game_over and not self.entering_name:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self.reset(start_with_intro=False)
                elif keys[pygame.K_ESCAPE]:
                    pygame.quit()
                    sys.exit()

            # 只在游戏进行中且未暂停时更新逻辑
            if not self.game_over and not self.paused:
                self.update()
            
            # 粒子系统始终更新（即使游戏暂停）
            self.particle_system.update()

            self.screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_obstacles()
            self.draw_foods()
            self.draw_snake()
            
            # 绘制粒子特效（在蛇上面）
            self.particle_system.draw(self.screen)
            
            self.draw_hud()

            if self.game_over:
                self.draw_game_over()

            # 显示排行榜（覆盖在游戏画面上）
            if self.show_leaderboard:
                self.draw_leaderboard()

            # 显示名字输入界面（覆盖在 game over 上）
            if self.entering_name:
                self.draw_name_input()

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    # 防止多次导入时自动运行
    game = SnakeGame()
    game.run()


