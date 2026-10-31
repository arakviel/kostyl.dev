# Візуалізації для лекції 14: Sequence-to-Sequence і Attention

Скрипти для генерації картинок до лекції "Encoder-decoder, bottleneck problem, attention mechanism, Q/K/V".

## Картинки

1. **encoder-decoder-basic.png** — Базова encoder-decoder архітектура (без attention)
2. **bottleneck-problem.png** — Проблема вузького місця: вся інформація в одному векторі c
3. **attention-architecture.png** — Seq2Seq з attention: decoder має доступ до всіх h_i
4. **attention-heatmap.png** — Теплова карта attention weights (англійська → українська)
5. **qkv-illustration.png** — Query-Key-Value концепція: аналогія зі словником

## Як запустити

```bash
cd /Users/arakviel/Work/kostyl.dev
python3 tools/figures/16.ai-python/16.natural-language-processing/14.seq2seq-attention/encoder-decoder-basic.py
python3 tools/figures/16.ai-python/16.natural-language-processing/14.seq2seq-attention/bottleneck-problem.py
python3 tools/figures/16.ai-python/16.natural-language-processing/14.seq2seq-attention/attention-architecture.py
python3 tools/figures/16.ai-python/16.natural-language-processing/14.seq2seq-attention/attention-heatmap.py
python3 tools/figures/16.ai-python/16.natural-language-processing/14.seq2seq-attention/qkv-illustration.py
```

Усі PNG зберігаються в `public/images/16.ai-python/16.natural-language-processing/14.seq2seq-attention/`
