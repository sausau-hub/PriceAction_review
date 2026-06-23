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
| [DeepSeek API](https://platform.deepseek.com) | 长文本生成辅助（可选，替代 Claude 处理大 token 任务） |
| Al Brooks / Rose 视频字幕 `.srt` 文件 | 分析素材，自行获取 |

---

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/sausau-hub/PriceAction_review.git
cd PriceAction_review
```

### 2. 安装 TradingView MCP

```bash
git clone https://github.com/tradesdontlie/tradingview-mcp.git
cd tradingview-mcp
npm install
```

参考 [tradingview-mcp 文档](https://github.com/tradesdontlie/tradingview-mcp) 配置 MCP 连接。

### 3. 配置环境变量

复制并编辑 `.env`：

```
DEEPSEEK_API_KEY=your_deepseek_key   # 可选
NOTION_TOKEN=your_notion_token       # 可选
```

### 4. 配置 Notion（可选）

复制配置模板：

```bash
cp notion_config_template.json notion_config.json
```

编辑 `notion_config.json`，填入你自己的 Notion 数据库 ID。

或者运行脚本自动创建数据库结构：

```bash
python create_notion_dbs.py
```

### 5. 修改路径

打开 `CLAUDE.md`，将所有路径替换为你本机的实际路径。

### 6. 启动 TradingView 调试模式

**Windows：**
```bash
python start_tradingview.py
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

## 分析原则

Agent 生成的所有分析内容遵循一条核心原则：**以视频内容还原为主，不加主观判断。**

- 交易决策（做多 / 做空 / 加仓）只在字幕里讲解人明确说出时才写，并附英文原话作为依据
- 概率数字只在字幕明确提及时才写，不由 AI 自行估算
- "为什么不进场"必须单独列出，不合并到进场逻辑里

这样做的目的：防止 AI 把自己的分析混入视频内容，让知识库只沉淀讲解人真实说过的东西。

---

## 个人过滤器

`知识库/我的交易关注点.md` 是提升分析质量的关键。

AI 分析 5 小时视频时默认会压缩大量内容，但每个人的交易系统关注点不同。通过这个文件告诉 AI：

- **必须完整保留**的技术维度（入场条件、止损逻辑、"为什么不进场"）
- **可以忽略**的内容（scalp、期权讨论）
- **自己目前理解有偏差**的地方（AI 会重点展开这些，而非泛泛而谈）

模板在仓库里，按自己的交易系统填写即可。

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
PriceAction_review/
├── CLAUDE.md                          # 项目主配置，Claude Code 读取
├── .claude/
│   └── agents/
│       ├── rose-video-analyst.md      # Agent 1：视频分析
│       └── alrose-daily-reviewer.md   # Agent 3：实盘复盘
├── 知识库/
│   ├── AL_Rose_迭代知识库.md          # 知识库（starter 版，5期）
│   ├── Rose_AlBrooks_分析系统提示词.md # 分析参考
│   └── 我的交易关注点.md              # 个人过滤器模板
├── 视频分析/                           # 示例分析输出
├── get_chart_data.mjs                 # 拉取 TradingView K 线数据
├── start_tradingview.py               # 自动启动 TradingView 调试模式
├── call_deepseek.py                   # DeepSeek API 辅助脚本
├── notion_writer.py                   # Notion 写入工具
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
