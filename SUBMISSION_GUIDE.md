# 提交指南 · M-CODE 麦当劳程序员创意开发大赛

> **截止时间：2026 年 10 月 25 日 23:59**（提交 Issue 报名）
> **排行榜数据截止：2026 年 10 月 26 日 00:00**，按 GitHub 公开 Star 数排名

---

## 一、官方要求的必交文件

| 文件 | 状态 | 说明 |
| --- | --- | --- |
| `README.md` | ✅ 已完成 | 项目介绍 / 安装方法 / 使用示例 / 目标用户，四项齐备 |
| `CONTEST_DECLARATION.md` | ✅ 已完成 | 参赛声明：原创性 + 合规性 + 敏感信息 |
| `MCP_INTEGRATION.md` | ✅ 已完成 | MCP Server / Tool / 调用流程 / 业务价值 |
| `mcp-config.example.json` | ✅ 已完成 | 脱敏配置示例，**仅含 `${MCD_MCP_TOKEN}` 占位符** |
| `workbuddy.md` | ⚠️ **需你导出** | WorkBuddy 完整开发对话（专项奖励必需） |

---

## 二、`workbuddy.md` 怎么导出（唯一需要你动手的）

`workbuddy.md` 要求是**完整的 WorkBuddy 开发对话上下文**。这个必须是你真实对话的导出，我不能代写——伪造对话记录在评审里是硬伤。

### 操作路径

1. 在 WorkBuddy 里打开本次项目的对话
2. 用对话导出功能导出为 **Markdown 格式**
3. 存为 `mcd-blind-box/workbuddy.md`

### 如果没有一键导出

退而求其次的合规做法：把本次项目的**关键开发对话**按时间线整理成对话体（`### 用户：` / `### Buddy：`），内容必须真实来自本对话，包括：

- 初次开盒的完整往返（含你提出的位置幻觉质疑）
- 「券到底是谁的」那轮追问与实测验证
- 未经确认领券的失误与修正
- 稀缺档优先级从「限量→周X」调整为「周X→限量→上新」的讨论
- MCP 掉线与恢复的排查过程

⚠️ 整理版可以，但**不要编造未发生的对话**。本项目的对话质量本身就是加分项——它完整记录了从幻觉到修正的全过程。

---

## 三、提交前自检（一条命令）

```bash
cd mcd-blind-box
python check_submission.py
```

脚本会检查 5 项：

1. 5 个必交文件是否齐全
2. 是否混入了 `.env` / 废弃配置
3. **全目录扫描真实凭证泄漏**
4. `mcp-config.example.json` 格式是否符合官方要求（type / url / 单 header / 占位符 / disabled）
5. **项目级副本与用户级生效版本是否同步**（SKILL.md / memory.json）

### 当前自检结果

```
[1] 必交文件    → 5/5 齐备（含 workbuddy.md，170KB）
[2] 禁止文件    → .env 等均被 gitignore 保护
[3] 凭证扫描    → 无未被忽略的真实凭证
[4] 配置示例    → 5/5 全部通过
[5] 双份同步    → SKILL.md / memory.json 均一致
```

✅ **全部通过，可以提交。**

---

## 四、⚠️ 凭证安全：这是当前唯一的硬风险

**`mcd-blind-box/.env` 第 8 行有你的真实 Token（`MCD_MCP_TOKEN=<你的真实Token>`）。**

它虽然写在 `.gitignore` 里，但有两个泄漏途径：
- 用 **GitHub 网页端拖拽上传**时，`.gitignore` 不生效
- 初始化仓库时 `git add .` 若误改了 ignore 规则

### 处理建议（三选一）

| 方案 | 做法 | 适合 |
| --- | --- | --- |
| **A. 移出仓库**（推荐） | 把 `.env` 移到项目外，比如 `C:\Users\hp\.mcd-mcp.env`，`.gitignore` 保留规则 | 你的真实 Token 只在用户目录，项目目录干净 |
| **B. 清空内容** | 保留 `.env` 文件但把 Token 行改为注释 | 简单，但文件仍可能被误提交 |
| **C. 换 Token** | 去平台重新申请 Token，旧 Token 作废 | 最彻底 |

> 无论选哪种，**提交后都要到仓库页面肉眼确认一遍**：搜 `Bearer` 和 `MCD_MCP_TOKEN`，确认只命中 `mcp-config.example.json` 里的 `${MCD_MCP_TOKEN}`。

> 顺带一提：`.env` 里的 `MCD_MCP_BASE_URL` 也是旧值（带多余后缀），已同步修正到 `.env.example`，如果你保留 `.env` 也建议改一下。

---

## 五、废弃配置文件的处理（已处理）

`mcp.json.bak` 和 `.workbuddy/mcp.json.disabled` 内容相同，都是**已失效的错误配置**（`type: "http"`、URL 多了后缀、三个冗余 header）。

**已移出交付目录**，备份在 `_trash/mcp-config-dead/`（可回溯）。

理由：它们是「错误示范」，留在项目里评委照抄必然连不上；而「踩坑过程」这个叙事已经在 `MCP_INTEGRATION.md` 第一节用文字表格完整保留了，文件本身没必要进仓库。

**现在仓库里 MCP 配置只有一个来源**：`mcp-config.example.json`（根目录），内容即实测跑通的正确格式。

`.gitignore` 已加 `mcp.json` / `mcp.json.disabled` / `mcp.json.bak` 三条规则，**防止任何人往仓库里塞真实凭证配置**。

---

## 六、发布到 GitHub

✅ **已完成推送**。仓库地址：https://github.com/xiah79/mcd-blind-box

- 仓库可见性：**Public**
- 分支：`main`，3 个提交，21 个文件
- 远端凭证扫描：`Bearer` / `MCD_MCP_TOKEN` 均为**零命中**
- 远端引用：仅 `refs/heads/main` 一个，**无隐藏的 PR 引用或旧分支**
- reflog 无 `.env` 任何痕迹

<details>
<summary>环境配置记录（你本机遇到的两个坑，供参考）</summary>

**坑 1 · SSL 证书劫持**

本机装有 SteamTools 证书劫持工具，把 GitHub 证书重签为 `BeyondDimension SteamTools Certificate`。系统信任它（浏览器/Python 正常），但 git 的静态 CA bundle 里没有。

修法（**不关闭任何校验**）：

```bash
git config http.sslBackend schannel   # 改用 Windows 系统证书库
```

已设为**仓库级**配置（写在 `.git/config`，不影响其他项目，不进版本库）。

> 系统里有两张 SteamTools 证书：一张已于 2026/3/19 过期，一张有效期到 2027/1/13。schannel 会自动选对的那张。

**坑 2 · GitHub 禁用密码推送 + 22 端口被封**

- GitHub 自 2021-08 起彻底关闭密码推送，只接受 PAT 或 SSH
- 你公司网络封了 SSH 22 端口（`Connection refused`），但 443 通

最终方案：**SSH over 443**

```bash
# ~/.ssh/config
Host github.com
    HostName ssh.github.com
    Port 443
    User git
    IdentityFile ~/.ssh/id_ed25519_github
    IdentitiesOnly yes

git remote set-url origin git@github.com:xiah79/mcd-blind-box.git
```

密钥对已生成于 `C:\Users\hp\.ssh\id_ed25519_github`，公钥已添加到 GitHub 账号。

> 相比 PAT 的优势：私钥永不上传、永久有效、撤销只需删掉那把 key。

</details>

### 仓库设置建议

- ✅ 可见性：Public
- **Description**：`M-CODE 麦当劳程序员创意开发大赛参赛作品 · 有记忆的随机盲盒 Skill`（已填）
- **Topics**（可在网页端添加）：`mcd-blind-box` `workbuddy` `mcp` `skill` `mcd-code` —— 利于被搜索到

---

## 七、提交报名 Issue

1. 进入麦当劳 GitHub 官方账号活动页面（`M-China` 组织的 `mcd-developer-innovation-challenge` 仓库）
2. 找到 Issues → 新建 → 选择指定 Issue 模板
3. 填写：

```
参赛申请
项目名称：麦当劳随机盲盒
项目地址：https://github.com/<你的用户名>/<仓库名>
项目简介：把点餐变成收集游戏。有记忆的开盒体验——优先推没抽过的、
          忌口硬排除、稀有档按可验证性分层；同时用四条铁律守住 AI
          幻觉与写操作边界：绝不编造用户位置、扣积分/下单/领券一律
          先确认、券只报实测口径不虚报资产、记忆只读不猜。
```

4. **10 月 25 日 23:59 前**提交

---

## 八、拿 Star：从提交到截止只剩 5 天

排名 = GitHub 公开 Star 数，这是唯一可量化的指标。可做的事：

| 动作 | 说明 |
| --- | --- |
| **发一条技术向分享** | 掘金/知乎/公众号/CSDN，写「用 MCP + Skill 做盲盒，踩了 5 个坑」，附仓库链接。**不要发"求 Star"的水贴**，技术贴带自然流量 |
| **加 README 首屏截图/动图** | 一张盲盒文案截图就够，让人 3 秒看懂这是什么 |
| **Twitter/X + 掘金双发** | 程序员社区流量池 |
| **社群分享** | MCP 相关开发者群、WorkBuddy 用户群 |
| **写 Issue 记录 bug** | 给 `MCP_BUG_REPORT.md` 的 3 个问题提 Issue，让接口方和开发者看到你的项目 |

### 建议给 README 加的第一屏内容

- 一张开盒输出的真实截图（**记得打码**，别露出券 ID、门店全名、手机号）
- 一句话定位：**「说一句话就出餐，AI 自己定位、自己抽签、自己给惊喜——但绝不编造你的位置，绝不擅自扣你的积分」**
- 3 个徽章：WorkBuddy / MCP / 1024 程序员节

### 已备好的推广物料

| 文件 | 用途 |
| --- | --- |
| `BLOG_ARTICLE.md` | 完整版技术长文，约 6800 字，掘金/知乎首发 |
| `BLOG_SHORTS.md` | 短版：①技术社区长贴（1200 字）②社交媒体短贴（200 字）③标题三选一 + 发布清单 |

⚠️ **发布前必改**：两处文件共 5 个 `https://github.com/<你的用户名>/<仓库名>` 占位符，务必全部替换成真实仓库地址。

两篇文章都保留了你的两句原话（"这是大模型没有 GPS 导致的幻觉"、"我觉得规则的优先权应该是 3、2、1"）——**别改成自己的话**，这两句是文章真实感的来源。

---

## 九、提交前最终清单

- [x] `workbuddy.md` 已导出并放入 `mcd-blind-box/`
- [ ] `.env` 已移出项目目录 或 内容已清空（**唯一必做的手动动作**）
- [x] `python check_submission.py` 全绿
- [ ] `git status` 确认无 `.env` / 废弃配置
- [ ] 仓库设为 **Public**
- [ ] README 首屏有截图和一句话定位
- [ ] Issue 模板已填好，**10-25 23:59 前**提交
- [ ] `BLOG_ARTICLE.md` / `BLOG_SHORTS.md` 的 5 处仓库地址占位符已替换
- [ ] 已在掘金/知乎发过带链接的技术贴

---

## 十、已修复的同步问题（记录备查）

开发过程中项目级 `.workbuddy/skills/` 副本与用户级生效版本曾出现不同步：

| 文件 | 问题 | 已处理 |
| --- | --- | --- |
| `SKILL.md` | 项目级是旧版（Token 铁律仍写「只从环境变量读取」） | 已用用户级最新版覆盖 |
| `memory.json` | 项目级只有 4 盒记录，用户级已到 6 盒 | 已同步为 6 盒版本 |

`check_submission.py` 的第 5 项检查就是为此加的——**提交的是项目级副本，它才是评委看到的东西**。
