подключение в дбеавере

connect by = URL
url = jdbc:mysql://localhost:6001/bdmysql?allowPublicKeyRetrieval=TRUE
сервер localhost
порт 6001
бд bdmysql
пользователь root
пароль mysqlpass

остальное в файле docker-compose.yml


docker-compose exec -ti vardserver python manage.py createsuperuser
docker network create mynetwork  запускать только 1 раз на компе
docker-compose --build  каждый раз когда надо зафигачить изменения в компостере и посмотреть их на локалке
docker-compose up - запустить компостер

не забываем поменять HOST в settings
'HOST': 'localhost' при python manage.py
'HOST': 'db' в компостере

