<h4 align="center">Вертикальне об'єднання jpg секвенцій<br>Наприклад для перекладу манхв</h4>

<h1></h1>


<p align="center">
  <a href="#можливості">Можливості</a> •
  <a href="#установка">Установка</a> •
  <a href="#використання">Використання</a> • 
  <a href="#допомогапитання">Допомога/Питання</a> •
  <a href="#nехнічнівимоги">Технічні вимоги</a> •
  <a href="#творці">Творці</a> •
  <a href="#gallery">Галерея</a>
</p>

<h1></h1>


# ImageSplitter
## Можливості  
- **Об'єднання зображень** — Дозволяє відкрити та переглянути набір зображень у суцільному форматі
- **Автоматичне розділення** —  Функція автоматичного розділення суцільного зображення на відрізки вказаної висоти
- **Користувацькі розділювачі** —  Є можливість розставлення своїх розділювачів за потреби
- **Універсальність** — Приймає будь-яку кількість зображень, за умови однакової шири цих зображень
- **Активна розробка** — Будуть додаватися нові функції та прислухуватимуся до відгуків користувачів
- **Український інтерфейс** — Виключно.

## Установка

### Завантажити реліз

Можна просто завантажити реліз. Запустити `.exe`, готово.

### Використання серцевого коду
Завантажте потрібні залежності для проєкту. Переконайтеся, що встановлена версія Python >= 3.8 64bit
 ```
 pip install -r requirements.txt
 або
 pip3 install -r requirements.txt
 ```
Після завантаження коду потрібно запустити консоль у місці розташування `main.py`. 
Запуск програми:
 ```
 python .\main.py
 або
 python3 .\main.py
 ```

## Використання
 [![Відео-інструкція на ютубі:](https://img.shields.io/badge/-Відеоінструкція_на_ютубі-090909?style=for-the-badge&logo=YouTube)]()<br/>
 ### Текстова інструкція
У текстове поле Шлях потрібно ввести директорію де розсташовується потрібна папка. У директорії повинна бути папка Raw у якій зберігатимуться зображення, які потрібно об'єднати.
Приблизна структура папко:
```
├───Chapters<br>
│   ├───chapter-1<br>
│   │   ├───Raw<br>
│   │   └───Translated<br>
│   └───chapter-2<br>
│       ├───Raw<br>
│       └───Translated<br>
...
```
>Папка `Translated` створена для прикладу. Вона не є обов'язковою.

Після натискання `Завантажити` програма створить tmp файли у місці вхідних зображень, щоб надалі завантажувати їх швидше. Папку можна видалити після використання. Вона не впливає на роботу програми, лише на швидкість (рекомендується видаляти її після завершення роботи з цим розділом, адже потім, за необхідності, вона створиться знову).

### Навігація

- Вікна гортаються паралельно активному вікну
- Вибір автоматичного розставляння розділювачів обмежений від 4 до 14 тис. пікселів, адже фотошоп не експортую формати jpg більше 14, а зображень менше 4тис. буде забагато
- Розставлення розділювачів мишкою доступне після натискання відповідного прапорця. Розділювачі можна ставити тіьки у найбільшому вікні коли воно активне. Тобто активуємо його лівим клацанням миші, а потім ставимо розділювач за допомогою Shift+ЛКМ.
- Таблиця розділювачів, яка знаходиться праворуч навігації, дозволяє швидко "скролити" до нього після натискання на назву в першому стовпці. Другий стовпець показує Відстань між розідлювачів. Вона потрібна для кращої орієнтації. Останній, третій стовпець містить кнопку для видалення розділювача. Під таблицею знаходиться кнопка "Очистити ВСЕ", яка прибирає всі розділення.
- Розділення підсвічуються червоною стрілкою, яка не буде експортована і існує лише у редакторі. Товщина розділення є умовною та є такою лише для кращої видимоті у редакторі, розділення відбуватиметься товщиною в 1 піксель.
- "Експорт" обробить та розділить зображення вказаним Вами чином у папку Split

## Допомога/Питання
- Запити щодо помилок можна створювати у вкладці Issues
- Для особистих звернень та консультації:
    - Discord: bigidan
    - Telegram:

### Планується додавання:
- Вибору вхідної папки замість Raw
- Експорт у нестандартну папку
- Підтримка зображень інших форматів

### Технічні вимоги
На поточний момент підтримується виключно Windows:<br>
| Platform | Graphics API | Newest Version |
|:---------|:-------------|:---------------|
| **Windows 10** | _DirectX 11_ | [![PYPI](https://img.shields.io/pypi/v/dearpygui)](https://pypi.org/project/dearpygui/) |

<br>У майбутньому планується підтримка Linux

## Творці

- Розроблено [Богданом/Bigidun/Bigidan](https://github.com/Bigidan), у першу чергу для використання командами перекладу манхв.
- Використана графічна бібліотека [DearPyGui](https://github.com/hoffstadt/DearPyGui/tree/master)

