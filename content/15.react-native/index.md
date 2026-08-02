---
title: React Native
icon: i-logos-react
description: Курс мобільної розробки на React Native для тих, хто вже знає React, Redux і TypeScript
---

# React Native

Курс проводить від знайомого **web React** до production-ready мобільних застосунків на **iOS** і **Android**.

## Для кого цей курс

- Ви вже пишете на **React**, **TypeScript** і **Redux** (Toolkit).
- Ви хочете системно опанувати **React Native**, а не зібрати «hello world» з випадкових туторіалів.
- Вам потрібен шлях **Expo → реальні фічі → stores → React Native CLI / bare**.

## Що буде далі

Основний навчальний застосунок курсу — **Nomad** (щоденник подорожей, український UI). Код: **[https://github.com/arakviel/nomad](https://github.com/arakviel/nomad)**. Кожна стаття містить теорію, **міні-проєкт «від А до Я»** і крок інтеграції в Nomad.

::card-group

::card{title="1. Навіщо React Native" to="/react-native/why-react-native" icon="i-lucide-smartphone"}
Навіщо потрібен мобільний застосунок, чим він відрізняється від сайту, і коли обирати React Native.
::

::card{title="2. Архітектура runtime" to="/react-native/react-native-architecture" icon="i-lucide-cpu"}
Як код на TypeScript доходить до кнопок на екрані: логіка, малювання, Metro, Hermes, шлях натискання.
::

::card{title="3. Expo і CLI" to="/react-native/expo-vs-cli-landscape" icon="i-lucide-git-branch"}
Два способи вести React Native-проєкт: Expo й класичний CLI — що обрати і як побудований курс.
::

::card{title="4. Середовище Expo" to="/react-native/expo-setup-and-tooling" icon="i-lucide-terminal"}
Node.js, create-expo-app, Metro, Expo Go та симулятори — перший запуск і ініціалізація Nomad.
::

::card{title="5. Структура проєкту" to="/react-native/project-structure-and-conventions" icon="i-lucide-folder-tree"}
app vs src, design tokens, Screen / AppText / Button, псевдоніми @/, платформні суфікси.
::

::card{title="6. Базові компоненти" to="/react-native/core-components" icon="i-lucide-layout-grid"}
View, Text, Image, Pressable, ScrollView, Safe Area, Platform — mock-картки поїздок у Nomad.
::

::card{title="7. Flexbox і layout" to="/react-native/flexbox-and-layout" icon="i-lucide-panels-top-left"}
Колонка за замовчуванням, align/justify, gap, sticky CTA, safe area, клавіатура — shell стрічки поїздок.
::

::card{title="8. StyleSheet і теми" to="/react-native/stylesheet-and-theming" icon="i-lucide-palette"}
StyleSheet, семантичні токени, light/dark, useColorScheme — ThemeProvider у Nomad.
::

::card{title="9. Списки та віртуалізація" to="/react-native/lists-and-virtualization" icon="i-lucide-list"}
FlatList, SectionList, FlashList, pull-to-refresh, empty/error — стрічки поїздок і місць у Nomad.
::

::card{title="10. Форми та валідація" to="/react-native/forms-input-validation" icon="i-lucide-text-cursor-input"}
TextInput, Switch, Checkbox, Slider, Picker, Pressable, date picker, RHF + Zod — форма поїздки в Nomad.
::

::card{title="11. Основи Expo Router" to="/react-native/expo-router-basics" icon="i-lucide-route"}
app/, layout, Tabs і Stack, Link і useRouter, назад, typed routes — оболонка навігації Nomad.
::

::card{title="12. Вкладені навігатори й модалки" to="/react-native/nested-navigators-and-modals" icon="i-lucide-layers"}
Stack у Tabs, presentation modal, auth-групи, guard на back — деталі поїздки в Nomad.
::

::card{title="13. Deep linking і params" to="/react-native/deep-linking-and-params" icon="i-lucide-link"}
Параметри маршруту, scheme, universal links, cold start — deep link на поїздку в Nomad.
::

::
