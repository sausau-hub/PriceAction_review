# PA Agent — Al Brooks & Rose 价格行为分析系统

> 用 Claude Code 自动分析 Al Brooks & Rose 视频，持续迭代你自己的交易知识库，每天收盘后做 Al Brooks 风格复盘。

**理念：市场奖池无限，知识共享不竞争。代码是大家的，知识库是你自己的。**

---

## 这是什么

一套基于 Claude Code 的三 Agent 工作流，专为 Al Brooks 价格行为学习者设计：

```
.srt 字幕文件
      ↓
 Agent 1：分析视频          ← 提炼每期 Rose/Al 视频的交易规则
      ↓
 Agent 2：迭代知识库        ← 跨视频积累规则，自动打置信度评级
      ↓
 Agent 3：复盘实盘          ← 每天收盘后，用你的知识库做逐棒分析
```

每个人积累自己的知识库。三个 Agent 全部开源，社区一起迭代。

---

## 你需要什么

| 工具 | 说明 |
|------|------|
| [Claude Code](https://claude.ai/code) | 运行 Agent 的平台 |
| [TradingView Desktop](https://www.tradingview.com/desktop/) | 拉取 K 线数据（需付费订阅） |
| [tradingview-mcp](https://github.com/tradesdontlie/tradingview-mcp) | TradingView ↔ Claude Code 桥接 |
| [Notion](https://www.notion.so/) | 存储分析结果（可选，免费账号即可） |
| Al Brooks / Rose 视频字幕 `.srt` 文件 | 分析素材，自行获取 |

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/laizheqixi-web/PA-Agent-.git
cd PA-Agent-
```

### 2. 安装 TradingView MCP

```bash
git clone https://github.com/tradesdontlie/tradingview-mcp.git
cd tradingview-mcp
npm install
```

参考 [tradingview-mcp 文档](https://github.com/tradesdontlie/tradingview-mcp) 配置 MCP 连接。

### 3. 配置 Notion（可选）

复制配置模板：

```bash
cp notion_config_template.json notion_config.json
```

编辑 `notion_config.json`，填入你自己的 Notion 数据库 ID。

或者运行脚本自动创建数据库结构：

```bash
python create_notion_dbs.py
```

### 4. 修改路径

打开 `CLAUDE.md`，将所有路径替换为你本机的实际路径。

### 5. 启动 TradingView 调试模式

**Windows：**
```bash
scripts\launch_tv_debug.bat
```

---

## 使用方法

在 Claude Code 中：

**分析一期视频：**
```
分析字幕 D:\path\to\your\video.srt
```

**迭代知识库：**
```
迭代知识库
```

**收盘复盘：**
```
复盘今天
```
或
```
帮我复盘 2026-06-18
```

---

## 知识库

`知识库/AL_Rose_迭代知识库.md` 是本项目的核心资产。

- 目录里的版本是 **starter 版**，包含 5 期视频提炼的规则
- **你的知识库应该是你自己的**：分析越多视频，规则越多，置信度越高
- 置信度评级：★★★ = 多次验证 / ★★ = 初步验证 / ★ = 待验证

社区可以通过 PR 提交新规则，但每个人自己决定合并什么。

---

## 目录结构

```
PA-Agent-/
├── CLAUDE.md                          # 项目主配置，Claude Code 读取
├── .claude/
│   └── agents/
│       ├── rose-video-analyst.md      # Agent 1：视频分析
│       └── alrose-daily-reviewer.md   # Agent 3：实盘复盘
├── 技能配置/
│   ├── SKILL_iterate-al-rose.md       # Agent 2：知识库迭代
│   └── SKILL_alrose-daily-review.md   # 复盘技能
├── 知识库/
│   ├── AL_Rose_迭代知识库.md          # 知识库（starter 版）
│   └── Rose_AlBrooks_分析系统提示词.md # 分析参考
├── 视频分析/                           # 示例输出
├── scripts/
│   └── get_chart_data.mjs             # 拉取 K 线数据
├── create_notion_dbs.py               # 创建 Notion 数据库结构
└── notion_config_template.json        # Notion 配置模板
```

---

## 社区

微信群：[二维码 / 联系方式]

一起学习 Al Brooks，一起迭代 Agent，一起在市场里赚钱。

---

## License

MIT
