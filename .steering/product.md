# Product Vision

> updated_by: VSCode - Claude-Opus-4.6
> updated_at: 2026-02-21 14:40:00

## Mission

Wisadel 致力于打造一款桌面级文本润色验证工具，通过 AI 增强技术帮助用户优化写作，并通过自动化验证机制确保输出质量。

## Vision

成为桌面端首选的 AI 文本润色工具，通过深度集成的验证机制确保输出质量，为写作者提供高效、可靠的文本优化体验。

## Target Users

### Primary Persona

**Name**: 文字工作者

- **Role**: 需要频繁撰写和修改文本的专业人士（编辑、作者、运营、秘书等）
- **Goals**: 快速润色文本，提升文字质量和工作效率
- **Pain Points**:
  - 在线润色工具需要复制粘贴，流程繁琐
  - 担心敏感内容泄露到第三方服务
  - 缺乏对润色结果的质量验证
- **Tech Savviness**: Medium

### Secondary Personas

- **开发者**: 需要撰写技术文档和代码注释
- **学生**: 撰写论文、作业和申请材料
- **商务人士**: 撰写邮件、报告和提案

## Problem Statement

当前桌面用户缺乏一款本地化部署的 AI 润色工具，需要反复切换应用进行复制粘贴操作，且无法保证润色结果的质量和一致性。

## Value Proposition

For 桌面用户 who 需要高效润色文本，Wisadel is a 桌面端 AI 润色工具 that 提供一键润色和自动化质量验证。Unlike 在线润色服务，我们提供本地化部署保障隐私安全，并内置验证机制确保输出质量。

## Key Metrics

### North Star Metric

**Metric**: 活跃用户数
**Current**: 待统计
**Target**: 月活用户 > 1000
**Why**: 用户规模是产品成功的核心指标

### Supporting Metrics

| Metric | Current | Target | Owner |
|--------|---------|--------|-------|
| 日活跃用户 | 待统计 | > 100 | 产品 |
| 平均润色次数/天 | 待统计 | > 3次 | 产品 |
| 用户留存率(7日) | 待统计 | > 40% | 产品 |
| 验证通过率 | 待统计 | > 85% | 工程 |

## Product Principles

When making trade-offs, prioritize in this order:

1. **隐私优先**: 所有数据处理均在本地完成，不上传用户文本到第三方服务
2. **质量保障**: 内置验证机制确保润色结果符合基本质量标准
3. **效率至上**: 通过全局快捷键实现一键唤起和快速上屏，最大化工作效率

## Roadmap Themes

### Current Quarter

- **核心功能完善**: 优化润色算法，提升润色质量和速度
- **跨平台支持**: 完成 Linux 平台支持
- **用户体验优化**: 改进 UI 交互，增加更多快捷键支持

### Next Quarter

- **插件系统**: 支持自定义润色规则和验证器
- **多语言支持**: 扩展对英文、日文等语言的支持
- **云端同步**: 可选的用户配置云同步功能

### Future (Not Committed)

- **团队协作**: 团队共享配置和规范
- **API 开放**: 提供 REST API 供其他应用集成

## Constraints

- 依赖 LLM API 服务（当前支持 MiniMax）
- 需要用户自行配置 API Key
- 桌面端应用，需要安装客户端

## Competitive Landscape

| Competitor | Strengths | Weaknesses | Our Advantage |
|------------|-----------|------------|---------------|
| Grammarly | 功能强大、生态成熟 | 需联网、数据隐私顾虑 | 本地部署、验证机制 |
| CopyAI | 操作简单 | 付费墙、隐私问题 | 快捷键集成、验证机制 |
| 本地脚本 | 完全隐私 | 功能有限、体验差 | 完整 GUI、验证机制 |

## Success Criteria

- 用户可通过全局快捷键快速唤起润色工具
- 润色结果经过自动化验证，确保基本质量
- 用户数据全程保存在本地，无隐私风险
- 支持 Windows 和 macOS 双平台

## Changelog

<!-- // 这是一个 Living Document，如无必要，无需维护变更历史。 -->
