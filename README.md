# Парсер книг

Парсер скачивает книги категории "Фантастика" с сайта бесплатной библиотеки [http://tululu.org]( http://tululu.org).


### Установка

Python 3.8 должен быть уже установлен. 
Затем используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```

### Использование

Переходим в каталог с программой.
Команда -

```
python parse_tululu_category.py
```

Можно также запускать с аргументами, кроме текста сообщения аргументы имеют параметры по умолчанию.

```
usage: parse_tululu_category.py [-h] [-start_page START_PAGE] [-end_page END_PAGE] [-dest_folder DEST_FOLDER] [-json_path JSON_PATH] [-skip_imgs] [-skip_txts]

optional arguments:
  -h, --help            show this help message and exit
  -start_page START_PAGE, --start_page START_PAGE
                        First lib page for parsing (default: 1)
  -end_page END_PAGE, --end_page END_PAGE
                        Last lib page for parsing (default: 1)
  -dest_folder DEST_FOLDER, --dest_folder DEST_FOLDER
                        download destination folder (default: )
  -json_path JSON_PATH, --json_path JSON_PATH
                        final json results path (default: )
  -skip_imgs, --skip_imgs
                        skip images download (default: False)
  -skip_txts, --skip_txts
                        skip txt files download (default: False)
```


```
python parse_tululu_category.py --start_page 300 --end_page 400
```
Парсер скачает страницы **с 300 по 400 включительно**: создаст в каталоге с программой json файл с описанием книг и каталоги **images** для обложек в одинаковом формате, **books** для текстов книг соотвественно.


```
python parse_tululu_category.py --end_page 20
```
Парсер скачает страницы **с 1 по 20 включительно**.


```
python parse_tululu_category.py --skip_imgs --start_page 19 --end_page 21 --dest_folder MY_FOLDER --json_path MY_JSON_FOLDER 
```
Парсер скачает страницы **с 19 по 21 включительно**, но пропустит обложки, тексты сохранятся по пути **MY_FOLDER**, json файл с описанием книг сохранится по пути **MY_JSON_FOLDER**.


### Особенности
Программа выводит лог своей работы -

```
INFO:root:http://tululu.org/txt.php?id=19632 downloaded & saved as MY_FOLDER\books\Бартер.txt (text/plain; charset="utf-8")
INFO:root: Process with G:\playground\parse_online_library\MY_FOLDER\images\Бартер.jpg
INFO:root:http://tululu.org/images/nopic.gif downloaded & saved as MY_FOLDER\images\Бартер.jpg (image/gif)
INFO:root:process with href='http://tululu.org/b19632/' - Бартер
INFO:root:http://tululu.org/txt.php?id=19634 downloaded & saved as MY_FOLDER\books\Бархатный сезон.txt (text/plain; charset="utf-8")
INFO:root: Process with G:\playground\parse_online_library\MY_FOLDER\images\Бархатный сезон.jpg
INFO:root:http://tululu.org/images/nopic.gif downloaded & saved as MY_FOLDER\images\Бархатный сезон.jpg (image/gif)
INFO:root:process with href='http://tululu.org/b19634/' - Бархатный сезон
INFO:root:json_books_file='MY_JSON_FOLDER\\library.json' book specifications downloaded & saved!
```

### Создание страниц сайта с полученными книгами 

Пример -

https://theegid.github.io/parse_online_library/pages/index1.html

Команда - 

```
python render_website.py
```

Аргументы настроек, дефолтные настраиваются через settings.ini в основном каталоге
```
usage: render_website.py [-h] 
                        [-template_folder TEMPLATE_FOLDER] 
                        [-template_file TEMPLATE_FILE] 
                        [-library_filepath LIBRARY_FILEPATH] 
                        [-pages_folder PAGES_FOLDER]          
                        [-amount_on_page AMOUNT_ON_PAGE]
```
Лог создания страниц -

```
INFO:root:Create Page: pages/index1.html
INFO:root:Create Page: pages/index2.html
INFO:root:Create Page: pages/index3.html
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).

