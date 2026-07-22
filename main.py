#!./venv/bin/python3

import logging
import yaml

import bot
from pybopomofo2hangul import bopomofo_to_hangul

def main():
    logging.basicConfig(
        format = '%(levelname)s - %(message)s',
        level  = logging.INFO,
    )

    with open('env.yaml', 'r') as file:
        tgbot = bot.bot(yaml.safe_load(file).get('bot').get('token'), handler_cb=bopomofo_to_hangul)
        tgbot.start()

if __name__ == '__main__':
    main()
