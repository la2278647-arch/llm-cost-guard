# Contributing to llm-cost-guard

感谢你的兴趣！以下是很好的入门贡献点：

## 价格表更新（最简单的 PR）
模型价格经常变。修改 `llm_cost_guard/pricing.py`，PR 标题格式：`pricing: update gpt-4o price (source: <官方页面链接>)`。

## 新 Provider 价格
在 `PRICES` 字典加前缀条目即可，附官方价格页链接。

## 开发

```bash
git clone https://github.com/la2278647-arch/llm-cost-guard
cd llm-cost-guard
python -m unittest discover -s tests -v   # 必须通过
```

约束：**核心库保持零第三方依赖（仅标准库）**。可选集成（如 `instrument.py`）必须懒加载、SDK 缺失时不报错。

## 代码风格
- Python ≥ 3.9 兼容
- 无格式化器强制要求，保持与现有代码一致即可

## 提交信息
`feat:` / `fix:` / `docs:` / `pricing:` 前缀。
