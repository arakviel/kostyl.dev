# Візуалізації для лекції 13: LSTM і GRU

Скрипти для генерації картинок до лекції "Long Short-Term Memory і Gated Recurrent Unit".

## Картинки

1. **lstm-architecture.png** — Схема LSTM з вентилями (forget, input, output) і cell state
2. **gradient-flow.png** — Порівняння потоку градієнтів: RNN (зникають) vs LSTM (зберігаються)
3. **gru-architecture.png** — Схема GRU з reset і update gates
4. **comparison-accuracy.png** — Порівняння RNN/LSTM/GRU: accuracy, параметри, час
5. **gates-heatmap.png** — Heatmap активації вентилів LSTM для речення

## Як запустити

```bash
cd /Users/arakviel/Work/kostyl.dev
python3 tools/figures/16.ai-python/16.natural-language-processing/13.lstm-gru/lstm-architecture.py
python3 tools/figures/16.ai-python/16.natural-language-processing/13.lstm-gru/gradient-flow.py
python3 tools/figures/16.ai-python/16.natural-language-processing/13.lstm-gru/gru-architecture.py
python3 tools/figures/16.ai-python/16.natural-language-processing/13.lstm-gru/comparison-accuracy.py
python3 tools/figures/16.ai-python/16.natural-language-processing/13.lstm-gru/gates-heatmap.py
```

Усі PNG зберігаються в `public/images/16.ai-python/16.natural-language-processing/13.lstm-gru/`
