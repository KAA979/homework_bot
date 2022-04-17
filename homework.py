import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

from exceptions import (GetApiAnswerError, NoResponseError,
                        UndocumentedStatusError)

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = 5197639266

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        logging.FileHandler('my_logger.log', encoding=None, delay=False),
        logging.StreamHandler(sys.stdout)
    ],
    format='%(asctime)s, %(levelname)s, %(message)s'
)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(TELEGRAM_CHAT_ID, message)
        info_message = f'Отправлено сообщение: {message}'
        logging.info(info_message)
    except telegram.TelegramError:
        logging.error('Сбой Telegram при доступе к эндпоинту')
        raise telegram.TelegramError('Сбой Telegram при доступе к эндпоинту')


def get_api_answer(current_timestamp):
    """Делает запрос к единственному эндпоинту API-сервиса."""
    timestamp = current_timestamp or int(time.time())
    params = {'from_date': timestamp}
    response = requests.get(url=ENDPOINT, headers=HEADERS, params=params)
    if response.status_code != HTTPStatus.OK:
        logging.error('Эндпоинт недоступен')
        raise GetApiAnswerError('Эндпоинт недоступен')
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    if not response:
        raise NoResponseError('Нет ответа от API')
    if type(response) is not dict:
        raise TypeError('Формат ответа отличается от словаря')
    if 'homeworks' not in response:
        logging.error('В ответе нет ключа homeworks')
        raise KeyError('В ответе нет ключа homeworks')
    homework = response['homeworks']
    return homework


def parse_status(homework):
    """Извлекает из информации о конкретной
    домашней работе статус этой работы
    """
    homework_name = homework['homework_name']
    homework_status = homework['status']
    if 'homework_name' not in homework:
        logging.error('В ответе нет имени домашней работы')
        raise KeyError('В ответе нет имени домашней работы')
    else:
        homework_name = homework.get('homework_name')
    if 'status' not in homework:
        logging.error('В ответе нет данных о статусе')
        raise KeyError('В ответе нет данных о статусе')
    else:
        homework_status = homework.get('status')
    if homework_status not in HOMEWORK_STATUSES:
        logging.error('Недокументированный статус домашней работы')
        raise UndocumentedStatusError(
            'Недокументированный статус домашней работы'
        )
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверяет доступность переменных окружения."""
    return all([PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID])


def main():
    """Основная логика работы бота."""
    if check_tokens() is False:
        logging.critical('Отсутствуют переменные окружения!')
        exit()
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if homeworks and len(homeworks):
                for homework in homeworks:
                    message = parse_status(homework[0])
                    send_message(bot, message)
            else:
                logging.debug('Отсутствуют новые статусы')
            current_timestamp = response['current_date']
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            send_message(bot, message)
        finally:
            time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
