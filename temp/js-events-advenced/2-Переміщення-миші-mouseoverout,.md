Давайте детальніше розглянемо події, які відбуваються, коли вказівник миші переміщається між елементами.

## [Події mouseover/mouseout, relatedTarget](https://uk.javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave#podiyi-mouseover-mouseout-relatedtarget)

Подія `mouseover` виникає, коли вказівник миші наводиться на елемент, а `mouseout` – коли залишає його.

Ці події особливі, оскільки мають властивість `relatedTarget`. Ця властивість доповнює `target`. Коли миша йде від одного елемента до іншого, один з них стає `target`, а інший – `relatedTarget`.

Для `mouseover`:

-   `event.target` – це елемент, на який наведено вказівник миші.
-   `event.relatedTarget` – це елемент, з якого прийшов вказіник (`relatedTarget` → `target`).

Для `mouseout` навпаки:

-   `event.target` – це елемент, який залишила миша.
-   `event.relatedTarget` – це новий елемент під вказівником, на який перейшла миша (`target` → `relatedTarget`).

У наведеному нижче прикладі кожне обличчя та його риси є окремими елементами. Коли ви рухаєте мишею, події миші відображаються в текстовій області.

Кожна подія містить інформацію як про `target`, так і про `relatedTarget`:

Результат

script.js

style.css

index.html

```
container.onmouseover = container.onmouseout = handler;

function handler(event) {

  function str(el) {
    if (!el) return "null"
    return el.className || el.tagName;
  }

  log.value += event.type + ':  ' +
    'target=' + str(event.target) +
    ',  relatedTarget=' + str(event.relatedTarget) + "\n";
  log.scrollTop = log.scrollHeight;

  if (event.type == 'mouseover') {
    event.target.style.background = 'pink'
  }
  if (event.type == 'mouseout') {
    event.target.style.background = ''
  }
}
```

```
body,
html {
  margin: 0;
  padding: 0;
}

#container {
  border: 1px solid brown;
  padding: 10px;
  width: 330px;
  margin-bottom: 5px;
  box-sizing: border-box;
}

#log {
  height: 120px;
  width: 350px;
  display: block;
  box-sizing: border-box;
}

[class^="smiley-"] {
  display: inline-block;
  width: 70px;
  height: 70px;
  border-radius: 50%;
  margin-right: 20px;
}

.smiley-green {
  background: #a9db7a;
  border: 5px solid #92c563;
  position: relative;
}

.smiley-green .left-eye {
  width: 18%;
  height: 18%;
  background: #84b458;
  position: relative;
  top: 29%;
  left: 22%;
  border-radius: 50%;
  float: left;
}

.smiley-green .right-eye {
  width: 18%;
  height: 18%;
  border-radius: 50%;
  position: relative;
  background: #84b458;
  top: 29%;
  right: 22%;
  float: right;
}

.smiley-green .smile {
  position: absolute;
  top: 67%;
  left: 16.5%;
  width: 70%;
  height: 20%;
  overflow: hidden;
}

.smiley-green .smile:after,
.smiley-green .smile:before {
  content: "";
  position: absolute;
  top: -50%;
  left: 0%;
  border-radius: 50%;
  background: #84b458;
  height: 100%;
  width: 97%;
}

.smiley-green .smile:after {
  background: #84b458;
  height: 80%;
  top: -40%;
  left: 0%;
}

.smiley-yellow {
  background: #eed16a;
  border: 5px solid #dbae51;
  position: relative;
}

.smiley-yellow .left-eye {
  width: 18%;
  height: 18%;
  background: #dba652;
  position: relative;
  top: 29%;
  left: 22%;
  border-radius: 50%;
  float: left;
}

.smiley-yellow .right-eye {
  width: 18%;
  height: 18%;
  border-radius: 50%;
  position: relative;
  background: #dba652;
  top: 29%;
  right: 22%;
  float: right;
}

.smiley-yellow .smile {
  position: absolute;
  top: 67%;
  left: 19%;
  width: 65%;
  height: 14%;
  background: #dba652;
  overflow: hidden;
  border-radius: 8px;
}

.smiley-red {
  background: #ee9295;
  border: 5px solid #e27378;
  position: relative;
}

.smiley-red .left-eye {
  width: 18%;
  height: 18%;
  background: #d96065;
  position: relative;
  top: 29%;
  left: 22%;
  border-radius: 50%;
  float: left;
}

.smiley-red .right-eye {
  width: 18%;
  height: 18%;
  border-radius: 50%;
  position: relative;
  background: #d96065;
  top: 29%;
  right: 22%;
  float: right;
}

.smiley-red .smile {
  position: absolute;
  top: 57%;
  left: 16.5%;
  width: 70%;
  height: 20%;
  overflow: hidden;
}

.smiley-red .smile:after,
.smiley-red .smile:before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0%;
  border-radius: 50%;
  background: #d96065;
  height: 100%;
  width: 97%;
}

.smiley-red .smile:after {
  background: #d96065;
  height: 80%;
  top: 60%;
  left: 0%;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <div id="container">
    <div class="smiley-green">
      <div class="left-eye"></div>
      <div class="right-eye"></div>
      <div class="smile"></div>
    </div>

    <div class="smiley-yellow">
      <div class="left-eye"></div>
      <div class="right-eye"></div>
      <div class="smile"></div>
    </div>

    <div class="smiley-red">
      <div class="left-eye"></div>
      <div class="right-eye"></div>
      <div class="smile"></div>
    </div>
  </div>

  <textarea id="log">Events will show up here!
</textarea>

  <script src="script.js"></script>

</body>
</html>
```

`relatedTarget` може бути `null`

Властивість `relatedTarget` може мати значення `null`.

Це нормально і просто означає, що вказівник миші прийшов не з іншого елемента, а десь з поза меж вікна. Або навпаки, що вказівник вийшов за межі вікна браузера.

Нам варто пам’ятати про цю можливість, використовуючи `event.relatedTarget` в коді. Бо якщо спробувати отримати доступ до `event.relatedTarget.tagName`, то виникне помилка.

## [Пропуск елементів](https://uk.javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave#propusk-elementiv)

Подія `mousemove` запускається, коли миша рухається. Але це не означає, що кожен навіть найменший рух веде до окремої події.

Час від часу браузер перевіряє положення миші. І якщо він помічає зміни, то ініціює події.

Ба більше, якщо користувач рухає мишею дуже швидко, деякі DOM-елементи можуть бути пропущені:

Якщо миша дуже швидко рухається від елементів `#FROM` до `#TO`, як зазначено вище, то проміжні елементи `<div>` (або деякі з них) можуть бути пропущені. Подія `mouseout` може бути ініційована на `#FROM`, а потім одразу `mouseover`на `#TO`.

Це добре для продуктивності, бо може бути багато проміжних елементів. Ми насправді не хочемо обробляти кожен із них.

З іншого боку, ми повинні мати на увазі, що вказівник миші не “відвідує” всі елементи на шляху і може “стрибати”.

Зокрема, можливо, що вказівник стрибне прямо всередину сторінки з поза меж вікна. У цьому випадку `relatedTarget` має значення `null`, тому що він прийшов “нізвідки”:

Ви можете перевірити це на тестовому стенді нижче.

Його HTML має два вкладені елементи: `<div id="child">` знаходиться всередині `<div id="parent">`. Якщо ви швидко наведете на них мишу, то, можливо, лише дочірній div ініціює події, або батьківський, або навіть подій не буде взагалі.

Також перемістіть вказівник у дочірній `div`, а потім швидко перемістіть його вниз через батьківський. Якщо рух досить швидкий, то батьківський елемент ігнорується. Миша перетне батьківський елемент, не помітивши цього.

Результат

script.js

style.css

index.html

```
let parent = document.getElementById('parent');
parent.onmouseover = parent.onmouseout = parent.onmousemove = handler;

function handler(event) {
  let type = event.type;
  while (type.length < 11) type += ' ';

  log(type + " target=" + event.target.id)
  return false;
}


function clearText() {
  text.value = "";
  lastMessage = "";
}

let lastMessageTime = 0;
let lastMessage = "";
let repeatCounter = 1;

function log(message) {
  if (lastMessageTime == 0) lastMessageTime = new Date();

  let time = new Date();

  if (time - lastMessageTime > 500) {
    message = '------------------------------\n' + message;
  }

  if (message === lastMessage) {
    repeatCounter++;
    if (repeatCounter == 2) {
      text.value = text.value.trim() + ' x 2\n';
    } else {
      text.value = text.value.slice(0, text.value.lastIndexOf('x') + 1) + repeatCounter + "\n";
    }

  } else {
    repeatCounter = 1;
    text.value += message + "\n";
  }

  text.scrollTop = text.scrollHeight;

  lastMessageTime = time;
  lastMessage = message;
}
```

```
#parent {
  background: #99C0C3;
  width: 160px;
  height: 120px;
  position: relative;
}

#child {
  background: #FFDE99;
  width: 50%;
  height: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

textarea {
  height: 140px;
  width: 300px;
  display: block;
}
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <div id="parent">parent
    <div id="child">child</div>
  </div>
  <textarea id="text"></textarea>
  <input onclick="clearText()" value="Clear" type="button">

  <script src="script.js"></script>

</body>

</html>
```

Якщо спрацьовує `mouseover`, обов’язково буде `mouseout`

У разі швидких рухів миші проміжні елементи можуть ігноруватися, але одне ми знаємо напевно: якщо вказівник “офіційно” увійшов на елемент (генерується подія `mouseover`), то при виході з нього ми завжди отримуємо `mouseout`.

## [Mouseout при переході на дочірній елемент](https://uk.javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave#mouseout-pri-perekhodi-na-dochirnii-element)

Важлива функція події `mouseout` – вона запускається, коли вказівник переміщується від елемента до його нащадка, наприклад, від `#parent` до `#child` у HTML нижче:

```markup
<div id="parent">
  <div id="child">...</div>
</div>
```

Якщо ми знаходимося на `#parent`, а потім переміщуємо вказівник глибше в `#child`, ми отримуємо `mouseout` на `#parent`!

Це може здатися дивним, але це легко пояснити.

**Відповідно до логіки браузера, вказівник миші може бути лише над _одним_ елементом у будь-який момент часу – найбільш вкладеним і верхнім за z-індексом.**

Отже, якщо він переходить до іншого елемента (навіть до нащадка), то він залишає попередній.

Зверніть увагу на ще одну важливу деталь обробки подій.

Подія `mouseover` на нащадку буде спливати. Отже, якщо `#parent` має обробник `mouseover`, він спрацює:

Ви можете це добре побачити в прикладі нижче: `<div id="child">` знаходиться всередині `<div id="parent">`. І обробники `mouseover/out` для елементу `#parent` виведуть деталі події.

Якщо ви перемістите вказівник миші від `#parent` до `#child`, це викличе дві події на `#parent`:

1.  `mouseout [target: parent]` (вказівник залишив parent), далі
2.  `mouseover [target: child]` (дійшов до child, спливання події).

Результат

script.js

style.css

index.html

```
function mouselog(event) {
  let d = new Date();
  text.value += `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()} | ${event.type} [target: ${event.target.id}]\n`.replace(/(:|^)(\d\D)/, '$10$2');
  text.scrollTop = text.scrollHeight;
}
```

```
#parent {
  background: #99C0C3;
  width: 160px;
  height: 120px;
  position: relative;
}

#child {
  background: #FFDE99;
  width: 50%;
  height: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

textarea {
  height: 140px;
  width: 300px;
  display: block;
}
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <div id="parent" onmouseover="mouselog(event)" onmouseout="mouselog(event)">parent
    <div id="child">child</div>
  </div>

  <textarea id="text"></textarea>
  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>

</html>
```

Як показано, коли вказівник переміщується від елемента `#parent` до `#child`, на батьківському елементі запускаються два обробники: `mouseout` і `mouseover`:

```javascript
parent.onmouseout = function(event) {
  /* event.target: parent елемент */
};
parent.onmouseover = function(event) {
  /* event.target: child елемент (спливання) */
};
```

**Якщо ми не перевіримо `event.target` всередині обробників, то може здатися, що вказівник миші залишив елемент `#parent`, а потім одразу повернувся на нього.**

Але це не так! Вказівник все ще знаходиться над батьківським елементом, він просто перемістився глибше на дочірній елемент.

Якщо є якісь дії після виходу з батьківського елемента, напр. анімація запускається в `parent.onmouseout`, ми зазвичай не хочемо цього, коли вказівник просто йде глибше в `#parent`.

Щоб уникнути цього, ми можемо перевірити `relatedTarget` в обробнику і, якщо вказівник все ще всередині елемента, ігнорувати цю подію.

Як альтернативу ми можемо використовувати інші події: `mouseenter` і `mouseleave`, які ми зараз розглянемо, оскільки вони не мають таких проблем.

## [Події mouseenter і mouseleave](https://uk.javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave#podiyi-mouseenter-i-mouseleave)

Події `mouseenter/mouseleave` схожі на `mouseover/mouseout`. Вони спрацьовують, коли вказівник миші входить або залишає елемент.

Але є дві важливі відмінності:

1.  Переходи всередині елемента до/від нащадків не враховуються.
2.  Події `mouseenter/mouseleave` не спливають.

Ці події надзвичайно прості.

Коли вказівник входить на елемент, спрацьовує `mouseenter`. Точне розташування вказівника всередині елемента або його нащадків не має значення.

Коли вказівник залишає елемент, спрацьовує `mouseleave`.

Цей приклад подібний до наведеного вище, але тепер у верхньому елементі є `mouseenter/mouseleave` замість `mouseover/mouseout`.

Як бачите, єдині генеровані події пов’язані з переміщенням вказівника в верхній елемент і з нього. Нічого не відбувається, коли вказівник йде до дочірнього елемента і назад. Переходи між нащадками ігноруються

Результат

script.js

style.css

index.html

```
function mouselog(event) {
  let d = new Date();
  text.value += `${d.getHours()}:${d.getMinutes()}:${d.getSeconds()} | ${event.type} [target: ${event.target.id}]\n`.replace(/(:|^)(\d\D)/, '$10$2');
  text.scrollTop = text.scrollHeight;
}
```

```
#parent {
  background: #99C0C3;
  width: 160px;
  height: 120px;
  position: relative;
}

#child {
  background: #FFDE99;
  width: 50%;
  height: 50%;
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

textarea {
  height: 140px;
  width: 300px;
  display: block;
}
```

```
<!doctype html>
<html>

<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>

  <div id="parent" onmouseenter="mouselog(event)" onmouseleave="mouselog(event)">parent
    <div id="child">child</div>
  </div>

  <textarea id="text"></textarea>
  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>

</html>
```

## [Делегування подій (Event delegation)](https://uk.javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave#deleguvannya-podii-event-delegation)

Події `mouseenter/leave` дуже прості та легкі у використанні. Але вони не спливають. Тому ми не можемо використовувати з ними делегування подій (event delegation).

Уявіть, що ми хочемо керувати входом/виходом вказівника миші для клітинок таблиці, в якій сотні клітин.

Ефективним рішенням було б встановити обробник на `<table>` і обробляти події там. Але `mouseenter/leave` не спливають. Отже, якщо така подія відбувається на `<td>`, то лише обробник на цьому `<td>` може її перехопити.

Обробники для `mouseenter/leave` на `<table>` запускаються лише тоді, коли вказівник входить/виходить із таблиці в цілому. Інформацію про переходи всередині нього отримати неможливо.

Отже, давайте використаємо `mouseover/mouseout`.

Почнемо з простих обробників, які підсвічують елемент під вказівником миші:

```javascript
// виділимо елемент під вказівником
table.onmouseover = function(event) {
  let target = event.target;
  target.style.background = 'pink';
};

table.onmouseout = function(event) {
  let target = event.target;
  target.style.background = '';
};
```

Ось вони в дії. Коли миша переміщається по елементах цієї таблиці, поточний виділяється:

Результат

script.js

style.css

index.html

```
table.onmouseover = function(event) {
  let target = event.target;
  target.style.background = 'pink';

  text.value += `over -> ${target.tagName}\n`;
  text.scrollTop = text.scrollHeight;
};

table.onmouseout = function(event) {
  let target = event.target;
  target.style.background = '';

  text.value += `out <- ${target.tagName}\n`;
  text.scrollTop = text.scrollHeight;
};
```

```
#text {
  display: block;
  height: 100px;
  width: 456px;
}

#table th {
  text-align: center;
  font-weight: bold;
}

#table td {
  width: 150px;
  white-space: nowrap;
  text-align: center;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 12px;
  cursor: pointer;
}

#table .nw {
  background: #999;
}

#table .n {
  background: #03f;
  color: #fff;
}

#table .ne {
  background: #ff6;
}

#table .w {
  background: #ff0;
}

#table .c {
  background: #60c;
  color: #fff;
}

#table .e {
  background: #09f;
  color: #fff;
}

#table .sw {
  background: #963;
  color: #fff;
}

#table .s {
  background: #f60;
  color: #fff;
}

#table .se {
  background: #0c3;
  color: #fff;
}

#table .highlight {
  background: red;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>


  <table id="table">
    <tr>
      <th colspan="3"><em>Bagua</em> Chart: Direction, Element, Color, Meaning</th>
    </tr>
    <tr>
      <td class="nw"><strong>Northwest</strong>
        <br>Metal
        <br>Silver
        <br>Elders
      </td>
      <td class="n"><strong>North</strong>
        <br>Water
        <br>Blue
        <br>Change
      </td>
      <td class="ne"><strong>Northeast</strong>
        <br>Earth
        <br>Yellow
        <br>Direction
      </td>
    </tr>
    <tr>
      <td class="w"><strong>West</strong>
        <br>Metal
        <br>Gold
        <br>Youth
      </td>
      <td class="c"><strong>Center</strong>
        <br>All
        <br>Purple
        <br>Harmony
      </td>
      <td class="e"><strong>East</strong>
        <br>Wood
        <br>Blue
        <br>Future
      </td>
    </tr>
    <tr>
      <td class="sw"><strong>Southwest</strong>
        <br>Earth
        <br>Brown
        <br>Tranquility
      </td>
      <td class="s"><strong>South</strong>
        <br>Fire
        <br>Orange
        <br>Fame
      </td>
      <td class="se"><strong>Southeast</strong>
        <br>Wood
        <br>Green
        <br>Romance
      </td>
    </tr>

  </table>

  <textarea id="text"></textarea>

  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>
</html>
```

У нашому випадку ми хочемо обробляти переходи між клітинами таблиці `<td>`: вхід у клітину та вихід з неї. Інші переходи, як всередині клітини або за її межами, нас не цікавлять. Відфільтруємо їх.

Ось що ми можемо зробити:

-   Запам’ятайте поточний виділений `<td>` у змінній, назвемо її `currentElem`.
-   При `mouseover` – ігноруємо, якщо ми все ще перебуваємо всередині поточного `<td>`.
-   При `mouseout` – ігноруємо, якщо ми не залишили поточний `<td>`.

Ось приклад коду, який враховує всі можливі ситуації:

```javascript
// <td> під вказівником прямо зараз (якщо є)
let currentElem = null;

table.onmouseover = function(event) {
  // перед переходом до нового елемента миша завжди залишає попередній
  // якщо вже встановлено currentElem, то ми ще не залишили попередній <td>,
  // і цей mouseover відбувається всередині, тому ігноруємо подію
  if (currentElem) return;

  let target = event.target.closest('td');

  // ми перейшли не в <td> - ігнорувати
  if (!target) return;

  // переміщено в <td>, але за межами нашої таблиці (можливо у випадку вкладених таблиць)
  // ігнорувати
  if (!table.contains(target)) return;

  // ура! ми перейшли до нового <td>
  currentElem = target;
  onEnter(currentElem);
};


table.onmouseout = function(event) {
  // якщо ми зараз поза будь-яким <td>, тоді ігноруємо подію
  // це, мабуть, переміщення всередину таблиці, але поза <td>,
  // напр. від <tr> до іншого <tr>
  if (!currentElem) return;

  // покидаємо елемент – але куди? Може ідемо до дочірнього елемента?
  let relatedTarget = event.relatedTarget;

  while (relatedTarget) {
    // піднімаємось батьківським ланцюжком і перевіряємо – чи ми все ще всередині currentElem
    // тоді це внутрішній перехід – ігноруємо його
    if (relatedTarget == currentElem) return;

    relatedTarget = relatedTarget.parentNode;
  }

  // ми залишили <td>. насправді.
  onLeave(currentElem);
  currentElem = null;
};

// будь-які функції для обробки входу/виходу з елемента
function onEnter(elem) {
  elem.style.background = 'pink';

  // показати це в textarea
  text.value += `over -> ${currentElem.tagName}.${currentElem.className}\n`;
  text.scrollTop = 1e6;
}

function onLeave(elem) {
  elem.style.background = '';

  // показати це в textarea
  text.value += `out <- ${elem.tagName}.${elem.className}\n`;
  text.scrollTop = 1e6;
}
```

І ще раз про важливі особливості такого підходу:

1.  Ми використовуємо делегування подій для обробки входу/виходу вказівника на будь-який `<td>` всередині таблиці. Таким чином, ми покладаємося на `mouseover/out` замість `mouseenter/leave`, які не спливають і, отже, не дозволяють делегування.
2.  Додаткові події, такі як переміщення між нащадками `<td>`, відфільтровуються, тому `onEnter/Leave` запускається, лише якщо вказівник залишає або входить на `<td>`.

Ось повний приклад з усіма деталями:

Результат

script.js

style.css

index.html

```
// <td> під вказівником прямо зараз (якщо є)
let currentElem = null;

table.onmouseover = function(event) {
  // перед переходом до нового елемента миша завжди залишає попередній
  // якщо вже встановлено currentElem, то ми ще не залишили попередній <td>,
  // і цей mouseover відбувається всередині, тому ігноруємо подію
  if (currentElem) return;

  let target = event.target.closest('td');

  // ми перейшли не в <td> - ігнорувати
  if (!target) return;

  // переміщено в <td>, але за межами нашої таблиці (можливо у випадку вкладених таблиць)
  // ігнорувати
  if (!table.contains(target)) return;

  // ура! ми перейшли до нового <td>
  currentElem = target;
  onEnter(currentElem);
};


table.onmouseout = function(event) {
  // якщо ми зараз поза будь-яким <td>, тоді ігноруємо подію
  // це, мабуть, переміщення всередину таблиці, але поза <td>,
  // напр. від <tr> до іншого <tr>
  if (!currentElem) return;

  // покидаємо елемент – але куди? Може ідемо до дочірнього елемента?
  let relatedTarget = event.relatedTarget;

  while (relatedTarget) {
    // піднімаємось батьківським ланцюжком і перевіряємо – чи ми все ще всередині currentElem
    // тоді це внутрішній перехід – ігноруємо його
    if (relatedTarget == currentElem) return;

    relatedTarget = relatedTarget.parentNode;
  }

  // ми залишили <td>. насправді.
  onLeave(currentElem);
  currentElem = null;
};

// будь-які функції для обробки входу/виходу з елемента
function onEnter(elem) {
  elem.style.background = 'pink';

  // показати це в textarea
  text.value += `over -> ${currentElem.tagName}.${currentElem.className}\n`;
  text.scrollTop = 1e6;
}

function onLeave(elem) {
  elem.style.background = '';

  // показати це в textarea
  text.value += `out <- ${elem.tagName}.${elem.className}\n`;
  text.scrollTop = 1e6;
}
```

```
#text {
  display: block;
  height: 100px;
  width: 456px;
}

#table th {
  text-align: center;
  font-weight: bold;
}

#table td {
  width: 150px;
  white-space: nowrap;
  text-align: center;
  vertical-align: bottom;
  padding-top: 5px;
  padding-bottom: 12px;
  cursor: pointer;
}

#table .nw {
  background: #999;
}

#table .n {
  background: #03f;
  color: #fff;
}

#table .ne {
  background: #ff6;
}

#table .w {
  background: #ff0;
}

#table .c {
  background: #60c;
  color: #fff;
}

#table .e {
  background: #09f;
  color: #fff;
}

#table .sw {
  background: #963;
  color: #fff;
}

#table .s {
  background: #f60;
  color: #fff;
}

#table .se {
  background: #0c3;
  color: #fff;
}

#table .highlight {
  background: red;
}
```

```
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="style.css">
</head>

<body>


  <table id="table">
    <tr>
      <th colspan="3"><em>Bagua</em> Chart: Direction, Element, Color, Meaning</th>
    </tr>
    <tr>
      <td class="nw"><strong>Northwest</strong>
        <br>Metal
        <br>Silver
        <br>Elders
      </td>
      <td class="n"><strong>North</strong>
        <br>Water
        <br>Blue
        <br>Change
      </td>
      <td class="ne"><strong>Northeast</strong>
        <br>Earth
        <br>Yellow
        <br>Direction
      </td>
    </tr>
    <tr>
      <td class="w"><strong>West</strong>
        <br>Metal
        <br>Gold
        <br>Youth
      </td>
      <td class="c"><strong>Center</strong>
        <br>All
        <br>Purple
        <br>Harmony
      </td>
      <td class="e"><strong>East</strong>
        <br>Wood
        <br>Blue
        <br>Future
      </td>
    </tr>
    <tr>
      <td class="sw"><strong>Southwest</strong>
        <br>Earth
        <br>Brown
        <br>Tranquility
      </td>
      <td class="s"><strong>South</strong>
        <br>Fire
        <br>Orange
        <br>Fame
      </td>
      <td class="se"><strong>Southeast</strong>
        <br>Wood
        <br>Green
        <br>Romance
      </td>
    </tr>

  </table>

  <textarea id="text"></textarea>

  <input type="button" onclick="text.value=''" value="Clear">

  <script src="script.js"></script>

</body>
</html>
```

Спробуйте перемістити курсор у клітини таблиці та всередину них. Швидко чи повільно – не має значення. На відміну від попереднього прикладу, виділено лише `<td>`.

## [Підсумки](https://uk.javascript.info/mousemove-mouseover-mouseout-mouseenter-mouseleave#pidsumki)

Ми розглянули події `mouseover`, `mouseout`, `mousemove`, `mouseenter` і `mouseleave`.

Варто звернути увагу на такі речі:

-   Швидкий рух миші може призвести до пропуску проміжних елементів.
-   Події `mouseover/out` і `mouseenter/leave` мають додаткову властивість: `relatedTarget`. Це елемент, до/від якого ми йдемо, ця властивість доповнює `target`.

Події `mouseover/out` запускаються, навіть коли ми переходимо від батьківського елемента до дочірнього. Браузер припускає, що вказівник миші може одночасно перебувати лише над одним елементом – найвкладенішим.

Події `mouseenter/leave` відрізняються в цьому аспекті: вони запускаються лише тоді, коли вказівник миші входить і виходить з елемента в цілому. І ще вони не спливають.