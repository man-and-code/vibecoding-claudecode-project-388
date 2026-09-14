#!/usr/bin/env python3
"""Отправка одного текстового сообщения в Telegram.

Запуск:
    python3 send.py "текст сообщения"

Настройки берутся только из переменных окружения TELEGRAM_BOT_TOKEN и
TELEGRAM_CHAT_ID. Файл .env не читается и не создаётся.

Используется только стандартная библиотека Python.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_URL = "https://api.telegram.org/bot{token}/sendMessage"
TIMEOUT = 30


def fail(message):
    """Печатает понятную ошибку в stderr и завершает процесс с кодом 1."""
    print("Ошибка: {}".format(message), file=sys.stderr)
    sys.exit(1)


def hide_token(text, token):
    """Убирает токен бота из текста, чтобы он не попал в вывод об ошибке."""
    if token and token in text:
        return text.replace(token, "<TELEGRAM_BOT_TOKEN>")
    return text


def read_text_argument(argv):
    """Возвращает текст сообщения из аргументов командной строки."""
    if len(argv) < 2:
        fail(
            "не передан текст сообщения. "
            'Запуск: python3 send.py "текст сообщения"'
        )
    if len(argv) > 2:
        fail(
            "передано несколько аргументов, ожидается ровно один. "
            'Текст с пробелами нужно взять в кавычки: python3 send.py "текст сообщения"'
        )
    text = argv[1]
    if not text.strip():
        fail("текст сообщения пустой")
    return text


def read_settings():
    """Возвращает токен бота и идентификатор чата из переменных окружения."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    missing = []
    if not token:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not chat_id:
        missing.append("TELEGRAM_CHAT_ID")
    if missing:
        fail(
            "не заданы переменные окружения: {}. "
            "Задайте их в окружении перед запуском.".format(", ".join(missing))
        )

    return token, chat_id


def send_message(token, chat_id, text):
    """Отправляет сообщение через Telegram Bot API и возвращает ответ API."""
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text})
    request = urllib.request.Request(
        API_URL.format(token=token),
        data=payload.encode("utf-8"),
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        description = body
        try:
            description = json.loads(body).get("description", body)
        except ValueError:
            pass
        fail(
            hide_token(
                "Telegram API вернул HTTP {}: {}".format(error.code, description),
                token,
            )
        )
    except urllib.error.URLError as error:
        fail(
            hide_token(
                "не удалось соединиться с api.telegram.org: {}".format(error.reason),
                token,
            )
        )
    except OSError as error:
        fail(hide_token("сетевая ошибка: {}".format(error), token))

    try:
        result = json.loads(body)
    except ValueError:
        fail(hide_token("Telegram API вернул не JSON: {}".format(body), token))

    if not result.get("ok"):
        fail(
            hide_token(
                "Telegram API отклонил запрос: {}".format(
                    result.get("description", body)
                ),
                token,
            )
        )

    return result


def main():
    text = read_text_argument(sys.argv)
    token, chat_id = read_settings()
    send_message(token, chat_id, text)
    print("Отправлено.")


if __name__ == "__main__":
    main()
