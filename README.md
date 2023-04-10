# Отправляем уведомления о проверке работ
### Описание
Telegram бот, который отправляет уведомления о проверке работ на сайте [dvmn.org](https://dvmn.org/)

### Стек технологий:
- Python
- python-telegram-bot
- Docker
- Doker-compose
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
- Установить стабильную версию docker-compose: 
```
sudo apt-get install curl -y
sudo curl -SL https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
```
- Применить к файлу права доступа: 
```
sudo chmod +x /usr/local/bin/docker-compose
```
- Проверить версию docker-compose:
```
docker-compose --version
```  
Клонировать репозиторий и перейти в него:
```
git clone https://github.com/wombatoff/dvmn_4
cd dvmn_4
```
Создать файл .env и заполнить его:
```
DVMN_TOKEN=
TELEGRAM_TOKEN=
TELEGRAM_CHAT_ID=
```
Разверните Docker-контейнер:
```
docker-compose up -d --build
```
### Автор:

[Wombatoff](https://github.com/wombatoff/)