# Тестирование проекта Yatube
[Yatube](https://github.com/jullitka/Yatube.git) - социальная сеть с авторизацией, публикациями, комментариями и подписками на авторов статей.

Тестирование Models:
- Проверка отображения значение поля __str__ в объектах моделей.
  
Тестирование URLs:
- Проверьте доступность страниц и названия шаблонов приложения Posts проекта Yatube с учетом прав доступа
- Проверка запрос к несуществующей странице
- Проверка использования правильных html-шаблонов что во view-функциях.
  
Тестирование Views:
- Проверка словаря context, передаваемого в шаблон
- Проверка отображения публикации в соответствующей группе при условии, что при создании публикации она была указана 
- Проверка отображения публикации на главной странице сайта
- Проверка отображения публикации в профайле пользователя
- Проверка, что пост не попал в группу, для которой не был предназначен\
  
Тестирование Forms: 
- Проверка, что при отправки корректной формы создается неовая запись в базе данных.
- Проверка, что при отправки формы редактирования публикации, происходит изменение публикации с соответствующим id в базе данных

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

## Запуск проекта:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/jullitka/Yatube.git
cd Yatube
```
Cоздать и активировать виртуальное окружение:

```
python -m venv env
```
Для Linux
    ```
    source venv/bin/activate
    ```
    
Для Windows
    ```
    source venv/Scripts/activate
    ```

Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Перейти в необходимую директорию и выполнить миграции:
```
cd yatube
python yatube/manage.py makemigrations
python manage.py migrate
```
Создать суперпользователя Django командой:

```
python manage.py createsuperuser
```
и выполнить запрашиваемые в терминале действия

Запустить проект:
```
python manage.py runserver
```
## Авторы
[Юлия Пашкова](https://github.com/Jullitka)
