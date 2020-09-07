#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import random
import datetime

class Aphorism(sqlite3.Connection):
    def cursor(self, *args):
        return super().cursor(AphorismCursor)


class AphorismCursor(sqlite3.Cursor):
    def count(self):
        self.execute('SELECT Count() FROM aphorisms')
        return self.fetchone()[0]

    def choose_unique_random(self):
        # choose random id
        number_of_rows = self.count()
        random_id = random.randrange(1, number_of_rows)

        # if does not exist create used_aphorisms table
        self.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="used_aphorisms"')
        exist = self.fetchall()
        if not exist:
            self.execute('CREATE TABLE "used_aphorisms" ("id"INTEGER UNIQUE,PRIMARY KEY("id" AUTOINCREMENT))')

        # check if that aphorism wasn't used and if was, chose next available
        start = random_id
        self.execute('SELECT id FROM used_aphorisms')
        used = self.fetchall()
        while True:
            if random_id == number_of_rows:
                random_id = 1
            if (random_id,) in used:
                random_id += 1
            else:
                break
            if start == random_id:
                print("Baza aforyzmów zostałą wyczerpana.")
                break

        # mark aphorism as used
        self.execute(f'INSERT INTO used_aphorisms SELECT id FROM aphorisms WHERE id = {random_id}')
        return random_id

    def print_aphorism(self, id):
        self.execute(f'SELECT text, author FROM aphorisms WHERE id = {id}')
        aphorism_content = self.fetchone()
        print(f'{aphorism_content[0]} \n\n{aphorism_content[1]}')
        
        # grade aphorism
        mark = input("Jak oceniasz aforyzm w skali od 1 do 5?\n")
        while mark.isdecimal() == False or int(mark) < 0 or int(mark) > 5:
            print("Nie ma takiej oceny. Spróbuj ponownie.")
            mark = input()
        else:
            print("Dziękujemy za ocenę.")

    def date_check(self):
        self.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="date"')
        exist = self.fetchall()
        if not exist:
            self.execute('CREATE TABLE "date" ("year"INTEGER,"month"INTEGER,"day"INTEGER)')
            self.execute('INSERT INTO date (year, month, day) VALUES (0,0,0)')
        self.execute('SELECT * FROM date')
        old_date = self.fetchone()
        current_day = datetime.datetime.now().date()
        if (current_day.year, current_day.month, current_day.day) == old_date:
            return 0
        else:
            self.execute(f'UPDATE date SET year = {current_day.year}, month = {current_day.month}, day = {current_day.day}')
            return 1
