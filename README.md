# body storage

```
Задание: Реализовать CRUD сервис, который обрабатывает, принимает и
хранит тела запросов, а также считает количество одинаковых запросов. Тела запросов хранятся по ключу (строка).
Ключ генерируется из параметров тела запроса, методом “ключ+значение”, после чего кодируется в base64.
Требования к API: 
1. Запрос:
 method: POST
 endpoint: api/add
 body: json {...}
Запрос возвращает ключ, по которому можно получить тело данного запроса.
2. Запрос:
 method: GET
 endpoint: api/get?key=key
Возвращается тело искомого запроса, запроса с дополнительным полем “duplicates”.
3. Запрос:
 method: DELETE
 endpoint: api/remove Удаляем запрос по ключу.
4. Запрос:
 method: PUT
 endpoint: api/update
Изменить тело запроса и вернуть новый ключ, обнулить счетчик дубликатов.
5. Запрос:
 method: GET
 endpoint: api/statistic
Получаем % дубликатов от количества общих запросов.
```
---
Запуск:
1. `git clone https://github.com/strpc/body_storage.git`
2. `cd body_storage`
3. `docker-compose -f ./docker-compose.yml up`

---
Документация доступна по адресу `localhost:8000/docs` и описывает 6 урлов:  
`POST /api/body` - сохранение тела запроса.  
`GET /api/body` - получение тела запроса по ключу(ключ передается query-параметром `key`)  
`PUT /api/body/{key}` - обновление тела запроса по ключу.  
`DELETE /api/body/{key}` - удаление тела запроса по ключу.  
`GET /api/statistic` - получение процента дубликатов от общих запросов.  
`GET /healthcheck` - сервисный урл, для проверки работоспособности приложения.  

---
Запуск тестов:
1. `git clone https://github.com/strpc/body_storage.git`
2. `cd body_storage`
3. `docker-compose -f ./docker-compose.tests.yml up --force-recreate --build`

---
Запуск для разработки(внутри контейнера):
1. `git clone https://github.com/strpc/body_storage.git`
2. `cd body_storage`
3. `docker-compose up`
