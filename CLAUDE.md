# Al Brooks & Rose 视频分析项目

## 项目目的
分析 Al Brooks 和 Rose 的 ES 期货实盘视频（字幕），提炼交易规则，迭代知识库，并同步写入 Notion。

---

## 核心工作流

```
.srt 字幕文件（D:\Trading\公开的Rose视频\ROSE2025\）
    ↓
分析字幕内容（Al Brooks 多周期逻辑 + Rose 操作体系）
    ↓
拉取 TradingView K线数据（node get_chart_data.mjs）
    ↓
生成分析文件（视频分析\YYYY-MM-DD_AlBrooks_Rose_分析.md）
    ↓
迭代知识库（知识库\AL_Rose_迭代知识库.md）
    ↓
写入 Notion（video_sessions_db_id / knowledge_rules_db_id）
```

---

## 目录结构

```
D:\AI视频\AI分析视频\
├── CLAUDE.md
├── notion_config.json
├── chart_data.json
├── get_chart_data.mjs
├── 启动TradingView调试模式.bat
├── create_notion_dbs.py
├── 复盘日志\               ← 收盘复盘文件（YYYY-MM-DD_盘面复盘.md）
├── 视频分析\               ← 字幕分析文件（YYYY-MM-DD_AlBrooks_Rose_分析.md）
├── 知识库\                 ← 知识库 + 提示词
│   ├── AL_Rose_迭代知识库.md
│   └── Rose_AlBrooks_分析系统提示词.md
├── 技能配置\               ← 技能草稿（复制到 skills\ 后生效）
└── tradingview-mcp\
```

---

## 关键文件

| 文件/目录 | 说明 |
|-----------|------|
| `D:\Trading\公开的Rose视频\ROSE2025\*.srt` | 字幕源文件 |
| `tradingview-mcp\get_chart_data.mjs` | 抓取月/日/H1 OHLCV 数据，输出 chart_data.json |
| `chart_data.json` | 最新抓取的 K线数据 |
| `视频分析\YYYY-MM-DD_AlBrooks_Rose_分析.md` | 每期视频的分析文件 |
| `复盘日志\YYYY-MM-DD_盘面复盘.md` | 收盘后复盘文件 |
| `知识库\AL_Rose_迭代知识库.md` | 跨场次规则汇总，含置信度评级 |
| `知识库\Rose_AlBrooks_分析系统提示词.md` | 分析时使用的提示词模板 |
| `notion_config.json` | Notion 连接配置（含各数据库 ID） |

---

## 已有技能（Skill）

| 触发词 | 技能 | 说明 |
|--------|------|------|
| 分析视频 / 分析字幕 | `analyze-rose-video` | 完整执行：读字幕→分析→拉数据→生成文件→迭代知识库→写Notion |
| 迭代知识库 / 更新知识库 | `iterate-al-rose` | 单独迭代知识库并写入 Notion |
| 复盘今天 / 帮我复盘 / 今天收盘了 / 分析今天盘面 / 分析 YYYY-MM-DD | `alrose-daily-review` | 收盘后全量复盘：拉取月线/日线/H1/5分钟数据 → 逐棒 Al Brooks 风格分析 → 生成分析报告 → 自动写入 Notion 视频复盘 |

---

## 当前进度

- 已分析场次：**3 期**（2025-04-01、2025-04-08、2025-04-21）
- 未分析场次：**18 期**（优先做 Al Brooks 参与的场次）
- 知识库状态：初版，★★★ 规则已有数条
- 已复盘日期：2026-06-17

### 待分析优先级
1. 其余 Rose 主讲场次（04/09、04/10、04/16、04/17、04/22、04/24、04/25 等）

---

## TradingView MCP

- 启动脚本：`启动TradingView调试模式.bat`
- CDP 端口：9222
- 抓数据命令（在 `tradingview-mcp\` 目录下执行）：
  ```
  node get_chart_data.mjs
  ```

---

## Notion 配置

- 配置文件：`notion_config.json`
- 如配置失效，运行 `create_notion_dbs.py` 重建数据库

| 数据库 | data_source_id |
|--------|---------------|
| 📹 Rose 视频分析场次 | `b99d60a3-eb57-4eaf-8d1c-d138531e1a12` |
| 📖 AL_Rose 知识库规则 | `9548f67e-5590-4d3b-be09-ace2f790c40b` |
| 🎥 视频复盘 | `e47c23af-d932-49cb-bf87-f5fcce59f6db` |
