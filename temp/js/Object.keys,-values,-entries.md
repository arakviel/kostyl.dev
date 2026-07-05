Відійдемо від окремих структур даних і поговоримо про ітерації над ними.

У минулому розділі ми бачили методи `map.keys()`, `map.values()`, `map.entries()`.

Ці методи є загальними, існує спільна згода використовувати їх для структур даних. Якщо ми створюватимемо власну структуру даних, нам слід їх також реалізувати.

Вони підтримуються для:

-   `Map`
-   `Set`
-   `Array`

Звичайні об’єкти також підтримують подібні методи, але синтаксис дещо інший.

## [Object.keys, values, entries](https://uk.javascript.info/keys-values-entries#object-keys-values-entries)

Для простих об’єктів доступні наступні методи:

-   [Object.keys(obj)](https://developer.mozilla.org/uk/docs/Web/JavaScript/Reference/Global_Objects/Object/keys) – повертає масив ключів.
-   [Object.values(obj)](https://developer.mozilla.org/uk/docs/Web/JavaScript/Reference/Global_Objects/Object/values) – повертає масив значень.
-   [Object.entries(obj)](https://developer.mozilla.org/uk/docs/Web/JavaScript/Reference/Global_Objects/Object/entries) – повертає масив пар `[ключ, значення]`.

Зверніть увагу на відмінності (порівняно з map, наприклад):

|Map|Object|
|---|---|
|Синтаксис виклику|`map.keys()`|`Object.keys(obj)`, а не `obj.keys()`|
|Повертає|ітерабельний|“реальний” масив|

Перша відмінність полягає в тому, що ми повинні викликати `Object.keys(obj)`, а не `obj.keys()`.

Чому так? Основною причиною цього є гнучкість. Пам’ятайте, об’єкти є базою всіх складних структур у JavaScript. Ми можемо мати власний об’єкт, такий як `data`, який реалізує власний метод `data.values()`. І ми все ще можемо застосовувати до нього `Object.values(data)`.

Друга відмінність полягає в тому, що `Object.*` методи повертають “реальний” масив об’єктів, а не просто ітерабельний. Це переважно з історичних причин.

Наприклад:

```javascript
let user = {
  name: "Іван",
  age: 30
};
```

-   `Object.keys(user) = ["name", "age"]`
-   `Object.values(user) = ["Іван", 30]`
-   `Object.entries(user) = [ ["name","Іван"], ["age",30] ]`

Це приклад використання `Object.values` для перебору значень властивостей у циклі:

```javascript
let user = {
  name: "Іван",
  age: 30
};

// Перебираємо значення
for (let value of Object.values(user)) {
  alert(value); // Іван, тоді 30
}
```

Object.keys/values/entries ігнорують символьні властивості

Як і цикл `for..in`, ці методи ігнорують властивості, що використовують `Symbol(...)` як ключі.

Зазвичай це зручно. Якщо ми хочемо враховувати символьні ключі також, то для цього існує окремий метод [Object.getOwnPropertySymbols](https://developer.mozilla.org/uk/docs/Web/JavaScript/Reference/Global_Objects/Object/getOwnPropertySymbols), що повертає масив лише символьних ключів. Також існує метод [Reflect.ownKeys(obj)](https://developer.mozilla.org/uk/docs/Web/JavaScript/Reference/Global_Objects/Reflect/ownKeys) , що повертає _усі_ ключі.

## [Трансформація об’єктів](https://uk.javascript.info/keys-values-entries#transformaciya-obyektiv)

У об’єктів немає багатьох методів, які є у масивів, наприклад `map`, `filter` та інші.

Якщо б ми хотіли їх застосувати, тоді б ми використовували `Object.entries` з подальшим викликом `Object.fromEntries`:

1.  Викликаємо `Object.entries(obj)`, щоб отримати масив пар ключ/значення з `obj`.
2.  На ньому використовуємо методи масиву, наприклад `map`, щоб перетворити ці пари ключів/значень.
3.  Використаємо `Object.fromEntries(array)` на отриманому масиві, щоб перетворити його знову на об’єкт.

Наприклад, у нас є об’єкт з цінами, і ми б хотіли їх подвоїти:

```javascript
let prices = {
  banana: 1,
  orange: 2,
  meat: 4,
};

let doublePrices = Object.fromEntries(
  // перетворити ціни на масив, потім застосувати map, щоб перетворити на пари ключ/значення
  // а потім fromEntries повертає об’єкт
  Object.entries(prices).map(entry => [entry[0], entry[1] * 2])
);

alert(doublePrices.meat); // 8
```

З першого погляду це може здатися важким, але стане зрозумілим після того, як ви використаєте це декілька разів. Таким чином ми можемо створювати потужні ланцюги перетворень.

## [Завдання](https://uk.javascript.info/keys-values-entries#tasks)

важливість: 5

Є об’єкт `salaries` з довільною кількістю властивостей, що містять заробітні плати.

Напишіть функцію `sumSalaries(salaries)`, що повертає суму всіх зарплат за допомогою `Object.values` та циклу`for..of`.

Якщо об’єкт `salaries` порожній, тоді результат повинен бути `0`.

Наприклад:

```javascript
let salaries = {
  "Іван": 100,
  "Петро": 300,
  "Марія": 250
};

alert( sumSalaries(salaries) ); // 650
```

[Відкрити пісочницю з тестами.](https://plnkr.co/edit/XdErYQ5Q1qw3oDBX?p=preview)

```javascript
function sumSalaries(salaries) {

  let sum = 0;
  for (let salary of Object.values(salaries)) {
    sum += salary;
  }

  return sum; // 650
}

let salaries = {
  "Іван": 100,
  "Петро": 300,
  "Марія": 250
};

alert( sumSalaries(salaries) ); // 650
```

Або ж ми можемо також отримати суму, використовуючи `Object.values` та `reduce`:

```javascript
// reduce перебирає масив значень salaries,
// складає їх
// і повертає результат
function sumSalaries(salaries) {
  return Object.values(salaries).reduce((a, b) => a + b, 0) // 650
}
```

[Відкрити рішення із тестами в пісочниці.](https://plnkr.co/edit/5ozil93cvDO3VdN4?p=preview)

важливість: 5

Напишіть функцію `count(obj)`, що повертає кількість властивостей об’єкта:

```javascript
let user = {
  name: 'Іван',
  age: 30
};

alert( count(user) ); // 2
```

Намагайтеся зробити код якомога коротшим.

P.S. Ігноруйте символьні властивості, враховуйте лише “звичайні”.

[Відкрити пісочницю з тестами.](https://plnkr.co/edit/k7I6bzA45VccjBpl?p=preview)