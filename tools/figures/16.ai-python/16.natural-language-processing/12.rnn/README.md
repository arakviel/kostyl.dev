# Візуалізації для лекції 12: RNN

Скрипти для генерації картинок до лекції "Рекурентні нейронні мережі".

## Картинки

1. **rnn-unfolding.png** — Схема RNN: згорнута форма (з петлею) і розгорнута в часі
2. **rnn-vs-average.png** — Графіки loss і accuracy: RNN vs усереднення embeddings на IMDB
3. **vanishing-gradient.png** — Зникнення градієнта: ||∂L/∂h_t|| від кроку t
4. **hidden-state-trajectory.png** — Траєкторія прихованого стану h_t в 2D (PCA проєкція)

## Як запустити

```bash
cd /Users/arakviel/Work/kostyl.dev
python3 tools/figures/16.ai-python/16.natural-language-processing/12.rnn/rnn-unfolding.py
python3 tools/figures/16.ai-python/16.natural-language-processing/12.rnn/rnn-vs-average.py
python3 tools/figures/16.ai-python/16.natural-language-processing/12.rnn/vanishing-gradient.py
python3 tools/figures/16.ai-python/16.natural-language-processing/12.rnn/hidden-state-trajectory.py
```

Усі PNG зберігаються в `public/images/16.ai-python/16.natural-language-processing/12.rnn/`
