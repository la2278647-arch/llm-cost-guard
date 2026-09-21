# llm-cost-guard 宣传物料包（Promotion Kit）

仓库：https://github.com/la2278647-arch/llm-cost-guard

> 使用说明：以下文案按平台定制。需要你登录对应账号后发布（我没有各平台账号凭据，无法代发）。

---

## Hacker News (Show HN)

**Title:** Show HN: llm-cost-guard – zero-dependency CLI to track and budget LLM API spending

**Body:**
I kept getting surprised by my LLM API bills, so I built a tiny zero-dependency (stdlib-only) Python tool that logs every call's token usage into a local SQLite file, prices it against a built-in table (OpenAI/Anthropic/DeepSeek), and can hard-fail your cron/CI when you exceed a daily/weekly/monthly budget.

- `lcg log --model gpt-4o-mini --input-tokens 1200 --output-tokens 300`
- `lcg report --by model` / `--by day` / `--json`
- `lcg budget set --monthly 50 && lcg budget check` (exit code 2 when over)

Data never leaves your machine. Feedback welcome — especially on the price table and what integrations (SDK wrappers, Slack alerts) you'd want next.

---

## Reddit r/LocalLLaMA / r/OpenAI / r/Python

**Title:** I built a zero-dependency tool to stop surprise LLM API bills (track + budget + alert, all local)

**Body:**（同 HN，补充）How do you all track spend across providers? I was juggling OpenAI + DeepSeek + Anthropic bills and nothing lightweight existed that doesn't require a hosted dashboard or sending my usage data somewhere. This is just a SQLite file + a CLI.

---

## V2EX / 掘金 / 知乎（中文）

**标题：** 开源了一个 LLM API 费用管家：零依赖、全本地，超预算直接让 CI 挂掉

**正文：**
大模型 API 账单失控是家常便饭。llm-cost-guard 只用 Python 标准库，把每次调用的 token 记进本地 SQLite，按内置价格表（OpenAI/Anthropic/DeepSeek）自动算钱，支持日/周/月预算，超了退出码直接非零——丢进 cron 或 CI 就能硬拦截。数据不出本机。
求 star 求拍砖： https://github.com/la2278647-arch/llm-cost-guard

---

## Twitter / X

Built a tiny zero-dep tool to stop surprise LLM bills 💸
`lcg log` → local SQLite → `lcg budget check` exits non-zero when you're over budget. OpenAI/Anthropic/DeepSeek price table built in. Your usage data never leaves your machine.
https://github.com/la2278647-arch/llm-cost-guard #LLM #OpenSource

---

## 发布清单（勾选）

- [ ] Hacker News — Show HN（美东上午 8-10 点发布效果最佳）
- [ ] Reddit r/Python、r/OpenAI、r/LocalLLaMA
- [ ] V2EX 分享创造节点
- [ ] 掘金 / 知乎专栏文章（可展开写教程）
- [ ] Twitter / X
- [ ] Product Hunt（需准备图标和截图，可第二轮做）
- [ ] 提交到 awesome-llm / awesome-ai-tools 等列表（发 PR）
