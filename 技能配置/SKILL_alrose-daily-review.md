---
name: alrose-daily-review
description: Post-close full session analysis of ES/NQ in Al Brooks & Rose style. Pulls today's multi-timeframe data (monthly/daily/H1/5-min) from TradingView, then generates a structured bar-by-bar analysis report identical in format to the video analysis files. Use when user says 复盘今天, 分析今天盘面, 帮我复盘, 今天收盘了, 盘面分析, or names a specific date for post-close review.
---

# AL Brooks & Rose 收盘后盘面复盘

## 触发条件
用户说"复盘今天"、"分析今天盘面"、"帮我复盘"、"今天收盘了"、"帮我分析 YYYY-MM-DD"。

## 工作模式
**收盘后全量复盘**：拉取当天完整 K 线数据（月线背景 + 日线 + H1 + 5分钟全session），像分析字幕视频一样逐棒还原，生成与 `2025-04-21_AlBrooks_Rose_分析.md` 格式完全一致的分析报告。

---

## 执行流程

### Step 1：确定复盘日期
- 若用户未指定，默认为今天
- 格式：`YYYY-MM-DD`（如 `2026-06-18`）

### Step 2：拉取多周期 K 线数据
在 `D:\AI视频\AI分析视频\tradingview-mcp\` 目录下运行：
```
node get_chart_data.mjs YYYY-MM-DD
```
（脚本已更新，支持日期参数，会抓取月线/日线/H1/5分钟数据）

读取输出文件 `D:\AI视频\AI分析视频\chart_data_YYYY-MM-DD.json`，提取：
- **月线**（近24棒）→ 大背景：趋势 or 区间
- **日线**（近40棒）→ 近期走势、今日缺口方向与大小
- **H1**（当日约14棒）→ 小时级结构、关键支撑阻力
- **5分钟**（当日 RTH 完整 session，约80棒）→ 逐棒分析主体

### Step 3：加载知识库
读取 `D:\AI视频\AI分析视频\AL_Rose_迭代知识库.md`

### Step 4：生成完整分析报告
按照以下格式（与 `2025-04-21_AlBrooks_Rose_分析.md` 一致）生成报告：

---

**报告格式**：

```markdown
# YYYY-MM-DD（周X）盘面复盘（Al Brooks 视角）
> 品种：ES 标普期货 5分钟图 | 日型：[待识别]

## 零、图表数据背景

### ▌月线数据
| 项目 | 数值 | 含义 |
前后月对比表格...

### ▌日线数据（近10日）
| 日期 | 开盘 | 最高 | 最低 | 收盘 | 备注 |

### ▌今日概况
缺口大小 / 与EMA关系 / 开盘性质

## 一、开盘背景（多周期分析）

### ▌月线视角
...

### ▌周线视角
...

### ▌日线视角
...

### ▌60分钟视角
...

### ▌开盘概率框架
| 项目 | 内容 |
| 缺口方向 | ... |
| 与均线关系 | ... |
| 开盘情景概率 | 60%XX / 20%XX / 20%XX |

## 二、K 线逐棒解析（Al Brooks 视角）

### ▌第一阶段：XXXX（K1–KN）
**K1（开盘棒）**
- 棒型：...
- Al Brooks 视角：...
- 概率判断：...

**K2**
...

### ▌第二阶段：XXXX（KN–KM）
...

## 三、关键形态与规则匹配

| 形态/规则 | 出现位置 | 知识库置信度 | 今日表现 |
|-----------|---------|------------|---------|
| 均线磁吸 | K12附近 | ★★★ | ✅ |
| AIS确认 | K3-K5 | ★★★ | ✅ |
| ... | | | |

## 四、日型总结

| 项目 | 内容 |
|------|------|
| 日型 | ... |
| Always In | ... |
| 关键低/高点 | ... |
| 反转质量 | ... |
| 日内结构 | ... |

## 五、明日参考
- 关键支撑：...
- 关键阻力：...
- 若明日平开，偏向：[多/空/中性]，原因：...
```

---

### Step 5：保存分析文件
将报告写入：
```
D:\AI视频\AI分析视频\YYYY-MM-DD_盘面复盘.md
```

### Step 6：知识库规则对照
列出今日触发的知识库规则，标注：
- ✅ 验证（频次+1）
- ❌ 反例（追加矛盾记录）
- 【待迭代】新发现规律

提示用户：如有新规律，运行 `/iterate-al-rose` 更新知识库。

### Step 7：写入 Notion（可选）
检查 `notion_config.json`，若有效则写入：
```json
{
  "date": "YYYY-MM-DD",
  "type": "盘面复盘",
  "day_type": "...",
  "ais_direction": "...",
  "key_rules_verified": [...],
  "new_patterns": [...],
  "file": "YYYY-MM-DD_盘面复盘.md"
}
```

---

## 注意事项
- 始终保持"左侧视角"还原：分析K1时只能看到K1，不能用K30的信息解读K1
- 每棒给出具体概率（60%/40%），不用"可能"、"也许"
- 优先引用知识库 ★★★ 规则，新规律标【待迭代】
- 5分钟数据超过80棒时，重点分析开盘前30棒（建仓阶段）和关键转折点
