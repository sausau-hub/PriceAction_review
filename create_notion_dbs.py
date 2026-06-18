"""
创建 Notion 数据库：Rose分析场次 + AL_Rose规则库
运行前需要设置 NOTION_TOKEN 环境变量，或直接在脚本里填入 token。

获取 token 方法：
  ntn whoami 返回的 bot token 可以从 ntn 的 keyring 里提取，
  或者在 notion.so → Settings → Integrations 创建一个 internal integration 获取 secret。

用法：
  python create_notion_dbs.py <NOTION_TOKEN>
"""

import sys
import json
import urllib.request
import urllib.error

PARENT_PAGE_ID = "eda7bd12-e82e-4b34-b274-f63b69b136e6"
API_BASE = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

def api_post(token, path, body):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Notion-Version": NOTION_VERSION,
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)

def create_session_db(token):
    body = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "Rose 分析场次"}}],
        "properties": {
            "名称": {"title": {}},
            "日期": {"date": {}},
            "日型": {"select": {"options": [
                {"name": "大幅高开", "color": "green"},
                {"name": "大幅低开", "color": "red"},
                {"name": "平开趋势", "color": "blue"},
                {"name": "平开区间", "color": "yellow"},
                {"name": "反转日", "color": "purple"},
                {"name": "大波动区间", "color": "orange"},
            ]}},
            "主讲人": {"multi_select": {"options": [
                {"name": "Al Brooks", "color": "blue"},
                {"name": "Rose", "color": "pink"},
                {"name": "Tim Fairweather", "color": "green"},
                {"name": "Tim Stout", "color": "yellow"},
                {"name": "Brad Wolff", "color": "orange"},
            ]}},
            "核心技巧": {"multi_select": {"options": [
                {"name": "卖出高潮", "color": "red"},
                {"name": "三腿结构", "color": "orange"},
                {"name": "II形态", "color": "yellow"},
                {"name": "Globex判断", "color": "green"},
                {"name": "整数关口", "color": "blue"},
                {"name": "均线目标", "color": "purple"},
                {"name": "R倍数目标", "color": "pink"},
                {"name": "停止单策略", "color": "brown"},
                {"name": "棒体收盘", "color": "gray"},
                {"name": "腿计数", "color": "default"},
                {"name": "假突破", "color": "red"},
                {"name": "三角旗形", "color": "orange"},
                {"name": "内部棒IB", "color": "yellow"},
                {"name": "缺口日", "color": "green"},
                {"name": "限价单判断", "color": "blue"},
            ]}},
            "收盘结构": {"select": {"options": [
                {"name": "多头趋势日", "color": "green"},
                {"name": "空头趋势日", "color": "red"},
                {"name": "震荡区间", "color": "yellow"},
                {"name": "多头反转", "color": "blue"},
                {"name": "空头反转", "color": "orange"},
                {"name": "混合", "color": "gray"},
            ]}},
            "日低":     {"number": {"format": "number"}},
            "日高":     {"number": {"format": "number"}},
            "缺口点数": {"number": {"format": "number"}},
            "知识点数": {"number": {"format": "number"}},
            "场次摘要": {"rich_text": {}},
            "月线背景": {"rich_text": {}},
            "分析文件": {"rich_text": {}},
        }
    }
    return api_post(token, "/databases", body)

def create_rules_db(token):
    body = {
        "parent": {"type": "page_id", "page_id": PARENT_PAGE_ID},
        "title": [{"type": "text", "text": {"content": "AL_Rose 规则库"}}],
        "properties": {
            "规则":     {"title": {}},
            "置信度":   {"select": {"options": [
                {"name": "★ 待验证",    "color": "gray"},
                {"name": "★★ 建立证据", "color": "yellow"},
                {"name": "★★★ 高置信度","color": "green"},
            ]}},
            "分类": {"select": {"options": [
                {"name": "均线相关",   "color": "blue"},
                {"name": "进场技巧",   "color": "green"},
                {"name": "目标体系",   "color": "orange"},
                {"name": "日型识别",   "color": "yellow"},
                {"name": "Globex判断", "color": "purple"},
                {"name": "概率框架",   "color": "pink"},
                {"name": "形态",       "color": "red"},
                {"name": "Rose实盘",   "color": "brown"},
                {"name": "多周期分析", "color": "gray"},
            ]}},
            "见到次数": {"number": {"format": "number"}},
            "最近更新": {"date": {}},
            "出处场次": {"rich_text": {}},
            "例外条件": {"rich_text": {}},
            "适用场景": {"rich_text": {}},
        }
    }
    return api_post(token, "/databases", body)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python create_notion_dbs.py <NOTION_TOKEN>")
        print("token 格式: secret_xxxxxxxx 或 ntn_xxxxxxxx")
        sys.exit(1)

    token = sys.argv[1]
    print("创建 Rose分析场次 数据库...")
    r1 = create_session_db(token)
    session_db_id = r1["id"]
    session_db_url = r1.get("url", "")
    print(f"  ✅ ID: {session_db_id}")
    print(f"  URL: {session_db_url}")

    print("\n创建 AL_Rose规则库 数据库...")
    r2 = create_rules_db(token)
    rules_db_id = r2["id"]
    rules_db_url = r2.get("url", "")
    print(f"  ✅ ID: {rules_db_id}")
    print(f"  URL: {rules_db_url}")

    # 输出 notion_config.json
    config = {
        "al_rose_session_db_id": session_db_id,
        "al_rose_rules_db_id":   rules_db_id,
    }
    config_path = r"D:\AI视频\AI分析视频\notion_config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    print(f"\n✅ notion_config.json 已写入: {config_path}")
    print("\n请把以下 ID 补充到 trading-workspace/config.md：")
    print(f"  Rose分析场次: {session_db_id}")
    print(f"  AL_Rose规则库: {rules_db_id}")
