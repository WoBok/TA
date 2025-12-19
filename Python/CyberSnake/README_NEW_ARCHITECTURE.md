# CyberSnake - 新架构说明

## 🎯 项目概述

CyberSnake 已完成全面重构，采用 **ECS（Entity-Component-System）架构** 和 **插件系统**，实现了高度模块化和可扩展的设计。

## 🚀 快速开始

### 运行游戏

```bash
# 新版本（ECS + 插件系统）
python main_ecs.py

# 旧版本（兼容保留）
python main.py
```

### 测试插件系统

```bash
python test_plugins.py
```

## 📖 核心文档

| 文档 | 内容 |
|------|------|
| `QUICK_START.md` | 快速开始指南 |
| `REFACTORING_COMPLETE.md` | 重构完成总结 |
| `plugins/README.md` | 插件系统文档 |
| `doc/REFACTORING_SUMMARY.md` | 详细重构说明 |
| `doc/PLUGIN_DEVELOPMENT_GUIDE.md` | 插件开发指南 |

## 🏗️ 架构特点

### ECS 架构

- **Entity（实体）** - 游戏对象容器
- **Component（组件）** - 数据存储
- **System（系统）** - 逻辑处理

### 插件系统

支持四种插件类型：
1. **FoodPlugin** - 食物
2. **ObstaclePlugin** - 障碍
3. **EnemyPlugin** - 敌人
4. **SnakeModifierPlugin** - 修改器

### 事件总线

所有模块通过事件总线通信，实现完全解耦。

## 🎮 示例插件

- `basic_food` - 基础食物（普通、能量）
- `basic_obstacle` - 基础障碍（静态）
- `basic_enemy` - 基础敌人（游走）
- `superbomb` - 超级炸弹（完整示例）

## 🔧 创建插件

### 1. 复制模板

```bash
Copy-Item -Recurse plugins\PLUGIN_TEMPLATE plugins\my_plugin
```

### 2. 重命名文件

```
template_main.py → my_plugin_main.py
template_food.py → my_plugin_food.py
template_obstacle.py → my_plugin_obstacle.py
template_enemy.py → my_plugin_enemy.py
template_snakemodify.py → my_plugin_snakemodify.py
```

### 3. 实现插件

参考 `plugins/PLUGIN_TEMPLATE/` 中的详细注释。

### 4. 运行游戏

插件会自动加载！

## ✨ 核心优势

- ✅ **热插拔** - 添加/移除插件无需修改核心代码
- ✅ **模块化** - 每个插件完全独立
- ✅ **可扩展** - 轻松添加新功能
- ✅ **解耦合** - 通过事件总线通信
- ✅ **易维护** - 清晰的代码结构

## 📂 项目结构

```
CyberSnake/
├── src/
│   ├── ecs/              # ECS核心
│   ├── plugins/          # 插件系统
│   └── scenes/           # 游戏场景
├── plugins/              # 插件目录
│   ├── PLUGIN_TEMPLATE/  # 插件模板
│   ├── basic_food/       # 示例插件
│   ├── basic_obstacle/
│   ├── basic_enemy/
│   └── superbomb/
├── doc/                  # 文档
├── main_ecs.py           # 新版入口
└── test_plugins.py       # 测试脚本
```

## 🎓 学习路径

1. 阅读 `QUICK_START.md`
2. 运行 `python test_plugins.py`
3. 查看示例插件代码
4. 阅读 `doc/PLUGIN_DEVELOPMENT_GUIDE.md`
5. 创建自己的插件

## 💡 需求实现

本次重构完全实现了 `doc/plan_04.md` 的所有需求：

- ✅ ECS架构
- ✅ 事件总线
- ✅ 插件接口（4种）
- ✅ 自动注册
- ✅ 热插拔
- ✅ 冲突解决
- ✅ 模板示例

## 🐍 开始创建你的插件吧！

查看 `QUICK_START.md` 获取详细指导。
