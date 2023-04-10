import logging
import os
import textwrap
import time
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

import requests
import telegram
from environs import Env

bot_logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def main():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    log_file = os.path.join("logs", "log_file.log")
    file_handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    bot_logger.setLevel(logging.DEBUG)
    bot_logger.addHandler(file_handler)

    env = Env()
    env.read_env()

    dvmn_url_long_poll = "https://dvmn.org/api/long_polling/"
    dvmn_token = env.str("DVMN_TOKEN")
    telegram_token = env.str("TELEGRAM_TOKEN")
    telegram_chat_id = env.int("TELEGRAM_CHAT_ID")

    timestamp = 0
    wait_time = 5 * 60
    dvmn_checker_bot = telegram.Bot(token=telegram_token)

    telegram_handler = TelegramLogsHandler(dvmn_checker_bot, telegram_chat_id)
    telegram_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    telegram_handler.setLevel(logging.ERROR)
    bot_logger.addHandler(telegram_handler)

    bot_logger.setLevel(logging.DEBUG)

    while True:
        try:
            raw_response = requests.get(
                dvmn_url_long_poll,
                headers={"Authorization": f"Token {dvmn_token}"},
                params={"timestamp": timestamp},
                timeout=180,
            )
            raw_response.raise_for_status()
            review_status_response = raw_response.json()
            bot_logger.debug(review_status_response)

            if "new_attempts" in review_status_response:
                for attempt in reversed(review_status_response["new_attempts"]):
                    submitted_at = datetime.fromtimestamp(attempt["timestamp"])
                    submitted_at = submitted_at.strftime("%d.%m.%Y %H:%M")
                    if attempt["is_negative"]:
                        message = textwrap.dedent(f"""
                            Работа \"{attempt['lesson_title']}\" 
                            проверена {submitted_at}, в работе есть ошибки.                        
                            {attempt['lesson_url']}
                        """)
                    else:
                        message = textwrap.dedent(f"""
                            Работа \"{attempt['lesson_title']}\" 
                            проверена {submitted_at}, все бенч.
                            {attempt['lesson_url']}
                        """)
                    dvmn_checker_bot.send_message(text=message, chat_id=telegram_chat_id)
                    bot_logger.info("Сообщение отправлено.")
                timestamp = review_status_response["last_attempt_timestamp"]
        except requests.exceptions.ReadTimeout:
            bot_logger.debug("Запрос превысил таймаут.")
            continue
        except (
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError,
                telegram.error.Unauthorized,
        ) as error:
            error_name = error.__class__.__name__
            error_message = {
                "HTTPError": "Ошибка HTTP запроса.",
                "ConnectionError": "Ошибка подключения к серверу.",
                "Unauthorized": "Ошибка авторизации. Проверьте правильность токена и chat_id.",
            }.get(error_name, f"Неизвестная ошибка: {error_name}")
            bot_logger.error(error_message)
            bot_logger.debug(f"Ожидание {wait_time} секунд перед следующей попыткой.")
            time.sleep(wait_time)


if __name__ == "__main__":
    main()
