# llm-cost-guard

**Track, budget, and control your LLM API spending — across OpenAI, Anthropic, DeepSeek, and any OpenAI-compatible provider.**

大模型 API 费用失控是 2025 年团队最常见的痛点之一：谁也不知道这个月烧了多少 token、哪个服务最贵、什么时候会超预算。`llm-cost-guard` 是一个零依赖（仅标准库）的 Python 工具，帮你：

- 📊 **记录** 每次调用的 token 用量与成本（本地 SQLite，无需任何服务）
- 💰 **自动计价**：内置主流模型价格表，支持自定义价格
- 🚨 **预算告警**：按日/周/月设预算，超额即报错退出（可直接接入 CI / cron）
- 📈 **报表**：按模型、按天、按标签聚合统计，输出表格或 JSON
- 🔌 **易集成**：三行代码包装任意调用，或直接用 CLI 记账

## 安装

```bash
pip install llm-cost-guard        # PyPI（发布后）
# 或者本地开发：
pip install -e .
```

## 快速开始

### CLI

```bash
# 记一笔：gpt-4o-mini 输入 1200 token，输出 300 token
lcg log --model gpt-4o-mini --input-tokens 1200 --output-tokens 300 --tag chatbot

# 查看报表
lcg report                    # 汇总表
lcg report --by day           # 按天
lcg report --by model --json  # JSON 输出

# 预算：本月预算 50 美元，超额退出码为 2（适合 cron/CI）
lcg budget set --monthly 50
lcg budget check              # 超预算时 exit 2

# 查看/添加价格表
lcg prices
lcg prices add my-finetune --input 0.5 --output 1.5   # 每百万 token 美元价
```

### Python API

```python
from llm_cost_guard import Tracker, price_of

tracker = Tracker()  # 默认存 ~/.llm-cost-guard/ledger.db

# 手动记录
cost = tracker.log(model="gpt-4o-mini", input_tokens=1200, output_tokens=300, tag="chatbot")

# 预算检查（超预算抛 BudgetExceeded）
tracker.check_budget(monthly_usd=50)
```

## 内置价格表（每百万 token，美元）

价格存于 `llm_cost_guard/pricing.py`，含 OpenAI / Anthropic / DeepSeek 主流模型，可随时用 `lcg prices add` 覆盖或扩展。价格以官方页面为准，使用前请核对。

## 数据在哪？

全部存本地 SQLite：`~/.llm-cost-guard/ledger.db`（可用 `--db` 或环境变量 `LCG_DB` 指定）。你的用量数据从不离开你的机器。

## 路线图

- [ ] OpenAI / Anthropic SDK 自动拦截包装器
- [ ] 团队模式：共享数据库 + 按 API key 归属
- [ ] Web Dashboard（可选组件）
- [ ] Slack / 邮件超预算通知

## 贡献

欢迎 PR！价格表更新、新 provider 适配、报表格式都是很好的入门贡献点。

## License

MIT
