"""
DeepSeek API 辅助脚本 — 供 Claude Code agent 调用，处理长文本生成任务。

输入文件格式（--input）：
  - 纯文本 → 直接作为 user message
  - 以 ---SYSTEM--- 开头 → 解析系统提示词与用户消息（用 ---USER--- 分隔）

用法：
  python call_deepseek.py --input=prompt.txt [--output=result.txt] [--model=deepseek-chat] [--max-tokens=8192]
  python call_deepseek.py --test

依赖：pip install openai
环境变量：DEEPSEEK_API_KEY
"""

import argparse
import os
import sys
from pathlib import Path


def load_env():
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Call DeepSeek API for text generation")
    parser.add_argument("--input", help="Path to input prompt file")
    parser.add_argument("--output", help="Path to write output (default: stdout)")
    parser.add_argument("--model", default="deepseek-v4-flash", help="DeepSeek model (default: deepseek-v4-flash)")
    parser.add_argument("--max-tokens", type=int, default=8192, help="Max output tokens (default: 8192)")
    parser.add_argument("--test", action="store_true", help="Test API connectivity and exit")
    args = parser.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY environment variable not set", file=sys.stderr)
        print("Set it with: $env:DEEPSEEK_API_KEY = 'your-key'  (PowerShell)", file=sys.stderr)
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    if args.test:
        try:
            response = client.chat.completions.create(
                model=args.model,
                messages=[{"role": "user", "content": "Say hello in one word."}],
                max_tokens=100,
            )
            content = response.choices[0].message.content
            print(f"DeepSeek API connected. Model: {args.model}. Response: {content}")
        except Exception as e:
            print(f"ERROR: API test failed - {e}", file=sys.stderr)
            sys.exit(1)
        return

    if not args.input:
        print("ERROR: --input is required (use --test to check connectivity)", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    # Parse optional system/user split
    system_prompt = None
    user_content = content.strip()

    if content.startswith("---SYSTEM---"):
        parts = content.split("---USER---", 1)
        if len(parts) == 2:
            system_prompt = parts[0].replace("---SYSTEM---", "").strip()
            user_content = parts[1].strip()
        else:
            # No ---USER--- found; treat everything after ---SYSTEM--- as user content
            user_content = content.replace("---SYSTEM---", "").strip()

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_content})

    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=messages,
            max_tokens=args.max_tokens,
        )
    except Exception as e:
        print(f"ERROR: API call failed — {e}", file=sys.stderr)
        sys.exit(1)

    result = response.choices[0].message.content

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        tokens_used = response.usage.total_tokens if response.usage else "unknown"
        print(f"[DeepSeek] Output written to {args.output} (tokens used: {tokens_used})", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
