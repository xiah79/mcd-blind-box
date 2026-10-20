#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mcd-blind-box 提交前自检脚本
用途：确认 GitHub 仓库里没有真实凭证，且必交文件齐全。

用法：
    python check_submission.py
    python check_submission.py --dir /path/to/repo
"""

import os
import re
import sys
import json

# 必交文件（官方要求的标准命名）
REQUIRED = [
    "README.md",
    "CONTEST_DECLARATION.md",
    "MCP_INTEGRATION.md",
    "mcp-config.example.json",
    "workbuddy.md",
]

# 推荐随仓库分发的补充材料（缺失会提示，但不阻断提交）
OPTIONAL = [
    "BLOG_ARTICLE.md",          # 工程复盘长文
    "BLOG_SHORTS.md",           # 对外发布短文模板
    "MCP_BUG_REPORT.md",        # 接口问题反馈
    "DEFENSE_NOTES.md",         # 答辩要点
    "TEST_REPORT_FINAL.md",     # 最终测试报告
    "SUBMISSION_GUIDE.md",      # 提交指南
    "check_submission.py",      # 本脚本
    "test_memory.py",           # 记忆算法离线测试
    ".workbuddy/skills/mcd-blind-box/SKILL.md",
    ".workbuddy/skills/mcd-blind-box/memory.json",
]

# 本地文件，不应出现在仓库里
LOCAL_ONLY = [
    "PUBLISH_NOTES.md",         # 发布工作笔记
    "mcp.json",                 # 真实凭证配置
]

# 绝不能出现的文件（若已在 .gitignore 中则不算问题）
FORBIDDEN_FILES = [
    ".env",
    "mcp.json",            # 真实凭证配置，绝不能进仓库
    "mcp.json.disabled",
    "mcp.json.bak",
]

# Token 特征（不含示例占位符）
TOKEN_PATTERNS = [
    (re.compile(r"Bearer\s+[A-Za-z0-9_\-]{16,}"), "疑似真实 Bearer Token"),
    (re.compile(r"MCD_MCP_TOKEN\s*=\s*[A-Za-z0-9_\-]{16,}"), "疑似真实 MCD_MCP_TOKEN"),
]

# 允许出现的占位符
PLACEHOLDER = re.compile(r"\$\{MCD_MCP_TOKEN\}")

TEXT_EXT = {".md", ".json", ".py", ".txt", ".example", ".env", ".gitignore"}


def scan_tokens(root):
    """扫描全目录，返回真实凭证泄漏点"""
    hits = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__"}]
        for fn in filenames:
            path = os.path.join(dirpath, fn)
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT and fn not in (".gitignore", ".env"):
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except OSError:
                continue
            for line_no, line in enumerate(content.splitlines(), 1):
                if PLACEHOLDER.search(line):
                    continue
                for pattern, desc in TOKEN_PATTERNS:
                    if pattern.search(line):
                        rel = os.path.relpath(path, root)
                        hits.append((rel, line_no, desc, line.strip()[:80]))
    return hits


def read_gitignore(root):
    """读取 .gitignore 规则（简单匹配）"""
    path = os.path.join(root, ".gitignore")
    rules = []
    if not os.path.isfile(path):
        return rules
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                rules.append(line.rstrip("/"))
    return rules


def is_gitignored(rel_path, rules):
    """判断某文件是否被 gitignore 规则覆盖"""
    name = os.path.basename(rel_path)
    for rule in rules:
        if rule == name or rel_path.endswith("/" + rule) or rel_path == rule:
            return True
        if rule.endswith("*") and name.startswith(rule[:-1]):
            return True
    return False


def main():
    root = os.path.abspath(
        sys.argv[sys.argv.index("--dir") + 1] if "--dir" in sys.argv else os.getcwd()
    )
    print(f"检查目录: {root}\n" + "=" * 60)

    ok = True
    rules = read_gitignore(root)

    # 1. 必交文件
    print("[1] 必交文件检查")
    for name in REQUIRED:
        exists = os.path.isfile(os.path.join(root, name))
        size = os.path.getsize(os.path.join(root, name)) if exists else 0
        mark = "OK  " if exists and size > 0 else "缺失"
        if mark == "缺失":
            ok = False
        print(f"    [{mark}] {name}" + (f"  ({size} bytes)" if exists else ""))
    print()

    # 1b. 推荐材料
    print("[1b] 推荐材料检查（缺失不阻断提交）")
    for name in OPTIONAL:
        p = os.path.join(root, name)
        if os.path.isfile(p):
            print(f"    [OK  ] {name}  ({os.path.getsize(p)} bytes)")
        else:
            print(f"    [缺失] {name}")
    print()

    # 2. 禁止文件（区分「已被 gitignore 忽略」与「会被提交」）
    print("[2] 不应提交的文件检查")
    found_forbidden = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for fn in filenames:
            if fn in FORBIDDEN_FILES or fn in LOCAL_ONLY:
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                found_forbidden.append((rel, is_gitignored(rel, rules)))
    if found_forbidden:
        for rel, ignored in found_forbidden:
            if ignored:
                print(f"    [安全] {rel}  已被 .gitignore 忽略，不会进入提交")
            else:
                ok = False
                print(f"    [警告] {rel}  未被忽略，提交前请移出或加入 .gitignore")
    else:
        print("    [OK  ] 未发现禁止文件")
    print()

    # 3. 凭证扫描
    print("[3] 凭证扫描（排除 ${MCD_MCP_TOKEN} 占位符）")
    hits = scan_tokens(root)
    real_leaks = []
    for rel, line_no, desc, snippet in hits:
        if is_gitignored(rel, rules):
            print(f"    [安全] {rel}:{line_no}  {desc}（已被 gitignore 忽略）")
        else:
            real_leaks.append((rel, line_no, desc, snippet))
    if real_leaks:
        ok = False
        for rel, line_no, desc, snippet in real_leaks:
            print(f"    [泄漏] {rel}:{line_no}  {desc}")
            print(f"           {snippet}")
    else:
        print("    [OK  ] 无未被忽略的真实凭证")
    print()

    # 4. 配置示例校验
    print("[4] mcp-config.example.json 校验")
    cfg_path = os.path.join(root, "mcp-config.example.json")
    if os.path.isfile(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            server = cfg.get("mcpServers", {}).get("mcd-mcp", {})
            checks = [
                ("type == streamablehttp", server.get("type") == "streamablehttp"),
                ("url == https://mcp.mcd.cn", server.get("url") == "https://mcp.mcd.cn"),
                ("仅 Authorization 一个 header", list(server.get("headers", {}).keys()) == ["Authorization"]),
                ("Authorization 使用占位符", PLACEHOLDER.search(server.get("headers", {}).get("Authorization", "")) is not None),
                ("disabled == false", server.get("disabled") is False),
            ]
            for desc, passed in checks:
                print(f"    [{'OK  ' if passed else '错误'}] {desc}")
                if not passed:
                    ok = False
        except (OSError, json.JSONDecodeError) as e:
            ok = False
            print(f"    [错误] 无法解析: {e}")
    else:
        ok = False
        print("    [缺失] mcp-config.example.json")
    print()

    # 4b. 官方文件完整性校验
    print("[4b] 官方文件内容完整性校验")
    decl_path = os.path.join(root, "CONTEST_DECLARATION.md")
    if os.path.isfile(decl_path):
        with open(decl_path, "r", encoding="utf-8") as f:
            decl = f.read()
        # 官方原文必须包含的 5 个章节标题
        required_sections = [
            "## 原创性声明",
            "## 合规声明",
            "## 信息安全声明",
            "## 使用提示",
            "## 规则遵守声明",
        ]
        missing = [s for s in required_sections if s not in decl]
        if missing:
            ok = False
            print(f"    [错误] CONTEST_DECLARATION.md 缺少官方章节: {missing}")
            print("           官方要求「文件内容不可修改」，请从官方仓库恢复原文：")
            print("           https://github.com/M-China/mcd-developer-innovation-challenge/blob/main/CONTEST_DECLARATION.md")
        else:
            # 校验没有夹带自定义内容
            custom_markers = ["参赛人签字", "**项目名称**", "GitHub 仓库地址", "_____"]
            polluted = [m for m in custom_markers if m in decl]
            if polluted:
                ok = False
                print(f"    [错误] CONTEST_DECLARATION.md 含自定义内容: {polluted}")
                print("           官方要求内容不可修改，请恢复为官方原文")
            else:
                print("    [OK  ] CONTEST_DECLARATION.md 与官方原文一致（5 章节齐全，无夹带）")
    else:
        ok = False
        print("    [缺失] CONTEST_DECLARATION.md")
    print()

    # 5. 双份副本同步检查
    print("[5] 项目级副本 vs 用户级生效版本 同步检查")
    user_skill_dir = os.path.expanduser("~/.workbuddy/skills/mcd-blind-box")
    pairs = [
        ("SKILL.md",
         os.path.join(root, ".workbuddy/skills/mcd-blind-box/SKILL.md"),
         os.path.join(user_skill_dir, "SKILL.md")),
        ("memory.json",
         os.path.join(root, ".workbuddy/skills/mcd-blind-box/memory.json"),
         os.path.join(user_skill_dir, "memory.json")),
    ]
    for name, proj, user in pairs:
        if not (os.path.isfile(proj) and os.path.isfile(user)):
            print(f"    [跳过] {name}  （缺少任一副本）")
            continue
        with open(proj, "r", encoding="utf-8") as f:
            a = f.read()
        with open(user, "r", encoding="utf-8") as f:
            b = f.read()
        if a == b:
            print(f"    [OK  ] {name}  两份一致")
        else:
            ok = False
            print(f"    [不同步] {name}  项目级({len(a.encode())}B) ≠ 用户级({len(b.encode())}B)")
            print(f"             提交前请把用户级版本复制覆盖到项目级：{proj}")
    print()

    print("=" * 60)
    print("结果:", "全部通过，可以提交" if ok else "存在问题，请先修复")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
