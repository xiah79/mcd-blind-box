#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
仓库状态自查脚本 —— 报名前后随时运行
用法：python check_repo.py
"""

import json
import ssl
import sys
import urllib.request

REPO = "xiah79/mcd-blind-box"
API = f"https://api.github.com/repos/{REPO}"
# Star 榜前 100 名门槛（2026-10-20 快照：第 97 名 22 Star）
RANKING_THRESHOLD = 22

# 期望的 topics（对照 GitHub 规则：小写字母或数字开头，<=50 字符，可含连字符）
EXPECTED_TOPICS = ["mcd-blind-box", "workbuddy", "mcp", "skill", "mcd-code"]


def fetch(url):
    """走系统证书库（企业环境有 MITM 证书，curl/python 默认 CA 会失败）"""
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "mcd-blind-box-check"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as f:
        return json.load(f)


def main():
    print(f"=== {REPO} 状态自查 ===\n")
    try:
        d = fetch(API)
    except Exception as e:
        print(f"  [错误] API 访问失败: {type(e).__name__} {str(e)[:120]}")
        print("  提示：企业网络的证书劫持会导致默认 CA 校验失败，")
        print("        本脚本用系统证书库（ssl.create_default_context）可正常访问。")
        return 1

    stars = d.get("stargazers_count", 0)
    topics = d.get("topics") or []
    forks = d.get("forks_count", 0)
    private = d.get("private")
    lic = (d.get("license") or {}).get("spdx_id")

    print("[1] 基础信息")
    print(f"    可见性   : {'Public ✅' if not private else 'Private ❌ 必须改成 Public'}")
    print(f"    Star     : {stars}")
    print(f"    Fork     : {forks}")
    print(f"    License  : {lic or '(未识别, GitHub 同步有延迟)'}")
    print(f"    描述     : {'已填 ✅' if d.get('description') else '未填 ❌'}")
    print()

    print("[2] Topics 校验（官方要求：小写字母/数字开头，≤50 字符，可含连字符）")
    if not topics:
        print("    [错误] Topics 为空 —— 会被搜索到但不利于曝光")
    else:
        for t in topics:
            ok = (t[0].islower() or t[0].isdigit()) and len(t) <= 50 and " " not in t
            print(f"    [{'OK  ' if ok else '错误'}] {t}")
        missing = [t for t in EXPECTED_TOPICS if t not in topics]
        if missing:
            print(f"    [提示] 建议补充: {missing}")
    print()

    print("[3] 入榜评估")
    if stars == 0:
        print("    [警告] Star = 0，官方规则「Star 数大于 0 的项目才进入排行榜」")
    elif stars < RANKING_THRESHOLD:
        gap = RANKING_THRESHOLD - stars
        print(f"    [提示] 当前 {stars} Star，榜内门槛约 {RANKING_THRESHOLD}（第 97 名）")
        print(f"           还差 {gap} 个 Star")
    else:
        print(f"    [OK  ] {stars} Star，已过前 100 名门槛")
    print()

    print("[4] 提交状态提醒")
    print("    报名 Issue : https://github.com/M-China/mcd-developer-innovation-challenge/issues")
    print("    要求      : 标题以【参赛申请】开头，字段名与内容同行，链接裸 URL")
    print("    排行榜    : https://github.com/M-China/mcd-developer-innovation-challenge/blob/main/RANKING.md")
    print("    截止      : 2026-10-25 23:59（统计截止 10-26 00:00）")

    return 0


if __name__ == "__main__":
    sys.exit(main())
