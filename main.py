#!/usr/bin/python
# -*- coding: utf-8 -*-

from aphorism import *
from playsound import playsound

sound = "arp-rise_93bpm_F#_minor.wav"
playsound(sound)

database = sqlite3.connect('./database.db', factory=Aphorism)
cursor = database.cursor()

cursor.execute('SELECT aphorisms_id FROM used_aphorisms ORDER BY id DESC LIMIT 1')
last_aphorism = cursor.fetchone()
if last_aphorism:
    random_id = last_aphorism[0]

if cursor.date_check():
    random_id = cursor.choose_unique_random()
    cursor.print_aphorism(random_id)

database.commit()
database.close()
