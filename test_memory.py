import json, sys

# 模拟一次开盒的抽签决策，验证去重规则
def pick_meals(candidates, opened, avoid, want=2):
    """按 SKILL.md 抽签规则选品"""
    # 规则1剔除忌口
    pool = [m for m in candidates if m not in avoid]
    # 规则2 优先未收集
    unseen = [m for m in pool if opened.get(m, 0) == 0]
    if unseen:
        return unseen[:want], "优先未收集"
    # 规则3 全抽过了，按次数升序
    pool.sort(key=lambda m: opened.get(m, 0))
    return pool[:want], "最冷门优先"

def rarity(count):
    if count == 0: return "未收集"
    if count == 1: return "初次邂逅"
    if count <= 3: return "常客"
    return "本命"

opened = {
    "9900016075": 1, "521914": 1, "9900015008": 1, "521770": 1,
    "9900016073": 1, "9900016371": 1, "9900005456": 1, "521901": 1
}

# 场景A：候选中含4 个未收集项
candsA = ["9900016075", "9900015008", "1100", "1406", "9900015602", "1700"]
r, why = pick_meals(candsA, opened, [])
print("场景A 含未收集项 ->", r, "|", why)
assert "1100" in r or "1406" in r or "9900015602" in r or "1700" in r, "FAIL: 应优先抽未收集项"
assert "9900016075" not in r and "9900015008" not in r, "FAIL: 已收集项不应优先"
print("  PASS 未收集项优先，已收集项被避开")

# 场景B：候选全部抽过，应挑最冷门
opened2 = {"A": 5, "B": 2, "C": 1, "D": 3}
r2, why2 = pick_meals(["A", "B", "C", "D"], opened2, [])
print("场景B 全部抽过 ->", r2, "|", why2)
assert r2 == ["C", "B"], f"FAIL: 应按次数升序，实际 {r2}"
print("  PASS 按出现次数升序，最冷门优先")

# 场景C：忌口硬排除
r3, why3 = pick_meals(["A", "B", "C"], {"A": 1, "B": 1, "C": 1}, ["B"])
print("场景C 含忌口B ->", r3, "|", why3)
assert "B" not in r3, "FAIL: 忌口项未被排除"
print("  PASS 忌口项已排除")

# 稀有度判定
print("稀有度判定:")
for c in [0, 1, 2, 3, 4, 10]:
    print(f"  {c} 次 -> {rarity(c)}")
assert rarity(0) == "未收集" and rarity(1) == "初次邂逅"
assert rarity(2) == "常客" and rarity(4) == "本命"
print("  PASS 稀有度分级正确")

# 收集进度计算
total = len(set(list(opened.keys())))
print(f"收集进度: 已集 {total} 种")
print("\n全部用例通过")