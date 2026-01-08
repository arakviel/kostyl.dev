---
title: Navigator Object - Ідентифікація та Можливості Пристрою
description: Вичерпний посібник з об'єкта Navigator. Детальний розбір User Agent Client Hints, Geolocation API, Clipboard API, MediaStream Constraints, Network Information, Battery Status, Screen Wake Lock та інших API.
---

# Navigator Object - Ідентифікація та Можливості Пристрою

## Вступ

Об'єкт `window.navigator` (або просто `navigator`) — це швейцарський ніж у світі веб-розробки. Він служить головним інтерфейсом між JavaScript-кодом та самим браузером / операційною системою. Якщо вам потрібно дізнатися, хто ваш користувач, де він знаходиться, чи є у нього доступ до інтернету, або попросити дозволу на використання мікрофона — ви звертаєтеся до `navigator`.

Цей об'єкт еволюціонував від простого рядка з назвою браузера до потужного шлюзу до апаратних можливостей пристрою. Сучасний `navigator` дозволяє веб-сайтам поводитися як нативні додатки: вібрувати, отримувати доступ до Bluetooth, USB, геолокації та буфера обміну.

У цьому масштабному посібнику ми детально розглянемо кожен аспект роботи з `navigator`, розберемо застарілі властивості та сучасні API, навчимося писати безпечний та сумісний код.

::tip
**Контекст виконання**
Більшість методів `navigator` доступні як в основному потоці (Window), так і в Web Workers (WorkerNavigator). Однак деякі API, пов'язані з UI або DOM, можуть бути недоступні у воркерах. Ми будемо відзначати такі моменти спеціальними помітки.
::

## 1. Ідентифікація Клієнта (User Agent)

Історично склалося, що найперша задача `navigator` — повідомити серверу або скрипту, який саме браузер використовує клієнт.

### `navigator.userAgent`

Це рядок, який браузер відправляє у заголовку HTTP `User-Agent`.

```javascript
console.log(navigator.userAgent);
// Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

#### Проблема User Agent
Рядок `userAgent` — це "велика брехня". Зверніть увагу на приклад вище: Chrome називає себе "Mozilla", "AppleWebKit", "KHTML", "Gecko" і "Safari". Це робиться для сумісності з сайтами, які перевіряють наявність певних підстрок.

Парсинг цього рядка — складна та ненадійна задача. Якщо ви намагаєтеся визначити браузер через RegEx, ви, ймовірно, робите помилку.

### User-Agent Client Hints (Сучасний підхід)

Щоб вирішити проблему "смітника" в `userAgent` та покращити приватність (зменшити можливості для "fingerprinting"), був введений **User-Agent Client Hints API**.

Доступ через `navigator.userAgentData`. Цей об'єкт надає структуровані дані без необхідності парсингу.

#### Основні властивості `userAgentData`

```javascript
if (navigator.userAgentData) {
    // 1. Brands - масив об'єктів { brand, version }
    // Браузер повертає кілька брендів, включаючи GREASE (випадкові значення для запобігання жорсткому кодуванню)
    const brands = navigator.userAgentData.brands;
    console.log(brands);
    // [
    //   { brand: "Google Chrome", version: "120" },
    //   { brand: "Not_A Brand", version: "8" },
    //   { brand: "Chromium", version: "120" }
    // ]

    // 2. Mobile - булеве значення
    const isMobile = navigator.userAgentData.mobile;
    console.log(`Мобільний пристрій: ${isMobile}`);

    // 3. Platform - загальна назва платформи (Windows, macOS, Android)
    const platform = navigator.userAgentData.platform;
    console.log(`Платформа: ${platform}`); // "Windows"
}
```

#### Метод `getHighEntropyValues()`

За замовчуванням `userAgentData` повертає лише базову інформацію (Low Entropy). Якщо вам потрібно більше деталей (версія ОС, архітектура процесора, повна версія браузера), ви повинні явно запросити ці дані. Це асинхронна операція.

```javascript
if (navigator.userAgentData) {
    navigator.userAgentData.getHighEntropyValues([
        "architecture",
        "model",
        "platformVersion",
        "fullVersionList"
    ])
    .then(ua => {
        console.log("CPU Architecture:", ua.architecture); // "x86"
        console.log("Device Model:", ua.model);           // "Pixel 6"
        console.log("OS Version:", ua.platformVersion);   // "10.0.0"
    });
}
```

::warning
**Підтримка браузерами**
User-Agent Client Hints наразі підтримується переважно в браузерах на базі Chromium (Chrome, Edge, Opera). Firefox та Safari поки що не підтримують цей API повноцінно. Завжди перевіряйте наявність властивості `navigator.userAgentData` перед використанням та майте fallback на `navigator.userAgent`.
::

### `navigator.language` та `navigator.languages`

Дозволяє дізнатися мовні налаштування користувача. Це критично для інтернаціоналізації (i18n) та форматування дат/чисел.

-   `language`: Рядок з основною мовою (наприклад, `"uk-UA"`).
-   `languages`: Масив усіх мов, які знає користувач, у порядку пріоритету (наприклад, `["uk-UA", "uk", "en-US", "en"]`).

**Стратегія визначення мови:**

```javascript
function getBestLanguage(supportedLanguages = ['en', 'uk']) {
    // Перевіряємо масив languages
    if (navigator.languages) {
        for (let lang of navigator.languages) {
            // Отримуємо код мови без регіону (uk-UA -> uk)
            const baseLang = lang.split('-')[0];
            if (supportedLanguages.includes(baseLang)) {
                return baseLang;
            }
        }
    }
    
    // Fallback на language
    const singleLang = (navigator.language || navigator.userLanguage || 'en').split('-')[0];
    return supportedLanguages.includes(singleLang) ? singleLang : 'en';
}

console.log(`Обрана мова: ${getBestLanguage()}`);
```

### `navigator.cookieEnabled`

Повертає `true`, якщо cookies дозволені, і `false`, якщо заблоковані налаштуваннями браузера. Це важливо перевіряти перед спробою запису в `localStorage` або `document.cookie`.

```javascript
if (!navigator.cookieEnabled) {
    // Показуємо банер
    showCookieWarning("Будь ласка, увімкніть Cookies для коректної роботи сайту.");
}
```

## 2. Геолокація (Geolocation API)

Один з найпопулярніших API об'єкта Navigator. Дозволяє отримати фізичне розташування користувача. Знаходиться у властивості `navigator.geolocation`.

::note
**Безпека та Приватність**
Цей API працює **тільки** у безпечному контексті (HTTPS). Браузер завжди запитує дозвіл користувача перед наданням доступу. Якщо користувач блокує доступ, ви не зможете отримати дані.
::

### Об'єкт налаштувань (PositionOptions)

Усі методи геолокації приймають третім аргументом об'єкт налаштувань:

-   `enableHighAccuracy` (boolean): За замовчуванням `false`. Якщо `true`, пристрій вмикає GPS (більш точний, але енергозатратний). Якщо `false` - використовує Wi-Fi/IP (швидше, менш точно).
-   `timeout` (number): Максимальний час очікування відповіді в мілісекундах. За замовчуванням `Infinity`.
-   `maximumAge` (number): Час життя кешу позиції в мілісекундах. Якщо `0`, браузер завжди намагатиметься отримати свіжі дані.

### `getCurrentPosition()`

Отримує поточне розташування один раз.

```javascript
const options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
};

const success = (pos) => {
    // pos - це об'єкт GeolocationPosition
    const crd = pos.coords; // GeolocationCoordinates

    console.log("Ваше поточне розташування:");
    console.log(`Широта: ${crd.latitude}`);
    console.log(`Довгота: ${crd.longitude}`);
    console.log(`Точність: +/- ${crd.accuracy} метрів`);
    
    // Додаткові параметри (можуть бути null)
    if (crd.altitude) console.log(`Висота: ${crd.altitude}`);
    if (crd.speed) console.log(`Швидкість: ${crd.speed} м/с`); // Тільки якщо рухається
    if (crd.heading) console.log(`Напрямок: ${crd.heading} градусів`);
};

const error = (err) => {
    // err - це об'єкт GeolocationPositionError
    switch(err.code) {
        case err.PERMISSION_DENIED: // code 1
            console.error("Користувач заборонив доступ до геолокації.");
            break;
        case err.POSITION_UNAVAILABLE: // code 2
            console.error("Інформація про місцезнаходження недоступна.");
            break;
        case err.TIMEOUT: // code 3
            console.error("Час очікування запиту вичерпано.");
            break;
        default:
            console.error("Невідома помилка:", err.message);
    }
};

navigator.geolocation.getCurrentPosition(success, error, options);
```

### `watchPosition()`

Стежить за зміною розташування. Функція `success` викликатиметься кожного разу, коли пристрій фіксує зміну позиції. Це ідеально для навігаторів або трекерів пробіжки.

```javascript
let watchId;

function startTracking() {
    if (navigator.geolocation) {
        watchId = navigator.geolocation.watchPosition(success, error, options);
        console.log(`Трекінг розпочато. ID: ${watchId}`);
    }
}

function stopTracking() {
    if (watchId) {
        navigator.geolocation.clearWatch(watchId);
        watchId = null;
        console.log("Трекінг зупинено.");
    }
}
```

## 3. Clipboard API (Буфер Обміну)

Сучасний асинхронний API для роботи з буфером обміну, який замінив старий і синхронний `document.execCommand('copy')`.
Доступний через `navigator.clipboard`.

::caution
**Вимоги до безпеки**
1. Тільки HTTPS (або localhost).
2. Для запису (`write`, `writeText`) сторінка має бути активною (у фокусі).
3. Для читання (`read`, `readText`) браузер запитає дозвіл у користувача.
::

### Робота з текстом

Найчастіший сценарій — копіювання промокодів, посилань тощо.

```javascript
/* Копіювання тексту */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        console.log("Текст успішно скопійовано!");
    } catch (err) {
        console.error("Помилка копіювання:", err);
    }
}

/* Читання тексту */
async function pasteFromClipboard() {
    try {
        const text = await navigator.clipboard.readText();
        console.log("В буфері:", text);
        return text;
    } catch (err) {
        console.error("Не вдалося прочитати буфер:", err);
    }
}
```

### Робота з іншими типами даних (зображення, HTML)

API дозволяє працювати не тільки з текстом, але й з бінарними даними (наприклад, вставка картинки прямо в редактор). Для цього використовуються методи `write()` та `read()`, які працюють з об'єктами `ClipboardItem`.

**Копіювання зображення:**

```javascript
async function copyImage(blob) {
    try {
        // Ми повинні передати об'єкт, де ключ - MIME type, значення - Blob
        const data = [new ClipboardItem({ [blob.type]: blob })];
        
        await navigator.clipboard.write(data);
        console.log("Зображення скопійовано!");
    } catch (err) {
        console.error(err);
    }
}

// Приклад використання з Canvas
const canvas = document.querySelector('canvas');
canvas.toBlob(blob => copyImage(blob));
```

**Читання (вставка) зображення:**

```javascript
async function pasteImage() {
    try {
        const clipboardItems = await navigator.clipboard.read();
        
        for (const item of clipboardItems) {
            // Перевіряємо, чи є в цьому елементі зображення
            if (item.types.includes('image/png')) {
                const blob = await item.getType('image/png');
                
                // Відображаємо
                const img = document.createElement('img');
                img.src = URL.createObjectURL(blob);
                document.body.appendChild(img);
            }
        }
    } catch (err) {
        console.error(err);
    }
}
```

## 4. Media Devices (Камера, Мікрофон, Екран)

Властивість `navigator.mediaDevices` надає доступ до підключених медіа-пристроїв. Це основа для WebRTC, відеодзвінків та запису екрану.

### `getUserMedia()` та MediaTrackConstraints

Метод `getUserMedia` приймає об'єкт `constraints`, який дозволяє дуже точно налаштувати бажаний потік.

```javascript
const constraints = {
    audio: {
        echoCancellation: true, // Придушення ехо
        noiseSuppression: true, // Шумозаглушення
        autoGainControl: false  // Автоматичне регулювання гучності
    },
    video: { 
        width: { min: 640, ideal: 1920, max: 3840 }, // 4K max, 1080p ideal
        height: { min: 480, ideal: 1080, max: 2160 },
        frameRate: { ideal: 60, min: 30 }, // Бажано 60 FPS
        facingMode: "user" // або { exact: "environment" } для задньої камери
    }
};

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        
        const videoElement = document.querySelector('video');
        videoElement.srcObject = stream;
        
        // Отримання списку треків для подальшого керування (наприклад, mute)
        const videoTrack = stream.getVideoTracks()[0];
        console.log(`Камера: ${videoTrack.label}`);
        
    } catch (err) {
        handleMediaError(err);
    }
}
```

**Типи помилок `getUserMedia`:**

-   `NotAllowedError`: Користувач натиснув "Block" у вікні запиту дозволу.
-   `NotFoundError`: Запитуваний пристрій (наприклад, камера) не знайдено.
-   `NotReadableError`: Пристрій зайнятий іншою програмою (наприклад, Zoom) або апаратна помилка.
-   `OverconstrainedError`: Браузер не може задовольнити ваші вимоги (наприклад, ви просили `min: 4K`, а камера тільки HD).

### `getDisplayMedia()` (Запис екрану)

Дозволяє захопити вміст екрану (весь екран, вікно програми або вкладку браузера).

```javascript
async function startScreenShare() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({
            video: { cursor: "always" },
            audio: false // Зазвичай аудіо системи доступне не у всіх ОС
        });
        
        document.querySelector('video').srcObject = stream;
        
        // Відстеження зупинки шерінгу (коли користувач натискає "Stop sharing" у браузері)
        stream.getVideoTracks()[0].onended = () => {
            console.log("Шерінг екрану зупинено");
        };
        
    } catch (err) {
        console.error("Помилка захоплення екрану:", err);
    }
}
```

### `enumerateDevices()` та подія `devicechange`

Ви можете отримати список усіх пристроїв і реагувати на підключення/відключення (наприклад, коли користувач вставив навушники).

```javascript
async function listDevices() {
    const devices = await navigator.mediaDevices.enumerateDevices();
    
    const cameras = devices.filter(d => d.kind === 'videoinput');
    const mics = devices.filter(d => d.kind === 'audioinput');
    const speakers = devices.filter(d => d.kind === 'audiooutput');
    
    console.log(`Знайдено: камер ${cameras.length}, мікрофонів ${mics.length}`);
}

// Слухаємо зміни
navigator.mediaDevices.ondevicechange = (event) => {
    console.log("Конфігурація пристроїв змінилася!");
    listDevices(); // Оновлюємо список у UI
};
```

## 5. Network Information API

Дозволяє дізнатися про якість підключення до мережі. Це корисно для **Adaptive Loading**: завантажувати відео високої якості для Wi-Fi та картинки-заглушки для повільного 2G.

Доступний через `navigator.connection` (в основному Chrome/Android).

```javascript
const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;

if (connection) {
    // effectiveType: 'slow-2g', '2g', '3g', '4g'
    // Це не фізичний тип мережі, а "ефективна швидкість"
    console.log(`Ефективний тип: ${connection.effectiveType}`); 
    
    // Приблизна швидкість завантаження (Мбіт/с)
    console.log(`Downlink: ~${connection.downlink} Mbps`);
    
    // Приблизний RTT (Round Trip Time) у мс
    console.log(`RTT: ${connection.rtt} ms`);
    
    // Save-Data заголовок (користувач увімкнув режим економії в налаштуваннях)
    const isSaveData = connection.saveData; // true/false

    if (isSaveData || connection.effectiveType.includes('2g')) {
        console.log("Завантажуємо полегшену версію сайту...");
        loadLowResImages();
    } else {
        loadHighResContent();
    }

    // Відстеження змін мережі
    connection.addEventListener('change', () => {
        console.log("Мережа змінилася:", connection.effectiveType);
    });
}
```

Для простої перевірки "онлайн/офлайн" використовуйте `navigator.onLine`.

```javascript
window.addEventListener('offline', () => showToast('Ви офлайн! Перевірте з\'єднання.'));
window.addEventListener('online', () => showToast('Зв\'язок відновлено!'));
```

## 6. Battery Status API

Надає інформацію про рівень заряду батареї та статус зарядки.

::warning
**Deprecation Warning & Privacy**
Цей API більше не підтримується у Firefox та WebKit через потенційну можливість відстеження користувачів (fingerprinting). Він працює переважно в Chrome.
::

```javascript
if ('getBattery' in navigator) {
    navigator.getBattery().then(battery => {
        function updateBatteryStatus() {
            const level = Math.round(battery.level * 100);
            const isCharging = battery.charging;
            
            console.log(`Заряд: ${level}% ${isCharging ? '⚡' : ''}`);
            
            if (level <= 20 && !isCharging) {
                console.warn("Низький заряд! Вимикаємо важкі анімації.");
                disableAnimations();
            }
        }

        updateBatteryStatus();

        // Події
        battery.addEventListener('chargingchange', updateBatteryStatus);
        battery.addEventListener('levelchange', updateBatteryStatus);
    });
}
```

## 7. Web Share API

Дозволяє викликати нативний діалог "Поділитися" мобільної операційної системи. Це набагато краще, ніж кастомні кнопки Facebook/Twitter.

**Вимоги:**
-   Тільки HTTPS.
-   Тільки у відповідь на дію користувача (клік).

```javascript
const shareBtn = document.getElementById('share');

shareBtn.addEventListener('click', async () => {
    const shareData = {
        title: 'MDN Web Docs',
        text: 'Вивчайте веб-розробку з MDN!',
        url: 'https://developer.mozilla.org',
    };
    
    // 1. Перевірка підтримки взагалі
    if (!navigator.share) {
        console.log("Web Share API не підтримується");
        return;
    }

    // 2. Перевірка валідності даних (чи можемо ми поділитися саме цим набором?)
    // Наприклад, деякі ОС не підтримують одночасний шерінг файлів і тексту
    if (navigator.canShare && !navigator.canShare(shareData)) {
        console.log("Ці дані не можна поширити");
        return;
    }

    try {
        await navigator.share(shareData);
        console.log("Успішно! Користувач вибрав додаток.");
    } catch (err) {
        if (err.name === 'AbortError') {
            console.log("Користувач закрив вікно шерінгу.");
        } else {
            console.error("Помилка:", err);
        }
    }
});
```

## 8. Permissions API

Дозволяє програмно перевіряти стан дозволів (geolocation, camera, notification, etc.) без запиту самого дозволу (який показує спливаюче вікно).

```javascript
const permissionsToCheck = ['geolocation', 'camera', 'microphone', 'notifications'];

async function checkPermissions() {
    for (const name of permissionsToCheck) {
        try {
            const result = await navigator.permissions.query({ name });
            
            console.log(`${name}: ${result.state}`);
            // 'granted' - дозволено
            // 'denied' - заборонено
            // 'prompt' - запитає при спробі доступу

            // Слухаємо зміни (наприклад, користувач змінив налаштування в панелі браузера)
            result.onchange = () => {
                console.log(`Дозвіл ${name} змінився на ${result.state}`);
            };
        } catch (error) {
            // Деякі дозволи можуть не підтримуватися в Firefox/Safari
            console.log(`${name} не підтримується Permissions API`);
        }
    }
}
```

## 9. Screen Wake Lock API

Новий API, що дозволяє заборонити екрану тьмяніти або блокуватися. Це критично для:
-   Сайтів з рецептами (коли руки брудні).
-   Презентацій.
-   QR-кодів (квитків).
-   Веб-ігор.

```javascript
let wakeLock = null;

// Функція запиту блокування (тримати екран увімкненим)
async function requestWakeLock() {
    if ('wakeLock' in navigator) {
        try {
            wakeLock = await navigator.wakeLock.request('screen');
            console.log('Screen Wake Lock активовано!');

            wakeLock.addEventListener('release', () => {
                console.log('Screen Wake Lock деактивовано (наприклад, вкладка стала неактивною)');
            });

        } catch (err) {
            console.error(`${err.name}, ${err.message}`);
        }
    }
}

// Функція звільнення
async function releaseWakeLock() {
    if (wakeLock !== null) {
        await wakeLock.release();
        wakeLock = null;
    }
}

// Важливо: Браузер автоматично знімає Wake Lock, якщо сторінка/вкладка згорнута.
// Нам потрібно поновити запит, коли користувач повертається.
document.addEventListener('visibilitychange', async () => {
    if (wakeLock !== null && document.visibilityState === 'visible') {
        await requestWakeLock();
    }
});
```

## 10. Інші корисні властивості

### `navigator.hardwareConcurrency`
Повертає кількість логічних процесорів (ядер), доступних для виконання потоків. Використовуйте це число для створення оптимальної кількості Web Workers.

```javascript
const cores = navigator.hardwareConcurrency || 4; // Fallback
console.log(`Доступно ядер: ${cores}`);
```

### `navigator.maxTouchPoints`
Повертає максимальну кількість точок дотику. Це найнадійніший спосіб перевірити, чи має пристрій тачскрін (на відміну від перевірки User Agent на "Mobile").

```javascript
const isTouchDevice = navigator.maxTouchPoints > 0;
```

### `navigator.vibrate()`
Змушує пристрій вібрувати (тактильний відгук).

```javascript
// Вібрувати 200мс (проста вібрація)
navigator.vibrate(200);

// Паттерн "SOS": ... --- ...
// [вібрація, пауза, вібрація, пауза, ...]
navigator.vibrate([
    100, 30, 100, 30, 100, 200, // S
    300, 100, 300, 100, 300, 200, // O
    100, 30, 100, 30, 100 // S
]);

// Зупинити вібрацію
navigator.vibrate(0);
```

### `navigator.sendBeacon(url, data)`
Метод для асинхронної відправки невеликої кількості даних (аналітика, логи) на сервер при закритті сторінки.

**Чому не `fetch`?**
Запит `fetch` може бути перерваний, якщо сторінка закривається. `sendBeacon` передає дані браузеру, і браузер гарантує їх відправку навіть після знищення сторінки.

```javascript
window.addEventListener("visibilitychange", function() {
    if (document.visibilityState === 'hidden') {
        const data = new Blob([JSON.stringify({ event: 'leave', time: Date.now() })], { type: 'application/json' });
        
        // Повертає true, якщо дані поставлені в чергу успішно
        const queued = navigator.sendBeacon('/api/analytics', data);
    }
});
```

## Підсумкова Таблиця API

| API | Властивість | Опис | HTTPS? | User Gesture? |
| :--- | :--- | :--- | :---: | :---: |
| **Geolocation** | `geolocation` | Координати GPS | ✅ | ✅ |
| **Clipboard** | `clipboard` | Копіювання/Вставка | ✅ | ✅ (Write) |
| **Media** | `mediaDevices` | Камера, Мікрофон, Екран | ✅ | ✅ |
| **Share** | `share()` | Нативний діалог шейрінгу | ✅ | ✅ |
| **Wake Lock** | `wakeLock` | Блокування екрану | ✅ | ❌ |
| **Vibration** | `vibrate()` | Вібро-відгук | ❌ | ✅ (Chrome) |
| **Connection** | `connection` | Тип мережі (4G/wifi) | ❌ | ❌ |
| **User Agent** | `userAgentData` | Інформація про браузер | ✅ | ❌ |

## Висновок

Об'єкт `navigator` надає неймовірні можливості для перетворення веб-сайту на повноцінний додаток. Вміле використання цих API дозволяє покращити UX (запам'ятовування позиції, адаптація під мережу, вібрація при помилках) та створити нові сценарії використання (відеодзвінки, карти, шерінг).

Пам'ятайте про **progressive enhancement**: ваші сайти повинні працювати (хоча б базово), навіть якщо ці API недоступні або заблоковані користувачем. Завжди перевіряйте наявність, наприклад: `if ('share' in navigator) { ... } else { ... }`.
