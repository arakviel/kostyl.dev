# Формат слотів для медіа (модуль 15)

Кожен слот — HTML-коментар у місці статті, де відео/картинка потрібні. Стаття має читатися повністю і без них.
Слоти не рендеряться. Після виготовлення ролика коментар замінюється на `::video-player`.

```md
<!-- VIDEO
id: why-conv-01-shift-breaks-dense
file: /videos/ai-python/cnn-image-classification/why-convolution/shift-breaks-dense.mp4
poster: /images/ai-python/cnn-image-classification/why-convolution/shift-breaks-dense-poster.jpg
duration: 30-40s
one-thing: одна думка, яку глядач має винести
viewer: хто дивиться і що вже знає
example: який конкретний приклад/числа з тексту статті проходять крізь ролик (мають збігатися зі статтею!)
beats: hook → tension → reveal → proof → payoff → claim
on-screen: ключові числа, підписи, формули (дослівно)
vo: текст озвучки українською (1-3 речення на біт)
look: палітра/шрифти (за замовчуванням: #070b14, cyan/emerald/amber, Inter + JetBrains Mono)
depends-on: статичні картинки зі статті, які ролик відтворює
-->
```

Для картинок:

```md
<!-- IMAGE id: ... file: .../NN.png | що показує | звідки дані -->
```
