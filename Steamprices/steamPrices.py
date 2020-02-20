#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types # Tipos para la API del bot.
import time # Librería para hacer que el programa que controla el bot no se acabe.
import tweepy
import os
import sys
from urllib import request, parse
from bs4 import BeautifulSoup

os.environ['TZ'] = 'Europe/Madrid'

#Coloca dentro de las comillas tus claves...
CONSUMER_KEY = 'CONSUMER_KEY' 
CONSUMER_SECRET = 'CONSUMER_SECRET'
ACCESS_KEY = 'ACCESS_KEY'
ACCESS_SECRET = 'ACCESS_SECRET'

#En esta parte nos identifica para poder realizar operaciones
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

TOKEN = 'TOKEN_KEY' # Nuestro tokken del bot (el que @BotFather nos dió).
usuarios = [line.rstrip('\n') for line in open('usuarios.txt')] # Cargamos la lista de usuarios.
bot = telebot.TeleBot(TOKEN) # Creamos el objeto de nuestro bot.

def listener(messages): # Con esto, estamos definiendo una función llamada 'listener', que recibe como parámetro un dato llamado 'messages'.
    for m in messages: # Por cada dato 'm' en el dato 'messages'
        if m.content_type == 'text':
            cid = m.chat.id # Almacenaremos el ID de la conversación.
            print("[" + str(cid) + "]: " + m.text) # Y haremos que imprima algo parecido a esto -> [52033876]: /start
bot.set_update_listener(listener) # Así, le decimos al bot que utilice como función escuchadora nuestra función 'listener' declarada arriba.
bot.polling(none_stop=True) # Con esto, le decimos al bot que siga funcionando incluso si encuentra algún fallo.

@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    if not str(cid) in usuarios: # Con esta sentencia, hacemos que solo se ejecute lo de abajo cuando un usuario hace uso del bot por primera vez.
        usuarios.append(str(cid)) # En caso de no estar en la lista de usuarios, lo añadimos.
        aux = open( 'usuarios.txt', 'a') # Y lo insertamos en el fichero 'usuarios.txt'
        aux.write( str(cid) + "\n")
        aux.close()
 
@bot.message_handler(commands=['steamoffer','Steamoffer']) # Indicamos que lo siguiente va a controlar el comando '/steamoffer'.
def command_steamoffer(entrada): # Definimos una función que resuelva lo que necesitemos.
    cid = entrada.chat.id # Guardamos el ID de la conversación para poder responder.
    separador = entrada.text.split(' ')
    stst = separador[1]
    bot.send_message(cid, 'Función no disponible por el momento')
    #if (stst == "start" or stst == "Start"):
        #bot.send_message(cid, 'Entro!')
        #Aux=True
        #while Aux==True:
            
            #schedule.every().day.at("19:00").do(command_steamoffer)
            #bot.send_message(cid, 'Posteando las ofertas diarias') # Imprimos un texto para que sepa que empieza
            #bot.send_message(cid, 'Entrando en bucle')
            #time.sleep(5)
            #x = tweepy.API(auth)
            #for tweets in x.search(q='steam_games',count=4, result_type='recent'):
                #bot.send_message(cid, tweets.text)
    #elif (stst == "stop" or stst == "Stop"):
        #bot.send_message(cid, 'Parando de postear las ofertas diarias') # Imprimos un texto para que sepa que para
        #bot.send_message(cid, 'Salgo!')
    #else:
        #bot.send_message(cid, 'Meteme un start o stop') # Si no es Start o Stop

@bot.message_handler(commands=['steamprice','Steamprice']) # Indicamos que lo siguiente va a controlar el comando '/steamprice'
def command_steamprice(entrada): # Definimos una función que resuleva lo que necesitemos.
    cid = entrada.chat.id # Guardamos el ID de la conversación para poder responder.
    separador = entrada.text.split(' ')
    msg = separador[1:]
    u = 'http://store.steampowered.com/search/suggest?%s' % (
        parse.urlencode({'term': msg,  # Que buscar. Nombre dle juego
                     'f': 'games',  # Donde buscar, Games: Juegos, Music: Música...
                     'cc': 'ES',  # Region de la store, ES: Euros, RU: Rublos rusos, US: Dólares
                     'lang': 'english'}) #Idioma de la información
    )
    r = request.urlopen(u) #Vemos cual es la url
    t = r.readall() #La leemos
    if len(t) > 0: #Si el texto que hemos dado en term es mayor que 1 letra
        bs = BeautifulSoup(t, "html5lib") #Metemos t en la libreria
        for m in bs.findAll('a', {'class': 'match'}): #Para todos los resultados que encuentre (los 6 por defecto)d
            if (m.find('div', {'class': 'match_price'}).string) == None:
                bot.send_message(cid, m.find('div', {'class': 'match_name'}).string + ' - Precio no disponible ')
            else:
                bot.send_message(cid, m.find('div', {'class': 'match_name'}).string +' - '+m.find('div', {'class': 'match_price'}).string) #Bot manda mensajito
    else: #Si está vacío o no lo encuentra
        bot.send_message( cid, "Game not found") # Si no encuentra el juego o la palabra, ta lue
 
while True: # Ahora le decimos al programa que no se cierre haciendo un bucle que siempre se ejecutará.
    time.sleep(300) # Hacemos que duerma durante un periodo largo de tiempo para que la CPU no esté trabajando innecesáremente.