# 软件概要设计文档 Skill

**[English](README.md) | 简体中文**

一个通用的软件概要设计 AI Skill，用于生成和审查软件概要设计（HLD，High-Level Design，高层设计）文档。支持需求分析、代码分析、软件架构设计、模块设计、接口设计、设计审查、架构图和设计文档生成，适用于不同语言、平台和软件项目。

这个 Skill 既可以在**完全没有代码、甚至还没有创建代码工程目录**时，仅根据需求从 0 开始进行架构和概要设计；也可以对已有代码工程进行架构逆向；还可以结合需求和代码检查实现偏差与架构漂移。

本 Skill 的职责范围明确限定为：**软件概要设计文档的分析、设计、审查与输出**。它不会继续生成项目工程骨架、目录结构、源码骨架、详细设计文档或业务实现代码。

它特别适合内网或离线环境。核心能力依赖 Skill 本身的规则，不要求访问互联网。CodeGraph、PlantUML、DOCX 工具、Pandoc 等都属于可选增强能力。

## 工作模式

- **需求驱动 / Greenfield（绿地项目）**：只有需求，没有代码，甚至没有项目工程目录。直接根据需求从 0 生成概要设计。
- **代码驱动 / Brownfield（棕地项目）**：已有代码，但概要设计缺失或过时。根据现有实现反向恢复软件架构。
- **Hybrid（混合模式）**：同时存在需求和代码，结合两者生成设计，并检查需求遗漏、实现偏差和架构漂移。
- **Review-only（仅审查）**：只审查已有的软件架构或概要设计，不强制重新生成整份文档。

## 范围边界

这个 Skill 的最终交付物是**软件概要设计文档**或**概要设计审查结果**。为了生成高质量概要设计，它可以分析或提出架构、模块、接口、数据、异常处理、日志、安全、可测试性、可维护性、风险和必要的设计图，但到概要设计文档完成为止，不继续进入工程创建、详细设计或编码阶段。

## 核心能力

- 只有需求文档或自然语言需求时，也可以从 0 开始设计
- 不要求预先创建代码工程、目录结构或项目骨架
- 根据需求和代码生成项目相关的概要设计，而不是输出通用套话
- 区分需求事实、代码事实、已有文档事实、设计方案、假设和待确认项，降低 AI 编造风险
- 支持总体架构、模块、数据、接口、异常、日志、安全、可测试性、可维护性和风险分析
- 支持后端、Web、桌面软件、Embedded Linux（嵌入式 Linux）、RTOS（Real-Time Operating System，实时操作系统）、MCU（Microcontroller Unit，微控制器）等不同项目类型
- 按需生成软件架构图、模块关系图、时序图、数据流图等
- 内置标准化 Word / DOCX 模板；没有公司模板时自动使用
- 如果用户提供公司或项目 Word 模板，则优先保留并使用其格式
- 支持中文和英文文档

## 从 0 开始设计

对于新项目，不需要先建立代码工程。最简单的输入可以只有：

```text
requirements.docx
```

或者甚至只是：

```text
开发一个设备管理系统，支持设备注册、状态上报、远程控制和日志查询。
```

Skill 会按下面的流程进行设计：

```text
需求
  ↓
系统范围与边界
  ↓
功能和约束分析
  ↓
总体架构方案
  ↓
模块划分与职责
  ↓
模块依赖与接口
  ↓
核心数据设计
  ↓
异常 / 日志 / 安全 / 可测试性分析
  ↓
风险、假设和待确认项
  ↓
软件概要设计文档
```

在这个模式下，Skill 不会把“设计建议”伪装成已经存在的实现。例如需求没有规定 PostgreSQL、MQTT 或具体线程模型时，这些只能作为设计方案或待确认项出现，而不能写成已经实现的事实。

## Claude Code 安装

### 安装为个人 Skill

```bash
git clone https://github.com/smallfishworld/software-design-doc-skill.git
mkdir -p ~/.claude/skills/software-design-doc
cp -r software-design-doc-skill/* ~/.claude/skills/software-design-doc/
```

然后启动 Claude Code，可直接调用：

```text
/software-design-doc
```

当用户需求与这个 Skill 的描述匹配时，Claude Code 也可以自动发现并使用它。

### 安装为项目级 Skill

```bash
mkdir -p .claude/skills/software-design-doc
cp -r /path/to/software-design-doc-skill/* .claude/skills/software-design-doc/
```

如果某个项目需要自己的设计规则、Word 模板或公司规范，建议使用项目级安装。

> 注意：对于一个全新项目，“安装 Skill”并不意味着必须先创建目标软件工程。你可以在任意工作目录中调用 Skill，并指定外部需求文档，让它直接从 0 完成概要设计。

## 使用示例

### 示例 1：完全没有代码和工程目录

```text
/software-design-doc
这是一个全新的项目，目前没有任何源代码，也没有项目工程骨架。
请读取 requirements.docx，根据需求从 0 生成中文软件概要设计。
所有架构、模块和接口方案都视为设计决策，并明确列出假设和待确认项。
```

### 示例 2：已有代码工程

```text
/software-design-doc
分析当前代码工程，根据现有实现生成软件概要设计文档。
```

### 示例 3：需求 + 代码

```text
/software-design-doc
同时分析需求文档和当前代码，生成中文软件概要设计，
并检查需求未实现、代码无需求来源和架构漂移问题。
如果存在 docs/company-template.docx，则使用公司模板。
```

### 示例 4：没有公司 Word 模板

```text
/software-design-doc
生成最终 Word 版软件概要设计说明书。
当前项目没有指定公司模板，请使用 Skill 内置的标准 DOCX 模板。
```

### 示例 5：只做架构审查

```text
/software-design-doc
只审查当前软件架构，指出模块耦合、依赖方向、循环依赖和职责划分问题，
暂时不要生成完整概要设计文档。
```

更多示例见 `examples/example-request.md`。

## 默认 Word 模板

仓库内置：

```text
templates/default-software-design-template.docx
```

当用户要求生成 Word / DOCX 文档，但没有指定公司或项目模板时，Skill 自动使用这个模板。

模板优先级：

1. 用户本次任务明确指定的公司 / 用户 Word 模板
2. 项目自身的概要设计 DOCX 模板
3. Skill 内置 `templates/default-software-design-template.docx`
4. 无法生成 DOCX 或用户要求 Markdown 时，使用 `templates/default-outline.md`

内置 Word 模板采用标准 A4 企业文档风格，包含封面、文档信息、修订记录、目录字段、标题样式、页眉页脚、页码以及架构/模块/数据/接口/异常/风险等常用表格结构。

详细规则见 `references/docx-template.md`。

## 默认概要设计目录

在没有公司模板，也没有显式指定目录时，默认使用精简的通用结构：

1. 引言
2. 系统概述
3. 设计目标与原则
4. 软件总体架构
5. 模块概要设计
6. 数据设计
7. 接口设计
8. 异常与故障处理
9. 日志与可观测性
10. 安全设计（项目相关时）
11. 可测试性设计
12. 可维护性与扩展性
13. 风险、约束与待确认项

线程 / 多任务、状态机、性能 / 实时性、编译部署等内容在确实影响架构时仍会分析，但默认**不单独拉成章节**，而是融合到总体架构、模块设计、数据设计、接口设计或风险章节中。

## 可选工具集成

Skill 本身不依赖任何 MCP（Model Context Protocol，模型上下文协议）服务器。环境允许时，可以使用以下工具增强能力：

- CodeGraph 或类似代码智能工具：分析调用关系、依赖关系和架构边界
- PlantUML：生成 UML（Unified Modeling Language，统一建模语言）和软件架构图
- DOCX MCP、`python-docx`、Microsoft Word 自动化等：直接生成或编辑 Word 文档
- Pandoc：在需要 Markdown-first 工作流时将 Markdown 转换为 DOCX

详细降级和工具选择规则见 `references/tool-integration.md`。

## 内网 / 离线环境检查

可以运行：

```bash
python3 scripts/check_environment.py
```

这个脚本只检查可选的本地增强工具。核心的需求驱动概要设计流程不依赖 CodeGraph、PlantUML、Pandoc 或互联网连接。默认 Word 模板已经包含在仓库中。

## 仓库结构

```text
software-design-doc-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── templates/
│   ├── default-outline.md
│   └── default-software-design-template.docx
├── references/
│   ├── architecture-analysis.md
│   ├── document-rules.md
│   ├── platform-profiles.md
│   ├── diagram-guide.md
│   ├── tool-integration.md
│   └── docx-template.md
├── examples/
│   └── example-request.md
├── scripts/
│   ├── check_environment.py
│   └── build_default_template.py
└── tests/
    └── test_skill.py
```

## 设计原则

概要设计文档应该描述“已经确认的事实”和“明确提出的设计”，而不是把模型猜测包装成事实。

分析过程中会区分：

- `[REQ]`：来自需求的已确认事实
- `[CODE]`：来自代码、配置或构建文件的已确认事实
- `[DOC]`：来自已有项目文档的事实
- `[DESIGN]`：概要设计阶段提出的方案
- `[ASSUMPTION]`：为了继续设计而引入、但仍需确认的假设
- `[TODO]`：尚未解决或需要人工决策的问题

对于 Greenfield 新项目，需求是事实基线，而软件架构和模块方案都应被明确视为“拟设计方案”，直到代码真正实现。

Skill 默认强调：高内聚、低耦合、依赖关系清晰、模块职责明确、接口简单稳定，并尽量让文档反映真实项目，而不是套用教科书模板。

## 评审与交付行为

- 先区分需求驱动、代码驱动或混合输入，再选择生成、增量更新或仅评审。
- 仅评审输出按影响排序的问题，包含位置、证据、影响、修正建议及覆盖范围；不强制生成 Word。
- 工具检查按交付物选择范围，脚本路径相对于 Skill 安装位置，不依赖当前项目目录。
- UML / 软件架构优先 PlantUML；流程图、树形图、功能分解和通用关系图优先 Mermaid。规则统一维护在 [绘图指南](references/diagram-guide.md)。
- `.puml` / `.mmd` 是权威可编辑源；统一优先生成 SVG，Markdown 使用相对路径引用 SVG，DOCX 在验证兼容后插入 SVG，否则使用高分辨率 PNG。Word 中的 SVG 只提供矢量缩放和有限图形编辑，不等于可以编辑 PlantUML/Mermaid 语义。
- 版本检查成功不代表实际渲染成功。Linux 无法渲染 Mermaid 时保留 `.mmd` 和 Windows 命令；缺少图的 Word 标为待补图草稿。
- Word 模板可从脚本重建，交付前应检查文件完整性和实际页面排版。

可按范围检查环境（脚本需要 Python 3.9+，只使用标准库）：

```bash
python3 scripts/check_environment.py --scope diagrams --plantuml-jar "/path/to/plantuml.jar"
python3 scripts/check_environment.py --scope docx --scope diagrams --json
python3 -m unittest discover -s tests -v
```

测试只依赖标准库；模板重建另需 `python-docx`。测试覆盖命令缺失、失败、超时、JAR 路径、DOCX 完整性、目录字段和本地引用。模板重建后还需实际渲染并检查页面。

## 当前状态

欢迎使用真实项目验证，尤其欢迎以下场景的反馈：

- 只有需求、没有代码的从 0 概要设计
- 公司软件概要设计 Word 模板适配
- Embedded Linux / RTOS / MCU 项目
- 后端、Web、桌面软件
- 现有代码架构逆向
- Word / DOCX 自动生成流程
