[3 tools called]

我复现并定位到了原因：每一帧蛇身被多 pop 了一次，长度会不断变短，最终 body 变成空列表，导致 Snake.head() 取 body[0] 抛出 IndexError。

问题点
- 在 GameScene.update 中，先执行了 self.snake.step(ate_food)，但此时 ate_food 还是 False，step 内部已经把尾巴 pop 掉了一次。
- 之后又有一段 if not ate_food: self.snake.body.pop()，导致没吃到食物时再多 pop 一次，每帧都会缩短 1 节。

已修复
1) 修正增长/收缩逻辑，去掉多余的 pop
- 文件：src/scenes/game_scene.py
- 修改后的尾部逻辑：
  - 吃到食物时，补一节尾巴以实现“增长”（因为 step 已经先 pop 过一次）
  - 没吃到食物时不再额外 pop（step 已经做过一次）
- 片段：
  - 原来：
    if not ate_food:
        self.snake.body.pop()
  - 现在：
    if ate_food:
        if self.snake.body:
            self.snake.body.append(self.snake.body[-1])
    # 不再额外 pop

2) 防御性修复，避免空蛇身直接崩溃
- 文件：src/entities/snake.py
- head() 加了保护：
  - 原来：return self.body[0]
  - 现在：return self.body[0] if self.body else (0, 0)

3) 顺手修正两个潜在问题（避免后续再报错）
- src/scenes/game_scene.py
  - 导入 HUD_HEIGHT（draw_hud 用到了）
  - spawn_ai_snake 调用了 random_empty_cell(for_snake=True)，但该函数没有这个参数，已改为 random_empty_cell()

为什么这样改
- step 本身已经处理了“移动 + 若不增长则 pop 尾巴”。由于是否吃到食物需要在 step 后才能判定，所以正确做法是：
  - 永远先 step(False)
  - 若判定吃到食物，再在外部补一节，达到增长的效果
  - 否则不做任何事，维持长度不变

请重新运行 main.py 测试一下。如果还有问题（例如蛇身长度异常或其它实体交互），把新的报错贴出来我继续跟进。注意不要直接运行单个模块（如 src/entities/boss.py），而是运行 main.py。