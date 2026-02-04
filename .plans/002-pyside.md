# PySide6 迁移计划

## 需求理解

1. **框架迁移**：Tkinter → PySide6
2. **UI 风格**：Windows 原生风格适配
3. **视觉效果**：窗口半透明效果（磨砂玻璃）
4. **系统托盘**：程序最小化至托盘运行
5. **兼容性**：确保原有功能完整保留

---

## 阶段一：基础窗口与框架搭建

### 1.1 PySide6 入口
- [x] 创建 `packages/windows-app/ui/__init__.py`
- [x] 创建 `packages/windows-app/ui/main_window.py`
- [x] 重写 `main.py`，使用新窗口类
- [x] 窗口框架运行验证成功

### 1.2 还原原 UI 设计
- [x] 左右分栏 QTextEdit（左侧输入，右侧输出）
- [x] 润色按钮（中间）
- [x] Accept 按钮（底部）
- [x] 设置窗口 Topmost
- [ ] 提供 `show()` / `hide()` 方法
- [ ] 提供 `get_output_text()` 方法

> **阶段一产出**：PySide6 窗口

---

## 阶段二：系统托盘

### 2.1 创建 SystemTrayIcon 类
- [x] 创建 `ui/system_tray.py`
- [x] 继承 `QSystemTrayIcon`
- [x] 初始化托盘图标
- [x] 设置右键菜单

### 2.2 托盘菜单项
- [x] "显示窗口" - 点击显示主窗口
- [x] "退出" - 点击退出程序

### 2.3 窗口与托盘联动
- [x] 点击关闭按钮时最小化到托盘（不退出程序）
- [x] 窗口关闭事件重写：`closeEvent` → `hide()`
- [x] 托盘"显示窗口"唤醒主窗口

### 2.4 窗口按钮设置
- [x] 仅保留关闭按钮
- [x] 移除最小化、最大化按钮

---

## 阶段三：视觉效果

### 3.1 效果目标
- 保持系统标题栏不变
- 内容区域（文本框、按钮）半透明
- 磨砂玻璃/模糊效果

### 3.2 实现方案
- 给 `central_widget` 设置半透明样式
- 使用 `rgba(r, g, b, alpha)` 控制透明度
- 可选：添加 border-radius 圆角

### 3.3 任务拆分

#### 3.3.1 内容区域半透明样式
- [ ] 给 central_widget 添加半透明样式
- [ ] 调整透明度参数
- [ ] 添加圆角效果

#### 3.3.2 控件背景
- [ ] 测试 QTextEdit 背景可见性
- [ ] 测试按钮清晰度

---

## 阶段四：功能迁移（逐个迁移 gui.py 函数）

### 目标：最终删除 gui.py

### 迁移清单（按依赖顺序）

#### 阶段 4.1 基础方法迁移
- [x] 迁移 `TEXT_FONT_FAMILIES` 常量
- [x] 迁移 `show()` 方法（全选 + 焦点）
- [x] 迁移 `hide()` 方法
- [x] 迁移 `get_output_text()` 方法

#### 阶段 4.2 润色按钮迁移
- [x] 迁移 `_on_polish()` 按钮回调
- [x] 添加 wisadel 实例支持
- [x] 迁移 `_on_accept()` 按钮回调

#### 阶段 4.3 Agent 集成
- [x] main.py 中创建 wisadel 实例
- [x] 传递给 MainWindow
- [x] 异步处理润色任务（QThread）
  - [x] 创建 `polish_worker.py` 文件（PolishWorker 类）
    - [x] 继承 QThread
    - [x] 定义信号：finished(str), error(str)
    - [x] 实现 run() 方法调用 wisadel.run()
  - [x] 修改 `main_window.py`
    - [x] 添加导入：QThread, PolishWorker
    - [x] 添加成员变量：self.polish_worker = None
    - [x] 重写 `_on_polish()` 方法
      - [x] 防止重复点击
      - [x] 创建并启动工作线程
      - [x] 连接信号到回调
    - [x] 添加 `_on_polish_finished(result)` 回调
    - [x] 添加 `_on_polish_error(error_msg)` 回调
    - [x] 添加 `closeEvent()` 清理资源
  - [ ] 测试异步润色功能

#### 阶段 4.3.1 窗口焦点优化
- [ ] 修复手动切换窗口时焦点问题
  - [ ] 添加导入：QEvent
  - [ ] 重写 `changeEvent()` 方法监听窗口激活
  - [ ] 提取焦点获取逻辑为私有方法 `_focus_left_text()`
  - [ ] 在 `show()` 和 `changeEvent()` 中调用
  - [ ] 测试快捷键和手动切换窗口场景

#### 阶段 4.4 完成迁移
- [x] 删除 gui.py
- [ ] 验证所有功能正常
