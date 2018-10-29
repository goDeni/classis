# API для управления иерархическим списком (классификатором)

Для запуска нужно установить docker

Собрать образ
```bash
sudo docker build -t classis .
```
Запустить образ
```bash
sudo docker run -d -p 8080:5000 classis
```
Если просто остановить контейнер то изменения в БД не сохраняться.
Чтобы их сохранить нужно выполнить команду
```bash
sudo docker commit CONTAINER_ID classis:latest
```
