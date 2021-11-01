from config import TOKEN
from datetime import datetime, timedelta
import http.client
import telebot
import json


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start_message(message):
        bot.send_message(message.chat.id, 'Привет чудик')

    @bot.message_handler(content_types=['text'])
    def send_text(message):
        if message.text.lower() == 'result':
            conn = http.client.HTTPSConnection("free-nba.p.rapidapi.com")
            headers = {
                'x-rapidapi-host': "free-nba.p.rapidapi.com",
                'x-rapidapi-key': "cae66e04femsh211f588ec99d043p11ca2fjsn185d7afefe3a"
            }
            conn.request("GET", "/games?start_date=" + str(datetime.now().date() - timedelta(days=3)) + "&end_date=" +
                         str(datetime.now().date() - timedelta(days=1)), headers=headers)
            res = conn.getresponse()
            data = res.read()
            data = json.loads(data)
            lst = []

            for _ in data['data']:
                game_date = _['date'].replace('T00:00:00.000Z', '')
                home_team = _['home_team']['name']
                home_team_score = _['home_team_score']
                visitor_team_score = _['visitor_team_score']
                visitor_team = _['visitor_team']['name']
                lst.append(f'{game_date} {home_team} {home_team_score} - {visitor_team_score} {visitor_team}')

            str_ = ''
            for _ in lst:
                str_ = str_ + _ + '\n'

            bot.send_message(message.chat.id, str_)

    bot.polling()


if __name__ == '__main__':
    telegram_bot(TOKEN)
