# API интерфейс S3 для базовых операций с файлами на Django

## Описание:
Сервис позволяет осуществлять загрузку файлов и скачивание файлов с помощью объектного хранилища Minio

## Cценарий работы:
Пользователь:
1. Регистрирует аккаунт
2. Логинится и получает токен для оуществления операциий с файлами
3. Загружает любой файл по ссылке `http://host:port/api/v1/auth/users/`
4. Просматривает список ранее загруженных файлов по ссылке `http://host:port/api/v1/list/`
5. Получает JSON с ссылками на все ранее загруженные файлы по ссылке`http://host:port/api/v1/download/`

## Порядок установки 

### Клонируем репозиторий `git clone https://github.com/Khristoforr/task.git`

### Меняем переменные окружения `.env.dev`

### Запускаем сервисы  `docker-compose up -d --build`

### Просмотр логов `docker-compose logs`