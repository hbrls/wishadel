# MVP3 实现计划

> 基于 [000-mvp3.md](../.specs/000-mvp3.md) 规格文档

---

## 阶段划分与功能递进

各 Task 不是独立的单元测试，而是 **功能递进**。每完成一个 Task，`main.py` 就是当前完整可用的程序：

| 阶段 | 名称 | 目标 | main.py 行为 |
|------|------|------|-------------|
| Task 0 | 环境搭建 | 依赖安装、项目结构 | 空壳，打印启动信息 |
| Task 1 | GUI 窗口 | Tkinter 双文本区 + 按钮 | 启动 GUI，Accept 打印文本 |
| Task 2 | 焦点管理 + 文本注入 | 记录/恢复焦点、WM_CHAR 注入 | Accept 后隐藏 GUI + 恢复焦点 + 注入测试文本 |
| Task 3 | 全局快捷键 | Alt+W 可触发回调 | 启动时隐藏 GUI，通过快捷键唤起（唤起时记录原窗口） |
| Task 4 | 复杂文本验证 | 中文、换行、长文本 | 验证复杂文本（中文、换行、长文本） |
| Task 5 | 集成联调 | 完整流程验证 | 完整流程（端到端验证） |
| Task 6 | 日志模块 | logger.py 实现 | 增加日志输出 |
| Task 7 | 打包发布 | PyInstaller 生成 exe | 打包为 exe |

---

## Task 0：环境搭建

### 任务清单

- [x] 创建项目目录 `packages/windows-app/`
- [x] 创建 `requirements.txt`
- [x] 创建入口文件 `main.py`

> 虚拟环境由 PyCharm 管理，不在此计划中
> 依赖管理以项目实际使用的 `requirements.txt` 为准

### 目录结构

```
packages/windows-app/
├── main.py              # 主入口
├── hotkey.py            # 全局快捷键模块
├── focus.py             # 焦点管理 + 文本注入模块
├── gui.py               # Tkinter GUI 模块
├── logger.py            # 日志模块
├── requirements.txt     # Python 依赖列表
├── build.bat            # PyInstaller 打包脚本
├── Wisadel.spec         # PyInstaller 配置文件
└── dist/                # PyInstaller 输出目录
    └── Wisadel.exe      # 打包后的可执行文件
```

---

## Task 1：GUI 窗口

### 任务清单

- [x] 实现 `gui.py`
- [x] 创建 Tkinter 窗口，设置 Topmost
- [x] 左右两个 Text widget
- [x] Accept 按钮
- [x] 窗口可拖动
- [x] 提供 `show()` / `hide()` 方法

### 接口声明

```python
class PolishWindow:
    def __init__(self, on_accept_callback)
    def show()
    def hide()
    def get_output_text() -> str
```

### 验证点

- [x] 窗口始终置顶
- [x] 可输入中文
- [x] Accept 按钮可点击

---

## Task 2：焦点管理 + 文本注入

### 任务清单

- [x] 实现 `focus.py`
- [x] 使用 `ctypes` 调用 Windows API 获取当前窗口句柄
- [x] 使用 `ctypes` 调用 Windows API 恢复焦点
- [x] 使用 `WM_CHAR` 方案注入文本（绕过输入法）
- [x] 验证：记录句柄后切换窗口，能恢复原窗口并输入测试文本

### 接口声明

```python
class FocusManager:
    def __init__(self)
    def save_current_focus() -> int  # 返回窗口句柄
    def restore_focus(delay_ms: int = 100)
    def type_text(text: str)  # 向当前焦点窗口注入文本
```

### 验证点

- [x] 能正确获取 HWND
- [x] 能恢复焦点到原窗口
- [x] 延迟参数可调
- [x] 英文和中文文本可注入

> 备注：使用 WM_CHAR + PostMessageW 方案，绕过输入法拦截
> 
> **为何 SendInput 会被输入法干扰**：
> - SendInput 发送的是虚拟按键码（VK），输入法会拦截这些按键事件
> - 中文输入法会将按键序列转换为拼音候选，而不是直接输入字符
> - WM_CHAR 消息是系统已处理完成的字符消息，输入法不会再次拦截，可直接输入 Unicode 字符

---

## Task 3：全局快捷键

### 任务清单

- [x] 实现 `hotkey.py`
- [x] 使用 `keyboard` 库监听 `Alt+W`
- [x] 触发时调用回调函数
- [x] 验证：在记事本中按 Alt+W 能打印日志

### 接口声明

```python
def register_hotkey(hotkey: str, callback: callable)
```

### 验证点

- [x] Alt+W 在任意应用中可触发

> 备注：使用 `suppress=True` 阻止 Alt+W 键本身传递给前台应用，避免快捷键被前台应用处理（如触发应用的菜单快捷键）

---

## Task 4：复杂文本验证

### 任务清单

- [x] 验证中文字符注入
- [x] 验证换行符处理
- [x] 验证长文本（500+ 字符）
- [x] 如需调整，更新 `focus.py` 的 `type_text()` 方法

### 测试文本

实际使用的综合测试用例（约 150 字，包含 Markdown 格式、英文、中文、Emoji、特殊符号、多行文本）：

```
# MVP3 文本润色工具 🚀

## 功能验证 ✅

The quick brown fox jumps over the lazy dog.
敏捷的棕色狐狸跳过了懒惰的狗。🦊

### 测试项

- **英文字符**: ABCDEFG abcdefg 0123456789
- **中文字符**: 你好世界，这是一段测试文本
- **特殊符号**: @#$%^&*() 【】「」
- **Emoji**: 😀 🎉 💻 ❤️ 👍

> 这是一段引用文字，用于测试多行场景。

完成！Done! 🎊
```

### 验证点

- [x] 中文字符正确显示
- [x] 换行正确处理（记事本出现多行）
- [x] 长文本无丢字符
- [x] Emoji 处理

> 备注：采用混合方案
> - 普通字符：WM_CHAR（绕过输入法）
> - 换行：SendInput 发送 Shift+Enter（软换行，避免触发聊天发送）
> - SendInput 后需延迟 50ms（原 10ms 有时序问题）

### 疑点

- **SendInput 时序问题**：SendInput 发送 Shift+Enter 后需要 50ms 延迟，10ms 会导致异常行为（具体原因未明，可能是 WM_CHAR 与 SendInput 混用时消息队列处理顺序问题）

- **Alt+W 唤起后焦点争抢**：窗口 topmost 但不一定获得焦点（表现为任务栏闪烁）
  - 原因：Windows 前台窗口保护机制，后台进程调用 `SetForegroundWindow` 会被拒绝
  - 解决方案：使用 `SetForegroundWindow(hwnd)`，部分应用不兼容（VSCode ✓，Trae ✗）

### 风险

- 部分应用可能不响应 WM_CHAR
- 某些特殊字符可能需要特殊处理

---

## Task 5：集成联调

### 任务清单

- [x] 在 `main.py` 中组装所有模块
- [x] 实现完整流程（快捷键 → GUI → Accept → 恢复焦点 → 注入文本）
- [x] 端到端测试（记事本、Chrome textarea）
- [x] 多应用切换场景测试
- [x] 实现 Alt+W 唤起时左侧文本全选（方案 C）

### 核心流程

Accept 回调执行顺序：
1. 隐藏 GUI 窗口
2. 恢复焦点到原窗口（延迟 50-200ms）
3. 注入文本到目标窗口

### 测试场景

| 场景 | 测试应用 | 预期结果 |
|------|----------|----------|
| 基本流程 | 记事本 | 文本完整写入 |
| 中文输入 | 记事本 | 中文正确显示 |
| 换行处理 | 记事本 | 多行文本正确 |
| 长文本 | 记事本 | 500字符无丢失 |
| 浏览器 | Chrome textarea | 文本正确写入 |

### 多应用切换用例

> 工具是全局的，用户会在多个应用间切换使用

1. 在记事本中按 Alt+W 唤起工具
2. 输入/润色文本，点 Accept 上屏到记事本
3. 用户主动切换到 Chrome
4. 在 Chrome 中按 Alt+W 再次唤起工具
5. 输入/润色文本，点 Accept 上屏到 Chrome

**问题**：步骤 4 再次唤起时，之前的文本没有清空

**解决方案**：Alt+W 唤起时自动全选左侧文本，用户直接输入即覆盖，也可通过方向键取消选中保留旧文本

---

## Task 6：日志模块

### 任务清单

- [x] 实现 `logger.py`
- [x] 开发阶段：控制台输出
- [ ] exe 形态：输出到 `Wisadel.log`

### 记录内容

- 全局快捷键触发事件
- 原窗口句柄（HWND）
- GUI 显示/隐藏状态
- 焦点恢复调用结果
- 文本注入开始/结束

### 约束

- 不记录用户文本内容
- 单个日志文件不超过 1MB
- **注意**：当前实现未包含日志滚动功能，日志文件可能持续增长

---

## Task 7：打包发布

### 任务清单

- [ ] 安装 PyInstaller
- [ ] 创建打包脚本 `build.bat`
- [ ] 执行打包
- [ ] 在无 Python 环境测试 exe
- [ ] GUI 去掉最小化、最大化按钮

### 打包命令

```batch
pyinstaller --onefile --windowed --name Wisadel main.py
```

### 验证点

- [ ] exe 文件生成成功
- [ ] exe 可在无 Python 机器运行
- [ ] 全局快捷键正常工作
- [ ] 焦点恢复正常
- [ ] 文本注入正常
- [ ] 日志文件正确生成

---

## Task 8：系统托盘（未实现）

> MVP 不实现，记录备用

### 背景

程序以后台方式运行（Alt+W 唤起），没有常驻窗口，用户难以关闭。

### 方案

使用 `pystray` + `Pillow` 实现系统托盘图标：
- 右键菜单：显示 / 退出
- 需要协调 pystray 和 Tkinter 事件循环（独立线程）

### 新增依赖

```
pystray
Pillow
```

### 状态

- [ ] 暂不实现，MVP 保持简洁

---

## 风险与备选方案

| 风险 | 影响 | 备选方案 |
|------|------|----------|
| SendInput 被部分应用屏蔽 | 文本无法注入 | 使用剪贴板 + Ctrl+V（非 MVP 范围） |
| SetForegroundWindow 失败 | 焦点无法恢复 | 使用 AttachThreadInput 辅助 |
| PyInstaller 打包后快捷键失效 | exe 不可用 | 检查是否需要管理员权限 |

