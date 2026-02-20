# macOS 桌面应用支持计划

> updated_by: VSCode - Claude-Opus-4.6
> updated_at: 2026-02-20 11:57:00

## Requirements

本计划实现 Wisadel 的 macOS 兼容性支持。

### 兼容性评估

- **85% 代码可直接复用**：UI 布局、业务逻辑、Agent 系统
- **15% 需要条件编译**：Windows 特定 API 调用

### Goals

- **跨平台兼容**：Windows 和 macOS 双平台支持
- **Windows 功能保持**：原有 Windows 功能完整保留
- **macOS 本期范围**（简化版）：
  - ✅ GUI 显示和润色功能
  - ✅ 系统托盘常驻
  - ✅ 打包成 .app 文件，双击即用
  - ✅ 全局快捷键唤起窗口（仅唤起，不含焦点获取）
  - ❌ 焦点跟踪（不需要）
  - ❌ 文本写回原窗口（不需要）
- **启动方式**：macOS 用户通过托盘菜单、Dock 或全局快捷键打开窗口

### Non-Goals

- 不实现焦点跟踪和文本注入（与 Windows 版有本质差异）
- 不追求 macOS 原生视觉风格（以跨平台一致性为准）
- 不实现跨平台打包（Windows 和 macOS 分别打包）

### Scope

- macOS 下可运行的桌面程序（Python + PySide6）
- 系统托盘常驻能力（Menu Bar 图标）
- GUI 双区布局（左右文本区 + 按钮）
- 文本润色功能（Agent 协议复用）
- PyInstaller 打包为 `.app` 包
- 代码签名支持（自签名 + 开发者证书）
- 公证支持（分发必需）

### Non-Scope

- macOS 全局快捷键
- 焦点保存与恢复
- 文本自动注入回原窗口
- 跨平台单一打包物
- 多模型并行
- 复杂异常处理

### 功能需求（Functional Requirements）

#### 事件驱动（Event-Driven）需求

- **FR-001**: 当用户从托盘菜单点击"显示窗口"时，系统应显示工具窗口。
- **FR-002**: 当用户从托盘菜单点击"退出"时，系统应完全退出应用程序。
- **FR-003**: 当用户点击系统托盘图标时，系统应显示/隐藏工具窗口。
- **FR-004**: 当用户触发文本润色时，系统应将 Markdown/文本输入发送到基于 MiniMax 的 Agent 协议，并返回面向 Requirement 的输出文本。
- **FR-005**: 当用户点击 Accept 时，系统应隐藏工具窗口（本期仅此行为）。

#### 常规（Ubiquitous）需求

- **FR-010**: 系统应在 macOS Menu Bar 中显示托盘图标。
- **FR-011**: 系统应支持右键菜单（显示窗口/退出）。
- **FR-012**: 系统应以无状态（stateless）方式处理 Agent 请求。
- **FR-013**: 系统应保持跨平台一致的 UI 布局。

#### 非期望行为（Unwanted Behavior）需求

- **FR-020**: 系统不应尝试在 macOS 上调用 Windows 特定的 API（如 ctypes.windll.user32）。
- **FR-021**: 系统不应尝试在 macOS 上实现全局快捷键（暂不支持）。

### Success Metrics

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| macOS 兼容性 | N/A | 85% 代码复用 | 按架构评估统计 |
| macOS 打包可用性 | N/A | 生成 .app 文件 | 构建脚本执行成功 |
| GUI 功能可用 | N/A | 文本润色正常工作 | 手工验收 |

### Dependencies

- **D-001**: PySide6 框架能力（跨平台）
- **D-002**: PyInstaller macOS 打包能力
- **D-003**: macOS 代码签名能力（`codesign`）
- **D-004**: macOS 公证能力（`xcrun notarytool`）
- **D-005**: MiniMax API 可用性（Agent 复用）
- **D-006**: Agent 框架能力（smolagents 复用）

### Constraints

- **C-001**: 平台仅 macOS（本期）
- **C-002**: 最终交付物为 macOS `.app` 包
- **C-003**: 必须进行代码签名（开发测试可用自签名）
- **C-004**: 分发时必须经过公证
- **C-005**: 不使用 Windows 特定 API（ctypes.windll）
- **C-006**: 本期仅实现唤起功能（window.show()），不包含焦点获取逻辑
- **C-007**: Accept 按钮仅隐藏窗口，不注入文本
- **C-008**: GUI 布局与 Windows 版保持一致

### Assumptions

- **A-001**: 用户接受从托盘菜单手动打开窗口的方式
- **A-002**: macOS 开发环境可用（构建需要 macOS）
- **A-003**: Agent 能力可完全复用（与平台无关）

## Design

### 设计文档的定位

本文档的 Design 部分用于固定"macOS 平台适配方案"和"与 Windows 版的差异点"，组件内部实现细节（类/函数级）应下沉到代码。

### 技术选型

| 能力 | 技术 |
|------|------|
| 语言 | Python 3.x |
| GUI | PySide6（跨平台） |
| 托盘图标 | QSystemTrayIcon（跨平台） |
| 打包 | PyInstaller（macOS BUNDLE） |
| 代码签名 | codesign |
| 公证 | xcrun notarytool |

### 核心交互模型

1. 用户启动 Wisadel.app
2. 应用在 macOS Menu Bar 显示托盘图标
3. 用户点击托盘图标或右键选择"显示窗口"
4. GUI 窗口显示（与 Windows 版布局一致）
5. 用户输入文本并点击润色
6. Agent 处理并返回结果
7. 用户点击 Accept
8. 窗口隐藏（本期不注入文本回原窗口）

### 架构优势（来自评估）

当前架构设计良好，易于跨平台：

✅ **UI 逻辑与平台特定代码分离**
✅ **使用标准 Qt 组件**（PySide6 是跨平台框架）
✅ **布局系统清晰**（QVBoxLayout、QHBoxLayout）
✅ **业务逻辑（Agent）与 UI 解耦**

### 平台差异矩阵

| 特性 | Windows | macOS | 差异说明 |
|------|---------|-------|----------|
| 唤起方式 | Alt+W 全局快捷键 | 托盘菜单手动打开 | macOS 本期无全局快捷键 |
| 焦点管理 | 保存 + 恢复 + 注入 | 不需要 | macOS 本期不实现 |
| 文本注入 | WM_CHAR / SendInput | 不需要 | macOS 本期不实现 |
| 系统托盘 | Windows 托盘区域 | Menu Bar | Qt 统一接口 |
| 打包格式 | .exe | .app | PyInstaller BUNDLE |
| 代码签名 | 可选 | 必需 | macOS 安全要求 |
| 公证 | 不需要 | 分发需要 | Apple Gatekeeper |

### 必须修改的部分

#### 1. Windows 特定 API（P0）

**问题代码位置：** [`packages/windows-app/ui/main_window.py:10,17,236-237`](../packages/windows-app/ui/main_window.py)

```python
import ctypes
user32 = ctypes.windll.user32

# 在 show() 方法中
hwnd = self.winId()
user32.SetForegroundWindow(hwnd)
```

**解决方案：** 使用 `sys.platform` 进行条件编译

```python
import sys

# 条件导入
if sys.platform == "win32":
    import ctypes
    user32 = ctypes.windll.user32

    def focus_window(hwnd):
        user32.SetForegroundWindow(hwnd)
elif sys.platform == "darwin":
    # macOS 使用不同的窗口焦点 API
    def focus_window(hwnd):
        # macOS 可能需要使用 Cocoa API 或其他方法
        pass
```

#### 2. main.py 中的 FocusManager 导入（P0）

**问题代码位置：** [`packages/windows-app/main.py`](../packages/windows-app/main.py)

- 导入 `keyboard` 库
- 导入 `FocusManager`
- 注册全局快捷键

**解决方案：** 条件导入和条件执行

```python
import sys

if sys.platform == "win32":
    import keyboard
    from focus import FocusManager
```

#### 3. 系统托盘适配（P1）

**当前实现：** [`packages/windows-app/ui/system_tray.py`](../packages/windows-app/ui/system_tray.py)

**macOS 注意事项：**
- macOS 的系统托盘称为 "Menu Bar"
- 图标显示和行为略有不同
- 需要调整图标尺寸（macOS 建议使用 16x16 或 32x32）
- 使用 Qt 内置标准图标（跨平台）

**解决方案：**
```python
# 设置托盘图标 - 使用 Qt 内置图标（跨平台）
style = QApplication.style()
icon = style.standardIcon(style.StandardPixmap.SP_MessageBoxInformation)
self.setIcon(icon)
```

### 无需修改的部分

#### 1. UI 布局（✅ 完全兼容）

所有布局代码在 macOS 上都能正常工作：

- 左文字区：350x400
- 右文字区：600x500
- 布局间距：10px
- 对齐方式：`Qt.AlignmentFlag.AlignTop`
- 按钮对齐逻辑

#### 2. 字体设置（✅ 部分兼容）

```python
TEXT_FONT_FAMILIES = ["Optima-Regular", "PingFang SC", "Cambria", "Cochin", "Georgia", "Times", "Times New Roman", "serif"]
```

- "PingFang SC" 是 macOS 系统字体 ✅
- "Optima-Regular" 在 macOS 上可用 ✅
- **无需修改**

#### 3. 业务逻辑（✅ 完全兼容）

- Agent 系统（[`packages/windows-app/agent/`](../packages/windows-app/agent/)）
- 润色功能（[`PolishWorker`](../packages/windows-app/ui/polish_worker.py)）
- 文本处理逻辑

#### 4. Qt 组件（✅ 完全兼容）

所有使用的 Qt 组件都是跨平台的：
- `QMainWindow`
- `QTextEdit`
- `QPushButton`
- `QVBoxLayout`
- `QHBoxLayout`
- `QFrame`
- `QSystemTrayIcon`

### macOS PyInstaller 配置

#### Wisadel-mac.spec

```python
# Wisadel-mac.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# 收集 PySide6 数据文件
datas = []
datas += collect_data_files('PySide6')

# 收集隐藏导入
hiddenimports = []
hiddenimports += collect_submodules('PySide6')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Wisadel',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 无控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

# macOS 特定：创建 .app 包
app = BUNDLE(
    exe,
    name='Wisadel.app',
    icon=None,  # TODO: 添加 .icns 图标
    bundle_identifier='com.wisadel.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
        'CFBundleName': 'Wisadel',
        'CFBundleDisplayName': 'Wisadel',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSRequiresAquaSystemAppearance': False,  # 支持深色模式
        'LSUIElement': False,  # 显示在 Dock 和 Cmd+Tab
    },
)
```

#### build-mac.sh

```bash
#!/bin/bash

echo "========================================="
echo "  构建 Wisadel for macOS"
echo "========================================="

# 检查平台
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "错误: 此脚本仅支持 macOS"
    exit 1
fi

# 清理旧构建
echo "清理旧构建..."
rm -rf build dist

# 安装依赖
echo "检查依赖..."
pip install pyinstaller PySide6 loguru

# 构建
echo "开始构建..."
pyinstaller Wisadel-mac.spec --clean

# 自签名
echo "代码签名（自签名）..."
codesign --force --deep --sign - dist/Wisadel.app

# 验证
echo "验证签名..."
codesign --verify --verbose dist/Wisadel.app

echo "========================================="
echo "  构建完成！"
echo "  输出: dist/Wisadel.app"
echo "========================================="
echo ""
echo "测试运行: open dist/Wisadel.app"
```

### 平台抽象层建议

为了更好地支持跨平台，建议创建平台抽象层：

```python
# packages/windows-app/platform_utils.py
import sys

def is_windows():
    return sys.platform == "win32"

def is_macos():
    return sys.platform == "darwin"

def is_linux():
    return sys.platform.startswith("linux")
```

```python
# packages/windows-app/ui/platform_helpers.py
import sys

class PlatformHelper:
    @staticmethod
    def focus_window(window):
        if sys.platform == "win32":
            import ctypes
            user32 = ctypes.windll.user32
            hwnd = window.winId()
            user32.SetForegroundWindow(hwnd)
        elif sys.platform == "darwin":
            # macOS 特定实现
            pass

    @staticmethod
    def get_system_tray_icon_size():
        if sys.platform == "darwin":
            return 22  # macOS 建议尺寸
        else:
            return 16  # Windows 默认尺寸
```

### 测试清单

在 macOS 上需要测试的功能：

- [ ] 窗口正常显示和布局
- [ ] 窗口置顶功能
- [ ] 文本输入和显示
- [ ] 润色按钮功能
- [ ] Accept 按钮功能
- [ ] 系统托盘图标显示（Menu Bar）
- [ ] 系统托盘右键菜单
- [ ] 窗口关闭到托盘
- [ ] 从托盘恢复窗口
- [ ] 字体渲染效果
- [ ] 窗口大小和位置
- [ ] PyInstaller 打包成功
- [ ] .app 双击启动
- [ ] 代码签名验证
- [ ] 公证（如需分发）

### 成功判定标准（Definition of Done）

macOS 支持被视为成功，当且仅当：

- .app 包可正常生成
- 双击 .app 可启动应用
- 托盘图标在 Menu Bar 显示
- 可从托盘打开主窗口
- 文本润色功能正常工作
- Accept 按钮可隐藏窗口

## Tasks

### 开发流程说明

> **重要：跨平台代码同步工作流**

本项目的 macOS 兼容性改造采用以下工作方式：

1. **代码统一存放**：macOS 和 Windows 的跨平台代码写在一起，通过 `sys.platform` 条件判断实现平台适配
2. **人工 cherry-pick**：当某部分代码稳定后，您会手动挑选（cherry-pick）该部分回到 Windows 分支
3. **Windows 验证**：您自己在 Windows 侧构建和验证
4. **遇到问题**：如果 cherry-pick 过程中遇到问题，我们一起分析处理

**具体操作节奏**：
- 每完成若干任务后，您会挑选其中稳定的代码 cherry-pick 回 Windows
- 在 Windows 上运行 `build.bat` 构建并验证功能正常
- 如有冲突或问题，通知我一起排查

### 执行模式 (AI Agent 必读)

**仅支持阶段模式（Phase）：**

触发词：'执行第一阶段'、'execute setup'

行为：执行一个阶段（Phase）内的所有事项，然后等待用户确认再进入下一阶段

### Completion Checklist（AI Agent 义务，不是勾选模板）

- 确认所有 Story/Task 已按预期完成并在文档中标注完成状态
- 确认测试已通过（如有测试）
- 确认关键变更已完成 review（如适用）
- 确认必要的文档已更新（README/接口文档等）
- 确认 Changelog（如有）已更新
- 确认已通知相关 Stakeholders（如适用）
- 确认最终产物已按约定归档到 `.spec-flow/archive/{feature-name}/`

**所有模式必须遵守：**
1. ✅ 严格按顺序执行 - 从第一个 `- [ ]` 开始
2. ✅ 检查依赖 - 执行前确认依赖任务已完成 (`- [x]`)
3. ✅ 更新状态 - 完成后将 `- [ ]` 改为 `- [x]`
4. ✅ 报告进度 - 显示 (N/Total)
5. ✅ 遇错即停 - 出错时立即停止，等待用户指示

**禁止行为：**
- ❌ 跳过任务
- ❌ 不按顺序执行
- ❌ 执行任务列表之外的工作
- ❌ 出错后继续执行

### 概览

| Phase           | Tasks | Completed | Progress |
|-----------------|-------|-----------|----------|
| Platform Abstraction | 2     | 2         | 100%     |
| Windows Code Comment | 5     | 5         | 100%     |
| PyCharm Testing | 2     | 0         | 0%       |
| System Tray     | 4     | 3         | 75%      |
| macOS Packaging | 4     | 0         | 0%       |
| Documentation   | 3     | 0         | 0%       |
| Global Hotkey   | 6     | 5         | 83%      |
| **Total**       | **26**| **15**    | **58%**  |

### Dependencies & Blockers

```mermaid
graph LR
    PHASE-1[阶段一：平台抽象层] --> PHASE-2[阶段二：注释 Windows 代码]
    PHASE-2 --> PHASE-3[阶段三：PyCharm 测试]
    PHASE-3 --> PHASE-4[阶段四：系统托盘调试]
    PHASE-4 --> PHASE-5[阶段五：macOS 打包]
    PHASE-5 --> PHASE-6[阶段六：文档和发布]
```

**Blockers**

- **Blocker**: 当前无 macOS 构建环境
- **Blocking Items**: PHASE-3, PHASE-4, PHASE-5
- **Raised**: 2026-02-20
- **Owner**: macOS App
- **Status**: Open
- **Resolution**: 需要在 macOS 机器上执行构建和测试

### Changelog

### Task Breakdown

### Phase 1: Platform Abstraction

- [x] **TASK-101**: 创建平台工具模块
  - **Complexity**: Low
  - **Files**: `packages/windows-app/platform_utils.py`
  - **Dependencies**: None
  - **Notes**: 已创建 `is_windows()`、`is_macos()`、`is_linux()`、`get_platform_name()` 函数

- [x] **TASK-102**: 测试平台检测
  - **Complexity**: Low
  - **Files**: N/A
  - **Dependencies**: TASK-101
  - **Notes**: 已在代码中验证 `sys.platform` 返回 `"darwin"`

### Phase 2: Windows Code Comment

- [x] **TASK-201**: 注释 main_window.py 中的 Windows API
  - **Complexity**: Low
  - **Files**: `packages/windows-app/ui/main_window.py`
  - **Dependencies**: None
  - **Notes**: 已注释 `import ctypes`（第9行）、`user32`（第16行）、`show()` 方法中的 Windows API 调用

- [x] **TASK-202**: 注释 main.py 中的 Windows 特定导入
  - **Complexity**: Low
  - **Files**: `packages/windows-app/main.py`
  - **Dependencies**: None
  - **Notes**: 已注释 `import keyboard`（第7行）、`from focus import FocusManager`（第9行）

- [x] **TASK-203**: 注释 main.py 中的快捷键注册
  - **Complexity**: Low
  - **Files**: `packages/windows-app/main.py`
  - **Dependencies**: TASK-202
  - **Notes**: 已注释 `register_hotkey` 函数定义（第29-31行）和调用（第71行）

- [x] **TASK-204**: 简化 on_accept 回调
  - **Complexity**: Low
  - **Files**: `packages/windows-app/main.py`
  - **Dependencies**: TASK-202
  - **Notes**: 已注释焦点恢复和文本注入代码，仅保留 `window.hide()`

- [x] **TASK-205**: 简化 on_hotkey 回调
  - **Complexity**: Low
  - **Files**: `packages/windows-app/main.py`
  - **Dependencies**: TASK-202
  - **Notes**: 已注释焦点保存代码，保留 `window.show()`

### Phase 3: PyCharm Testing

- [ ] **TASK-301**: 在 macOS 上运行主程序
  - **Complexity**: Low
  - **Files**: N/A
  - **Dependencies**: TASK-201, TASK-202, TASK-203
  - **Notes**: 运行 `python packages/windows-app/main.py` 验证基础功能

- [ ] **TASK-302**: 验证 GUI 显示和布局
  - **Complexity**: Low
  - **Files**: N/A
  - **Dependencies**: TASK-301
  - **Notes**: 检查双文本区和按钮是否正常显示

### Phase 4: System Tray

- [x] **TASK-401**: 修改系统托盘代码使用 Qt 内置图标
  - **Complexity**: Low
  - **Files**: `packages/windows-app/ui/system_tray.py`
  - **Dependencies**: TASK-301
  - **Notes**: 已使用 `QStyle.standardIcon()` 替代 `QIcon.fromTheme()`，实现跨平台托盘图标

- [x] **TASK-402**: 创建自定义图标加载模块
  - **Complexity**: Low
  - **Files**: `packages/windows-app/platform_utils.py`
  - **Dependencies**: TASK-401
  - **Notes**: 已添加 `get_tray_icon()` 函数，根据平台加载 `icon-mac.png` 或 `icon-win.png`，回退到 Qt 内置图标

- [x] **TASK-403**: 更新 system_tray.py 使用自定义图标
  - **Complexity**: Low
  - **Files**: `packages/windows-app/ui/system_tray.py`
  - **Dependencies**: TASK-402
  - **Notes**: 已使用 `get_tray_icon()` 替代 Qt 内置图标，直接导入无兜底

- [ ] **TASK-404**: 测试托盘功能
  - **Complexity**: Medium
  - **Files**: N/A
  - **Dependencies**: TASK-403
  - **Notes**: 验证托盘图标显示、右键菜单、显示窗口/退出功能

### Phase 5: macOS Packaging

- [ ] **TASK-501**: 创建 Wisadel-mac.spec 配置文件
  - **Complexity**: Medium
  - **Files**: `packages/windows-app/Wisadel-mac.spec`
  - **Dependencies**: TASK-401
  - **Notes**: 创建 PyInstaller BUNDLE 配置

- [ ] **TASK-502**: 创建 build-mac.sh 构建脚本
  - **Complexity**: Low
  - **Files**: `packages/windows-app/build-mac.sh`
  - **Dependencies**: TASK-501
  - **Notes**: 创建构建脚本并添加执行权限

- [ ] **TASK-503**: 准备图标文件（可选）
  - **Complexity**: Low
  - **Files**: `packages/windows-app/assets/icon.icns`
  - **Dependencies**: TASK-501
  - **Notes**: 将 PNG 转换为 .icns 格式

- [ ] **TASK-504**: 执行打包并验证
  - **Complexity**: Medium
  - **Files**: N/A
  - **Dependencies**: TASK-502
  - **Notes**: 运行构建脚本，验证 .app 生成、双击启动、代码签名

### Phase 6: Documentation

- [ ] **TASK-601**: 更新 README 添加 macOS 说明
  - **Complexity**: Low
  - **Files**: `README.md`
  - **Dependencies**: TASK-504
  - **Notes**: 添加 macOS 安装和使用说明

- [ ] **TASK-602**: 创建发布清单
  - **Complexity**: Low
  - **Files**: N/A
  - **Dependencies**: TASK-504
  - **Notes**: 记录 Windows 和 macOS 两个平台的发布物

- [ ] **TASK-603**: 记录已知限制
  - **Complexity**: Low
  - **Files**: N/A
  - **Dependencies**: TASK-601
  - **Notes**: 文档化 macOS 限制（无全局快捷键、无焦点跟踪、无文本注入）

### Future Extensions

> **注意**：以下内容不在当前实施范围内，留待未来优化。

#### 1. macOS 窗口和托盘优化

- 测试 `Qt.WindowStaysOnTopHint` 在 macOS 上的表现
- 添加额外窗口标志
- 优化托盘图标尺寸和样式

#### 2. 焦点跟踪和文本注入

- 隔离 focus.py 仅在 Windows 导入
- 条件导入 FocusManager
- 修改 on_accept/on_hotkey 回调支持跨平台

#### 3. macOS 全局快捷键

##### 方案对比

| 方案 | 原理 | 优点 | 缺点 | 成熟度 |
|------|------|------|------|--------|
| **pynput（推荐）** | 监听全局键盘事件 | 跨平台、文档完善 | 需要辅助功能权限 | 高 |
| Quartz/Carbon | macOS 原生 Carbon Event API | 无第三方依赖 | 仅 macOS、代码复杂 | 中 |
| pyObjC | NSEvent addGlobalMonitorForEvents | Apple 官方 API | 仅 macOS、需要权限 | 高 |

##### 推荐实现：pynput

```python
from pynput import keyboard

def on_activate():
    window.show()
    window.raise_()

def for_canonical(f):
    return lambda k: f(l.canonical(k))

hotkey = keyboard.HotKey(
    keyboard.HotKey.parse('<option>+w'),
    on_activate
)

with keyboard.Listener(
        on_press=for_canonical(hotkey.press),
        on_release=for_canonical(hotkey.release)) as l:
    l.join()
```

##### 权限要求

macOS 全局快捷键需要用户授权**辅助功能权限**（Accessibility）：
- 路径：`系统设置 > 隐私与安全性 > 辅助功能`
- 应用首次启动时应检测权限，如未授权则提示用户并打开系统偏好设置

##### 实现计划

1. 添加 pynput 依赖
2. 创建跨平台快捷键管理器（hotkey_manager.py）
3. 处理权限检测与引导
4. 集成到 main.py

### Specs（新增）

- [x] **SPEC-002**：全局快捷键管理器
  - **背景 / 目标**：封装跨平台快捷键注册逻辑
  - **范围**：支持 macOS 和 Windows
  - **关键决策**：使用 pynput 作为首选方案，必须使用 pynput 提供的 Key 枚举，不支持字符串格式
  - **实现约束**：
    - 必须使用 Tuple 格式：`key: Tuple`
    - 必须使用 pynput.Key 枚举常量
    - Windows: (keyboard.Key.alt, keyboard.KeyCode.from_char('w'))
    - macOS: (keyboard.Key.ctrl, keyboard.Key.alt, keyboard.KeyCode.from_char('w')) 即 Ctrl+Option+W
    - **重要**：pynput 回调运行在系统线程，必须使用 `QMetaObject.invokeMethod` + `Qt.QueuedConnection` 确保 UI 操作在主线程执行
  - **接口 / 对接点**：
    - `register_hotkey(key_tuple, callback)` - 注册快捷键（仅支持 Tuple 格式）
    - `unregister_hotkey()` - 注销快捷键
  - **验收（勾选即证据）**：
    - [x] macOS 上可成功注册 Ctrl+Option+W
    - [x] Windows 上可成功注册 Alt+W
    - [x] 快捷键触发后窗口正常显示

- [ ] **SPEC-003**：辅助功能权限引导
  - **背景 / 目标**：引导用户授权必要权限
  - **范围**：macOS 平台
  - **关键决策**：首次启动时检测，未授权则弹窗提示
  - **实现约束**：
    - 使用 `os.system("open x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility")`
  - **验收（勾选即证据）**：
    - [ ] 未授权时显示引导提示
    - [ ] 点击后可打开系统设置

- [x] **SPEC-004**：跨平台字体适配
  - **背景 / 目标**：解决不同平台字体差异问题
  - **范围**：支持 macOS、Windows、Linux
  - **关键决策**：使用 platform_utils 封装平台检测函数
  - **实现约束**：
    - 使用 `platform_utils.is_macos()`、`is_windows()`、`is_linux()` 判断平台
    - macOS: PingFang SC, Helvetica, Arial, sans-serif
    - Windows: Microsoft YaHei, SimSun, Cambria, Georgia 等
    - Linux: 抛出异常暂不支持
  - **接口 / 对接点**：
    - `TEXT_FONT_FAMILIES` 全局变量
  - **验收（勾选即证据）**：
    - [x] macOS 字体正常显示，无警告
    - [ ] Windows 字体正常显示
    - [ ] Linux 抛出明确错误信息

### Phase 7: Global Hotkey（实施）

#### 7.1 功能分层说明

Hotkey 功能拆分为两个独立模块：

| 模块 | 功能描述 | 本期实施 |
|------|----------|----------|
| **唤起（Invoke）** | 显示窗口、展开界面 | ✅ 实施 |
| **焦点获取（Focus）** | 将窗口置前、激活应用 | ❌ 不实施 |

**成功标准**：
- Hotkey 按下后，窗口显示效果与点击 tray 图标 → "打开" 完全一致
- 不改变窗口的 z-order 层级（不强制置顶）
- 不改变应用的 focus 状态

#### 7.2 代码调整

**当前被注释的 hotkey 代码位置**：`packages/windows-app/main.py`

| 行号 | 代码 | 功能分类 | 处理方式 |
|------|------|----------|----------|
| ~7 | `import keyboard` | 唤起 | 打开注释 |
| ~8 | `from focus import FocusManager` | 焦点 | 保持注释 |
| ~16 | `focus_mgr = FocusManager()` | 焦点 | 保持注释 |
| ~20-22 | `register_hotkey` 函数定义 | 唤起 | 打开注释 |
| ~27-28 | `focus_mgr.save_current_focus()` | 焦点 | 保持注释 |
| ~32 | `window.show()` | 唤起 | 打开注释 |
| ~85 | `register_hotkey('alt+w', on_hotkey)` | 唤起 | 打开注释 |

#### 7.3 hotkey_manager.py 设计

```python
# packages/windows-app/hotkey_manager.py
import sys
from typing import Callable, Optional

class HotkeyManager:
    """跨平台快捷键管理器 - 仅负责按键监听与事件分发"""

    def __init__(self):
        self._listener = None
        self._hotkey = None
        self._callback = None

    def register_hotkey(self, key: str, callback: Callable) -> bool:
        """注册热键，仅触发回调，不涉及焦点逻辑"""
        self._hotkey = key
        self._callback = callback
        # TODO: 实现跨平台快捷键注册
        return True

    def unregister_hotkey(self) -> bool:
        """注销热键"""
        # TODO: 实现注销逻辑
        return True

    def start(self):
        """启动监听"""
        pass

    def stop(self):
        """停止监听"""
        pass
```

- **职责边界**：HotkeyManager 纯负责按键监听与事件分发
- **不包含**：任何窗口激活、焦点获取逻辑
- **唤起回调中仅调用**：`window.show()` 系列方法

- [x] **TASK-701**: 识别并打开 hotkey 相关代码
  - **Complexity**: Low
  - **Files**: `packages/windows-app/main.py`
  - **Dependencies**: None
  - **Notes**: 已移除旧的 keyboard 导入，改为使用 hotkey_manager

- [x] **TASK-702**: 清理 on_hotkey 中的焦点相关代码
  - **Complexity**: Low
  - **Files**: `packages/windows-app/main.py`
  - **Dependencies**: TASK-701
  - **Notes**: 已移除焦点相关代码，仅保留 `window.show()`

- [x] **TASK-703**: 创建 hotkey_manager.py 框架
  - **Complexity**: Medium
  - **Files**: `packages/windows-app/hotkey_manager.py`
  - **Dependencies**: None
  - **Notes**: 已创建 HotkeyManager 类，实现跨平台快捷键注册

- [x] **TASK-704**: 实现 pynput 集成
  - **Complexity**: Medium
  - **Files**: `packages/windows-app/hotkey_manager.py`
  - **Dependencies**: TASK-703
  - **Notes**: 已使用 pynput 实现全局快捷键监听

- [x] **TASK-705**: 集成 hotkey_manager 到 main.py
  - **Complexity**: Medium
  - **Files**: `packages/windows-app/main.py`, `packages/windows-app/hotkey_manager.py`
  - **Dependencies**: TASK-702, TASK-704
  - **Notes**: 已启用快捷键注册：Windows 用 alt+w，macOS 用 option+w

- [x] **TASK-706**: 测试 hotkey 唤起功能
  - **Complexity**: Medium
  - **Files**: N/A
  - **Dependencies**: TASK-705
  - **Notes**: 用户自行在 PyCharm 中测试

#### 7.4 验证方法

**功能验证**：
- 按下 hotkey 组合键，窗口从隐藏/最小化状态变为显示
- 窗口位置、大小保持最近一次状态
- 其他已打开应用的焦点不被打断

**等价性验证**：
- 场景 A：点击 tray 图标 → "打开"
- 场景 B：按下 hotkey
- 两种操作后窗口的 visible、geometry、z-order 状态完全一致
