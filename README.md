## Сервис авторизации

Нужно дл начала добавить .env файл, для примера предоставлен .env.simple

Поднимаем сервис 
#### docker-compose up -d
### Валидация параметров в запросе происходит с помощью @api.expect(validate=True)
#### Используется связка nginx + gunicorn + gevent
#### Докуменатация и апи flaskrest-x
#### Для работы с jwt используется flask-jwt_extended

### При регистрации пользователя назначаются стандартные права.

## Добавление суперпользователя
### По дефолту у суперпользователя добавится супер-роль с супер-правами

```export FLASK_APP=run.py```
```flask createsuperuser```

- login (обязательный параметр)
- password (обязательный параметр)
- email
- name
- last-name

```flask --help``` - все команды
```flask createsuper --help``` - описание полей для создания суперпользователя

## Для поднятия тестового контейнера:

#### docker-compose -f docker-compose.tests.yaml up -d
