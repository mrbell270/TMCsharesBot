# -*- coding: utf-8 -*-

import telebot
import re
from telebot import types

token = '268361464:AAG5gx_qSIZG7SRi-48gl4WLkw7XKXM6B_U'
bot = telebot.TeleBot(token)

shares = {
    'Daniil':0,
    'Damir':0,
    'Иван':0,
    'Said':0
}

votesBy = {
    'Daniil': set(),
    'Damir': set(),
    'Иван': set(),
    'Said': set()
}

votesAgainst = {
    'Daniil': set(),
    'Damir': set(),
    'Иван': set(),
    'Said': set()
}

votesFor = {
    'Daniil': set(),
    'Damir': set(),
    'Иван': set(),
    'Said': set()
}

help_string = '''
/% : Проценты.
/? : Голоса.
/- <Имя> : Голос против.
/+ <Имя> : Голос за.
/сброс, /reset : Сброс голосов.
'''

@bot.message_handler(commands=['start'])
def send_start(message):
    if message.from_user.first_name == 'Иван':
        shares = {
            'Daniil':25,
            'Damir':25,
            'Иван':25,
            'Said':25
        }
        help_message = 'Проценты уравнены\n' + help_string
        bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, help_string)


@bot.message_handler(content_types=["text"], regexp=r'^/-[ ]*[a-zA-Zа-яА-Я]+$')
def downvote(message):
    name = message.text[3:]
    if name in shares.keys():
        bot.send_message(
          message.chat.id,
          "{} votes against {}".format(message.from_user.first_name, name)
        )
        votesBy[message.from_user.first_name].add(name)
        votesAgainst[name].add(message.from_user.first_name)
        if len(votesAgainst[name]) == 3:
            votesAgainst[name] = set()
            shares[name] -= 3
            for voter in shares.keys():
                if not voter == name:
                    shares[voter] += 1
                    votesBy[voter].remove(name)


@bot.message_handler(content_types=["text"], regexp=r'^/[+][ ]*[a-zA-Zа-яА-Я]+$')
def upvote(message):
    name = message.text[3:]
    if name in shares.keys():
        bot.send_message(
          message.chat.id,
          "{} votes for {}".format(message.from_user.first_name, name)
        )
        votesBy[message.from_user.first_name].add(name)
        votesFor[name].add(message.from_user.first_name)
        if len(votesFor[name]) == 4:
            votesFor[name] = set()
            shares[name] += 3
            for voter in shares.keys():
                if not voter == name:
                    shares[voter]-= 1
                    votesBy[voter].remove(name)


@bot.message_handler(commands=['reset', 'сброс'])
def devote(message):
    name = message.from_user.first_name
    votesBy[name] = set()
    for each in votesFor.keys():
        if name in votesFor[each]:
            votesFor[each].remove(name)
    for each in votesAgainst.keys():
        if name in votesAgainst[each]:
            votesAgainst[each].remove(name)


@bot.message_handler(commands=['%'])
def percentage(message):
    result = ''
    for name in shares.keys():
      result += name
      result += ' - '
      result += str(shares[name])
      result += '%\n'
    bot.send_message(message.chat.id, result)


@bot.message_handler(commands=['?'])
def votesInfo(message):
    name = message.from_user.first_name
    result = name
    result += "'s votes:\n"
    for vote in votesBy[name]:
      result += vote
      result += '\n'
    result += 'Votes against '
    result += name
    result += ':\n'
    for vote in votesAgainst[name]:
      result += vote
      result += '\n'
    result += 'Votes for '
    result += name
    result += ':\n'
    for vote in votesFor[name]:
      result += vote
      result += '\n'
    bot.send_message(message.chat.id, result)
    
    
bot.polling(none_stop=True)