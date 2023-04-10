# Отправляем уведомления о проверке работ
### Описание
Telegram бот, который отправляет уведомления о проверке работ на сайте [dvmn.org](https://dvmn.org/)

### Стек технологий:
- Python
- python-telegram-bot
- Docker
---


## Запуск проекта на сервере

### Подготовка сервера
- Запустить сервер и подключиться к нему:
```
ssh username@ip_address
```
- Установить обновления apt:
```
sudo apt upgrade -y
```
- Установить docker:
```
sudo apt-get install docker.io -y
```

- Клонировать репозиторий и перейти в него:
```
git clone https://github.com/wombatoff/dvmn_4
cd dvmn_4
```
- Создать файл .env и заполнить его:
```
DVMN_TOKEN=
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
```
- Разверните Docker-контейнер:
```
sudo docker build -t dvmn_checker_bot .
```
```
sudo docker run -d \
  --name dvmn_checker_bot \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  --env-file .env \
  --restart unless-stopped \
  dvmn_checker_bot \
  python dvmn_checker.py
```
### Автор:

[Wombatoff](https://github.com/wombatoff/)
