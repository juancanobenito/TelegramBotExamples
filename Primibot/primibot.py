#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types # Tipos para la API del bot.
import time
from urllib import request
from bs4 import BeautifulSoup

TOKEN = 'TOKEN_BOT'
bot = telebot.TeleBot(TOKEN)

def listener(messages):
    for m in messages:
        if m.content_type == 'text':
            cid = m.chat.id
            print("[" + str(cid) + "]: " + m.text)
 
bot.set_update_listener(listener)
bot.polling(none_stop=True)
 
@bot.message_handler(commands=['resultados','Resultados']) 
def command_resultados(m):
    cid = m.chat.id 
    rq = request.Request('http://www.loteriasyapuestas.es/es/la-primitiva', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'})
    r = request.urlopen(rq)
    t = r.readall()
    bs = BeautifulSoup(t, "html5lib")
    regIzq = bs.find('div', {'class': 'cuerpoRegionIzq'})
    regDer = bs.find('div', {'class': 'cuerpoRegionDerecha'})
    primitiva = ''
    for n in regIzq.find('ul').findAll('li'):
        primitiva += n.string.strip() + ' '
    bolasPeq = regDer.findAll('span', {'class': 'bolaPeq'})
    complementario = bolasPeq[0].string.strip()
    reintegro = bolasPeq[1].string.strip()
    joker = regIzq.find('div', {'class': 'joker'}).find('span', {'class': 'numero'}).string.strip()
    bot.send_message(cid, 'Número premiado: ' + primitiva)
    bot.send_message(cid, 'Complementario: ' + complementario)
    bot.send_message(cid, 'Reintegro: ' + reintegro)
    bot.send_message(cid, 'Joker: ' + joker)
    
@bot.message_handler(commands=['premios','Premios']) 
def command_premios(m):
    cid = m.chat.id 
    #u='http://www.loteriasyapuestas.es/es/la-primitiva'
    rq = request.Request('http://www.loteriasyapuestas.es/es/la-primitiva', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'})
    r = request.urlopen(rq)
    t = r.readall()
    bs = BeautifulSoup(t, "html5lib")
    section = bs.find('div', {'class': 'masInfo'})
    url = section.find('a').get('href')
    urlparch = url[18:]
    urlFinal = 'http://www.loteriasyapuestas.es/es/la-primitiva'+urlparch
    rd = request.urlopen(urlFinal)
    td = rd.readall()
    bsd = BeautifulSoup(td, "html5lib")
    bot.send_message(cid, 'Puedes ver la lista de acertantes aquí: ' + urlFinal)
    
while True:
    time.sleep(3600)