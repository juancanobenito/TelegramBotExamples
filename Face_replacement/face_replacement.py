#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import sys
import cv2
import logging
import telebot


if 'CHANGE_FACE' not in os.environ:
    print("Environment variable 'CHANGE_FACE' not defined.", file=sys.stderr)
    exit(1)


logger = telebot.logger
logger.setLevel(logging.INFO)

bot = telebot.TeleBot(os.environ['CHANGE_FACE'], skip_pending=True)

botname = bot.get_me().username

image_to_replace = cv2.imread('image.png', -1)
img_ext = '_replaced.png'

cc_scale_factor = 1.2
cc_min_neighbors = 5
cc_min_size = (20, 20)
cc_flags = cv2.CASCADE_SCALE_IMAGE | cv2.CASCADE_DO_ROUGH_SEARCH

adaptative = True
clahe_clip = 3.0
clahe_tile = (8, 8)


def face_replacement(img_file):
    face_cc = cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml')

    img = cv2.imread(img_file)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if adaptative:
        clahe = cv2.createCLAHE(clipLimit=clahe_clip, tileGridSize=clahe_tile)
        gray = clahe.apply(gray)
    else:
        gray = cv2.equalizeHist(gray)

    faces = face_cc.detectMultiScale(gray,
                                     scaleFactor=cc_scale_factor,
                                     minNeighbors=cc_min_neighbors,
                                     minSize=cc_min_size,
                                     flags=cc_flags)

    for (x, y, w, h) in faces:
        image_rescale = cv2.resize(image_to_replace, (w, h))

        for c in range(0, 3):
            img[y:y+h, x:x+w, c] = image_rescale[:, :, c] * \
                                   (image_rescale[:, :, 3] / 255.0) + \
                                   img[y:y+h, x:x+w, c] * \
                                   (1.0 - (image_rescale[:, :, 3] / 255.0))

    n_faces = len(faces)
    if n_faces > 0:
        cv2.imwrite(img_file+img_ext, img)

    return n_faces


@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    cid = m.chat.id

    f_id = None
    b_size = 0
    for p in m.photo:
        t_size = p.height * p.width
        if t_size > b_size:
            b_size = t_size
            f_id = p.file_id

    f_info = bot.get_file(f_id)
    f_download = bot.download_file(f_info.file_path)

    with open(f_id, 'wb') as f:
        f.write(f_download)

    n_faces = face_replacement(f_id)

    if n_faces > 0:
        bot.send_chat_action(cid, 'upload_photo')

        bot.send_photo(cid,
                       open(f_id+img_ext, 'rb'),
                       caption='TADAAAAAAAA.' %
                       ('s' if n_faces > 1 else ''))

        try:
            os.unlink(f_id+img_ext)
        except Exception as e:
            logger.error(e)

    elif cid > 0:
        bot.send_chat_action(cid, 'typing')
        bot.send_message(cid, 'No faces detected.')

    try:
        os.unlink(f_id)
    except Exception as e:
        logger.error(e)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(m):
    cmd = m.text.split()[0]
    if '@' in cmd and cmd.split('@')[-1] != botname:
        return

bot.polling(none_stop=True)