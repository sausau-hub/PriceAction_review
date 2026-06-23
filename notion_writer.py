"""
Notion 写入工具 — 供 agent Bash 步骤调用
用法:
  python notion_writer.py --target=video_session --input=notion_data.json
  python notion_writer.py --target=daily_review  --input=notion_data.json
  python notion_writer.py --target=knowledge_rule --input=notion_data.json

--target 对应的数据库和字段映射见下方 TARGETS。
--input  JSON 文件路径，格式见各 target 的 FIELDS 说明。
"""

import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# ── 加载 .env ──────────────────────────────────────────────────────────────
def load_env():
    env_path = Path(__file__).parent / '.env'
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        import os
        os.environ.setdefault(k.strip(), v.strip())

load_env()

import os
TOKEN = os.environ.get('NOTION_TOKEN', '')
NOTION_VERSION = '2022-06-28'

# ── 数据库 ID ──────────────────────────────────────────────────────────────
config_path = Path(__file__).parent / 'notion_config.json'
_cfg = json.loads(config_path.read_text(encoding='utf-8')) if config_path.exists() else {}

DB = {
    'video_session':  _cfg.get('video_sessions_db_id', '260273a9-1e7f-4d08-a4ba-d1702d8c87b3'),
    'daily_review':   _cfg.get('daily_review_db_id',   '388991d2-5740-4209-9073-9c204800cce3'),
    'knowledge_rule': _cfg.get('knowledge_rules_db_id', 'd005a9e2-2f20-46bc-bd20-341a7817f3cc'),
}

# ── 字段构建器 ─────────────────────────────────────────────────────────────

def _title(text):
    return {'title': [{'text': {'content': str(text)[:2000]}}]}

def _rich(text):
    return {'rich_text': [{'text': {'content': str(text)[:2000]}}]}

def _date(d):
    return {'date': {'start': str(d)}}

def _select(name):
    return {'select': {'name': str(name)}}

def _multi_select(names):
    if isinstance(names, str):
        names = [n.strip() for n in names.split(',') if n.strip()]
    return {'multi_select': [{'name': n} for n in names]}

def _number(v):
    try:
        return {'number': float(v)}
    except (TypeError, ValueError):
        return {'number': None}


def build_video_session(d: dict) -> dict:
    """
    输入字段（JSON）：
      title         str   页面标题，如 "2025-04-14 Al Brooks + Rose 视频分析"
      date          str   YYYY-MM-DD
      speakers      list|str  主讲人，如 ["Al Brooks","Rose"] 或 "Al Brooks,Rose"
      day_type      str   日型 select（大幅高开/大幅低开/平开多头急拉/平开区间/超级反转日/空头趋势日）
      close_structure str 收盘结构 select（多头趋势日/空头趋势日/震荡区间/反转多头/反转空头/混合）
      techniques    str   核心技巧（逗号分隔）
      summary       str   场次摘要
      file          str   分析文件路径
      rule_count    int   知识点数
    """
    props = {
        '名称':    _title(d.get('title', '')),
        '日期':    _date(d['date']),
    }
    if d.get('speakers'):
        props['主讲人'] = _multi_select(d['speakers'])
    if d.get('day_type'):
        props['日型'] = _select(d['day_type'])
    if d.get('close_structure'):
        props['收盘结构'] = _select(d['close_structure'])
    if d.get('techniques'):
        props['核心技巧'] = _rich(d['techniques'])
    if d.get('summary'):
        props['场次摘要'] = _rich(d['summary'])
    if d.get('file'):
        props['分析文件'] = _rich(d['file'])
    if d.get('rule_count') is not None:
        props['知识点数'] = _number(d['rule_count'])
    return props


def build_daily_review(d: dict) -> dict:
    """
    输入字段（JSON）：
      title         str   标题，如 "2025-04-14 大幅高开三段日"
      date          str   YYYY-MM-DD
      patterns      str   知识点&入场形态（逗号分隔）
      direction     str   方向 select（多/空）
      probability   int   本单概率 0-100
      result        str   失败或者成功 select（成功/失败）
      rr_ratio      float 盈亏比
    """
    props = {
        '标题': _title(d.get('title', '')),
        '日期': _date(d['date']),
    }
    if d.get('patterns'):
        props['知识点&入场形态'] = _rich(d['patterns'])
    if d.get('direction'):
        props['方向'] = _select(d['direction'])
    if d.get('probability') is not None:
        props['本单概率'] = _number(d['probability'])
    if d.get('result'):
        props['失败或者成功'] = _select(d['result'])
    if d.get('rr_ratio') is not None:
        props['盈亏比'] = _number(d['rr_ratio'])
    return props


def build_knowledge_rule(d: dict) -> dict:
    """
    输入字段（JSON）：
      rule          str   规则名称（title）
      category      str   分类
      confidence    str   置信度（如 ★★★）
      count         int   见到次数
      description   str   规则说明
      exceptions    str   例外/注意
      sources       str   出处场次
    """
    props = {
        '规则': _title(d.get('rule', '')),
    }
    if d.get('category'):
        props['分类'] = _rich(d['category'])
    if d.get('confidence'):
        props['置信度'] = _rich(d['confidence'])
    if d.get('count') is not None:
        props['见到次数'] = _number(d['count'])
    if d.get('description'):
        props['规则说明'] = _rich(d['description'])
    if d.get('exceptions'):
        props['例外/注意'] = _rich(d['exceptions'])
    if d.get('sources'):
        props['出处场次'] = _rich(d['sources'])
    return props


BUILDERS = {
    'video_session':  build_video_session,
    'daily_review':   build_daily_review,
    'knowledge_rule': build_knowledge_rule,
}

# ── Notion API ─────────────────────────────────────────────────────────────

def create_page(db_id: str, properties: dict) -> dict:
    if not TOKEN:
        raise RuntimeError('NOTION_TOKEN 未设置，请检查 .env 文件')
    payload = {'parent': {'database_id': db_id}, 'properties': properties}
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json',
    }
    req = urllib.request.Request(
        'https://api.notion.com/v1/pages',
        data=body, headers=headers, method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode('utf-8', errors='replace')
        raise RuntimeError(f'Notion API 错误 {e.code}: {err_body}')


# ── 主入口 ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', required=True, choices=list(BUILDERS.keys()),
                        help='写入目标: video_session / daily_review / knowledge_rule')
    parser.add_argument('--input', required=True, help='JSON 数据文件路径')
    args = parser.parse_args()

    data_path = Path(args.input)
    if not data_path.exists():
        print(f'[ERROR] 文件不存在: {data_path}', file=sys.stderr)
        sys.exit(1)

    data = json.loads(data_path.read_text(encoding='utf-8'))

    # 支持单条（dict）和批量（list）
    items = data if isinstance(data, list) else [data]

    db_id = DB[args.target]
    builder = BUILDERS[args.target]

    results = []
    for i, item in enumerate(items):
        try:
            props = builder(item)
            page = create_page(db_id, props)
            url = page.get('url', '')
            print(f'[OK] #{i+1} → {url}')
            results.append({'ok': True, 'url': url, 'id': page.get('id', '')})
        except Exception as e:
            print(f'[ERROR] #{i+1} → {e}', file=sys.stderr)
            results.append({'ok': False, 'error': str(e)})

    failed = [r for r in results if not r['ok']]
    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
