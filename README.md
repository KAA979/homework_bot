# Бот-ассистент
### Описание проекта:
**Telegram-бот**, который обращается к API сервиса Практикум.Домашка и узнаёт статус вашей домашней работы:
- раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы;
- при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram;
- логирует свою работу и сообщает вам о важных проблемах сообщением в Telegram.

**Статусы домашней работы**:

- **reviewing**: работа взята в ревью;
- **approved**: ревью успешно пройдено;
- **rejected**: в работе есть ошибки, нужно поправить.

Если домашку ещё не взяли в работу — её не будет в выдаче.

**Реализован с помощью [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot).**
### Инструкция по развёртыванию:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/KAA979/homework_bot.git
```
```
cd homework_bot
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Создать в корне проекта файл .env и сохранить в нём переменные окружения:
```
touch .env
```
- PRACTICUM_TOKEN - токен Я.Практикума. Можно получить [здесь](https://oauth.yandex.ru/authorize?response_type=token&client_id=1d0b9dd4d652455a9eb710d450ff456a).
- TELEGRAM_TOKEN - токен телеграм-бота. Получается при создании бота [здесь](https://t.me/BotFather).
- TELEGRAM_CHAT_ID - идентификатор чата с пользователем в Telegram. Можно получить [здесь](https://t.me/userinfobot).
```
PRACTICUM_TOKEN=...
TELEGRAM_TOKEN=...
CHAT_ID=...
```
Запускаем бота
```
python homework.py
```
Автор: [Андрей Казанджян](https://github.com/KAA979) &#128013;
