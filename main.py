#!./venv/bin/python3

import logging
import yaml

import bot, zhtw2ko

def main():
    logging.basicConfig(
        format = '%(levelname)s - %(message)s',
        level  = logging.INFO,
    )

    with open('env.yaml', 'r') as file:
        tgbot = bot.bot(yaml.safe_load(file).get('bot').get('token'), handler_cb=zhtw2ko.chinese_to_hangul)
        tgbot.start()

if __name__ == '__main__':
    main()
