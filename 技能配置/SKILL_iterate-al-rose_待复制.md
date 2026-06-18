---
name: iterate-al-rose
description: Iterate and update the AL & Rose trading knowledge base after a new video analysis file is generated. Read all session analysis files in D:\AI视频\AI分析视频\, extract patterns, update AL_Rose_迭代知识库.md, and write structured records to Notion. Use when user says 迭代知识库, update knowledge base, iterate, 更新知识库, or after finishing a new analysis file.
---

# AL & Rose 知识库迭代技能

## 触发条件
用户完成一期新的视频字幕分析后运行，或者说"迭代知识库"、"update knowledge"。

## 执行流程

### Step 1：扫描所有分析文件
读取 `D:\AI视频\AI分析视频\` 下所有以 `_分析.md` 结尾的文件，以及 `Rose_AlBrooks_分析系统提示词.md`。
按日期排序，确认哪些是新文件（未在知识库更新日志中记录的）。

### Step 2：读取现有知识库
读取 `D:\AI视频\AI分析视频\AL_Rose_迭代知识库.md`，了解当前已知规则、频次和置信度。

### Step 3：从新文件提取结构化数据
对每个新分析文件，提取以下信息：

**基础信息：**
- 日期
- 品种（ES/NQ/其他）
- 主讲人（Al Brooks / Rose / 学生）
- 日型（大幅高开/低开/平开+趋势/平开+区间/反转日）
- 最终收盘结构（Always In Long / Short / 震荡区间）

**技巧层面（重点提取）：**
- Al Brooks 提到的概率数字和场景
- Rose 的进场点、止损、目标设定方式
- 出现的新形态或规则
- 与已知规则相符或矛盾的地方

**关键价位：**
- 当日低点/高点（实际数值）
- 量度目标是否达到
- 均线位置与价格距离

### Step 4：更新知识库
按以下逻辑更新 `AL_Rose_迭代知识库.md`：

1. **元数据索引**：在表格最上方追加新场次记录
2. **已有规则**：如新场次再次验证，则 `见到次数 +1`，置信度可能升级（2次→★★, 3次→★★★）
3. **新规则**：如新场次出现从未见过的技巧或规律，添加到对应章节，标注 `1/N` 和 `★`
4. **矛盾**：如新场次与已知规则相反，在"已发现矛盾"章节追加记录，标注"需追踪"
5. **待深化**：将新发现但仅见一次的内容放入第六节
6. **更新日志**：在第八节追加今日更新记录

### Step 5：写入 Notion（需配置数据库ID）
检查 `D:\AI视频\AI分析视频\notion_config.json` 是否存在且含有 `al_rose_db_id` 字段。

如果存在，使用 n8n MCP 或 Notion API 创建新数据库行，字段如下：

```json
{
  "date": "YYYY-MM-DD",
  "day_type": "大幅低开",
  "teacher": ["Al Brooks", "Rose"],
  "techniques": ["三腿卖出高潮", "5200大整数", "II形态"],
  "final_structure": "震荡区间",
  "key_low": 5171.75,
  "key_high": 5339.25,
  "file_path": "D:\\AI视频\\AI分析视频\\2025-04-21_AlBrooks_Rose_分析.md",
  "summary": "大幅低开130点后三腿卖出高潮至5171，5200区域反转进入震荡区间"
}
```

如果不存在配置文件，输出结构化数据并提示用户设置 Notion 数据库ID。

### Step 6：输出报告
告知用户：
- 本次新增了哪些规则（新发现）
- 哪些规则置信度升级（从★到★★，从★★到★★★）
- 是否发现了矛盾
- 知识库当前状态（总场次、规则数、高置信度规则数）

## 输出格式示例

```
✅ 知识库已更新（第3场次）

新增规则：
- [★新] 三角旗形突破后目标 = 旗杆高度（来源：04/28场次）

升级规则：
- [★→★★] "区间日早期识别：前3棒出现双影"（2/3 场次验证）

矛盾记录：
- 无

当前状态：总场次3 | 总规则47条 | 高置信度(★★★)：12条
```
