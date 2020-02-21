# Парсер книг

Парсер скачивает книги категории "Фантастика" с сайта бесплатной библиотеки [http://tululu.org]( http://tululu.org).


### Установка

Python 3.8 должен быть уже установлен. 
Затем используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```

### Использование

Переходим в каталог с программой
Команда -

```
python parse_tululu_category.py
```

Можно также запускать с аргументами, кроме текста сообщения аргументы имеют параметры по умолчанию.

```
usage: parse_tululu_category.py [-h] [-start_page START_PAGE] [-end_page END_PAGE]

optional arguments:
  -h, --help            show this help message and exit
  -start_page START_PAGE, --start_page START_PAGE
                        First lib page for parsing (default: 1)
  -end_page END_PAGE, --end_page END_PAGE
                        Last lib page for parsing (default: 1)
```


```
python parse_tululu_category.py --start_page 300 --end_page 400
```
Парсер скачает страницы с 300 по 400 включительно: создаст в каталоге с программой json файл с описанием книг и каталоги **images** для обложек в одинаковом формате, **books** для текстов книг соотвественно.

```
python parse_tululu_category.py --end_page 4
```

Будут скачены страницы с 1 по 4 включительно


### Особенности
Программа выводит лог своей работы

```
INFO:root:http://tululu.org/txt.php?id=18941 downloaded & saved as books/7-я книга_День Откровения.txt
INFO:root: Process with G:\playground\parse_online_library\images/7-я книга_День Откровения.jpg
INFO:root:http://tululu.org/images/nopic.gif downloaded & saved as G:\playground\parse_online_library\images/7-я книга_День Откровения.jpg
INFO:root:process with href='http://tululu.org/b18941/' - 7-я книга_День Откровения
INFO:root:http://tululu.org/txt.php?id=18942 downloaded & saved as books/8-я книга_Полет Уригленны.txt
INFO:root: Process with G:\playground\parse_online_library\images/8-я книга_Полет Уригленны.jpg
INFO:root:http://tululu.org/images/nopic.gif downloaded & saved as G:\playground\parse_online_library\images/8-я книга_Полет Уригленны.jpg
INFO:root:process with href='http://tululu.org/b18942/' - 8-я книга_Полет Уригленны.
INFO:root:info_books_file='library.json' books specification downloaded & saved!
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

