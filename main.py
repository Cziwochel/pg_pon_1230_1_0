#!/usr/bin/python
# -*- coding: utf-8 -*-

from aphorism import *
from playsound import playsound

sound = "arp-rise_93bpm_F#_minor.wav"
playsound(sound)

database = sqlite3.connect('./database.db', factory=Aphorism)
cursor = database.cursor()

if cursor.date_check():
    random_id = cursor.choose_unique_random()
    cursor.print_aphorism(random_id)

database.commit()
database.close()