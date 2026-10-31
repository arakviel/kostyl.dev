# План модуля 6 «Обробка природної мови» (папка `content/16.ai-python/16.natural-language-processing/`)

Джерело: `temp/ai-python-course-plan.md`, Модуль 6 (статті 6.1–6.3). Тут вони розбиті на 16 лекцій.
Правила: `.agents/skills/college-lectures/SKILL.md`, компоненти з `DOCUS_COMPONENTS.md` (без mermaid).

## Робочі правила

- Файл пишеться частинами по ~150 рядків. Кожна лекція ≈ 450–700 рядків.
- Frontmatter `title` + `description`; далі `# Заголовок`, картки «Мета» і «Ключові терміни», `---`. Без нумерації в заголовках.
- Код — `::jupyter-notebook`/`::jupyter-cell`; усі виводи з реальних запусків (фіксоване зерно, версії бібліотек).
- Формули — `::math-formula`. Практика у `::::accordion` (завдання + розв'язок). Закінчення: картки «Підсумок» і «Що далі».
- Картинки: matplotlib. Скрипт `tools/figures/ai-python/natural-language-processing/<урок>/NN-назва.py` → `public/images/ai-python/natural-language-processing/<урок>/NN-назва.png`. Запуск: `uv run --python 3.13 --with matplotlib python <скрипт>`. Вставка: `![підпис](/images/...){.diagram-img}`.
- Відео: тільки слоти (коментар `<!-- VIDEO ... -->` за форматом `temp/cnn-media-slots.md`), самі ролики не робимо. Повний перелік слотів — у `temp/nlp-media-slots.md`.
- PlantUML лише для послідовностей і класів.

## Що студент уже знає (можна використовувати)

nn.Linear, softmax, CrossEntropy, Adam, Dataset/DataLoader, Dropout, LayerNorm, residual, зникнення градієнта, `clip_grad_norm_`, transfer learning (5.3), precision/recall/F1, `train_test_split`, LogisticRegression, one-hot для таблиць, кореляція, pandas, matplotlib.

## Що НЕ можна випереджати

PCA/SVD, кластеризація, TF-IDF, рекомендаційні системи (Модуль 7); LLM як продукт, temperature, context window, Ollama, OpenAI API, хмарні сервіси (Модуль 8). Косинусна подібність вводиться в лекції 07 (7.3 лише нагадає).

## Рішення, прийняті разом із користувачем

16 файлів; українська мова розділами в лекціях 02–04; PCA лише як «чорна скринька» з приміткою; основний датасет англійський (`nltk movie_reviews`, потім IMDB), український — окремі розділи; `index.md` модуля є.

## Лекції

| # | Файл | Зміст | Картинки (matplotlib) |
|---|---|---|---|
| 00 | `index.md` | Мета модуля, карта «текст → числа → модель», структура | карта модуля |
| 01 | `01.text-as-data.md` | Чому текст складний; задачі NLP; рядок, Unicode, байти; конвеєр | задачі NLP, омоніми, UTF-8 байти, конвеєр |
| 02 | `02.tokenization.md` | Нормалізація, `re`, `word_tokenize`/`sent_tokenize`; пастки; українська | розбиття речення, порівняння токенізаторів |
| 03 | `03.stemming-lemmatization-stopwords.md` | Стеммінг, лемматизація, стоп-слова; українська (`pymorphy3`) | схема стем/лема, таблиця помилок, до/після стоп-слів |
| 04 | `04.corpus-and-frequency.md` | Корпус, частоти, закон Ципфа, bar-plot | топ-слова, Ципф (лог-лог), розмір корпусу |
| 05 | `05.bag-of-words.md` | Словник, мішок слів, розрідженість, втрата порядку | матриця документ×слово, розрідженість, два речення з однаковим мішком |
| 06 | `06.text-classification-baseline.md` | LogisticRegression на мішку слів, метрики, найвагоміші слова | матриця помилок, ваги слів, крива якості від розміру словника |
| 07 | `07.from-one-hot-to-embeddings.md` | One-hot проти щільних векторів, `nn.Embedding`, косинусна подібність | відстані one-hot, 2D-іграшкові вектори, косинус як кут, lookup-таблиця |
| 08 | `08.word2vec.md` | Контекст, CBOW, skip-gram, `gensim` | вікно контексту, пари skip-gram, схема мережі, динаміка loss |
| 09 | `09.glove-pretrained-embeddings.md` | GloVe, найближчі слова, аналогії, упередження, 2D-проєкція | матриця co-occurrence, проєкція слів, аналогія-паралелограм |
| 10 | `10.embeddings-for-classification.md` | Вектор речення = середнє; класифікатор; порівняння з еталоном | усереднення векторів, порівняння якості підходів |
| 11 | `11.language-models-and-sequences.md` | Мовна модель, біграми, послідовності, padding, `collate_fn` | таблиця ймовірностей, padding-батч, розподіл довжин |
| 12 | `12.rnn.md` | Прихований стан, розгортання, `nn.RNN`, класифікація | розгорнута RNN, траєкторія стану, loss/acc |
| 13 | `13.lstm.md` | Згасання/вибух у часі, ворота LSTM, `nn.LSTM` | множення Jacobian у часі, схема LSTM, RNN vs LSTM на довгих текстах |
| 14 | `14.attention.md` | Вузьке місце, увага, Q/K/V на числах | seq2seq bottleneck, теплова карта уваги, Q·K |
| 15 | `15.transformer.md` | Self-attention, multi-head, positional encoding, блок | матриця уваги, positional encoding, блок, encoder/decoder |
| 16 | `16.pretrained-models-sentiment.md` | Hugging Face, підслова, `pipeline`, дотренування, підсумок | підслова, порівняння трьох підходів, підсумкова таблиця |

## Контроль випередження (перевіряти на кожній лекції)

01–06 без жодного вектора слова; 07–10 без послідовностей; 11–13 без уваги; 14–15 без HF; 16 без LLM-термінів з Модуля 8.
