# **Тестовое задание в компанию Funbox**
## Задание

Реализуйте web-приложение для простого учета посещенных (неважно, как, кем и когда)
ссылок. Приложение должно удовлетворять следующим требованиям.
- Приложение написано на языке Python версии ~> 3.7.
- Приложение предоставляет JSON API по HTTP.
- Приложение предоставляет два HTTP ресурса.

```
Запрос:
POST /visited_links
 {
    "links": [
    "https://ya.ru",
    "https://ya.ru?q=123",
    "funbox.ru",
    "https://stackoverflow.com/questions/11828270/how-to-exit-the-vim-editor"
    ]
}
Ответ:
{
    "status": "ok"
}
```

```
Запрос:
GET /visited_domains?from=1545221231&to=1545217638
Ответ:
{
    "domains": [
    "ya.ru",
    "funbox.ru",
    "stackoverflow.com"
    ],
    "status": "ok"
}
```

- Первый ресурс служит для передачи в сервис массива ссылок в POST-запросе. Временем их посещения считается время получения запроса сервисом.
- Второй ресурс служит для получения GET-запросом списка уникальных доменов,
посещенных за переданный интервал времени.
- Поле status ответа служит для передачи любых возникающих при обработке запроса
ошибок.
- Для хранения данных сервис должен использовать БД Redis.
- Код должен быть покрыт тестами.
- Инструкции по запуску должны находиться в файле README.

## Инструкция по запуску
* Установите зависимости: `pip install -r requirements.txt`
* Запустите redis server
* Настройте данные для подключения к redis-server в файле `Funbox/settings.py` 
* Запустите сервер: `python manage.py runserver`


## Тестировние
###### Информация по тестированию: [![Build Status](https://travis-ci.com/Kaktysig/Funbox.svg?branch=master)](https://travis-ci.com/Kaktysig/Funbox)
###### Информация по покрытию тестами: [![Coverage Status](https://coveralls.io/repos/github/Kaktysig/Funbox/badge.svg)](https://coveralls.io/github/Kaktysig/Funbox)
* Запустите команду: `pytest`
