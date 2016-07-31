# -*- coding: utf-8 -*-

import telebot
import re
from telebot import types

token = '268361464:AAG5gx_qSIZG7SRi-48gl4WLkw7XKXM6B_U'
bot = telebot.TeleBot(token)

shares = {
    'Daniil':25,
    'Damir':25,
    'Иван':25,
    'Said':25
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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_message = '/% - Проценты.\n/? - Голоса.\n/- Имя - Голос против.\n/+ Имя - Голос за.'
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(content_types=["text"], regexp=r'^/[?]$')
def vote(message):
    result = ''
    for name in votes.keys():
      result += name
      result += ' - '
      result += diciper(votes[name])
      result += '\n'
    bot.send_message(message.chat.id, result)

def diciper(list):
    return len(list)


@bot.message_handler(content_types=["text"], regexp=r'^/%$')
def percentage(message):
    result = ''
    for name in shares.keys():
      result += name
      result += ' - '
      result += str(shares[name])
      result += '%\n'
    bot.send_message(message.chat.id, result)


@bot.message_handler(content_types=["text"], regexp=r'^/- [a-zA-Zа-яА-Я]+$')
def downvote(message):
    name = message.text[3:]
    if name in shares.keys():
        bot.send_message(message.chat.id, name)
        votesBy[message.from_user.first_name].add(name)
        votesAgainst[name].add(message.from_user.first_name)
        if len(votesAgainst[name]) == 3:
            votesAgainst[name] = set()
            shares[name] -= 3
            for voter in shares.keys():
                print(name, voter)
                if not voter == name:
                    print(name, voter)
                    shares[voter] += 1
                    votesBy[voter].remove(name)
        print(votesBy[message.from_user.first_name])
        print(votesAgainst[name])


@bot.message_handler(content_types=["text"], regexp=r'^/[+] [a-zA-Zа-яА-Я]+$')
def upvote(message):
    name = message.text[3:]
    if name in shares.keys():
        bot.send_message(message.chat.id, name)
        votesBy[message.from_user.first_name].add(name)
        votesFor[name].add(message.from_user.first_name)
        if len(votesFor[name]) == 3:
            votesFor[name] = set()
            shares[name] += 3
            for voter in shares.keys():
                print(name, voter)
                if not voter == name:
                    print(name, voter)
                    shares[voter]-= 1
                    votesBy[voter].remove(name)
        print(votesBy[message.from_user.first_name])
        print(votesFor[name])
    
    
if __name__ == '__main__':
     bot.polling(none_stop=True)