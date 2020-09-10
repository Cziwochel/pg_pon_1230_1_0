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
        self.execute('CREATE TABLE IF NOT EXISTS"used_aphorisms" ('
                         '"id"	INTEGER UNIQUE,'
                         '"aphorisms_id"	INTEGER UNIQUE,'
                         'PRIMARY KEY("id" AUTOINCREMENT));')

        # check if that aphorism wasn't used and if was, chose next available
        start = random_id
        self.execute('SELECT aphorisms_id FROM used_aphorisms')
        used = self.fetchall()
        while True:
            if (random_id,) in used:
                if random_id == number_of_rows:
                    random_id = 1
                    continue
                random_id += 1
                if start == random_id:
                    print("Baza aforyzmów została wyczerpana.")
                    return -1
            else:
                break


        # mark aphorism as used
        self.execute(f'INSERT INTO used_aphorisms (aphorisms_id) SELECT aphorisms_id FROM aphorisms WHERE aphorisms_id = {random_id}')
        return random_id

    def print_aphorism(self, id=0, grade=0):
        self.execute(f'SELECT text, author FROM aphorisms WHERE aphorisms_id = {id} OR grades = {grade}')
        aphorism_content = self.fetchone()
        print("="*40)
        print(f'\n{aphorism_content[0]} \n\n{aphorism_content[1]}\n')
        print("=" * 40)

    def grade_aphorism(self, id):
        mark = input("Jak oceniasz aforyzm w skali od 1 do 5?\n")
        while mark.isdecimal() is False or int(mark) < 0 or int(mark) > 5:
            print("Nie ma takiej oceny. Spróbuj ponownie.")
            mark = input()
        else:
            print("Dziękujemy za ocenę.")
            self.execute('UPDATE aphorisms SET grades = {} WHERE aphorisms_id = {} '.format(mark, id))

    def favourites(self):
        mark = input("W celu wyświetlenia aforyzmów z podaną oceną wpisz liczbę od 1 do 5: ")
        while mark.isdecimal() is False or int(mark) < 0 or int(mark) > 5:
            print("Nie ma takiej oceny. Spróbuj ponownie.")
            mark = input()
        self.execute(f'SELECT text, author FROM aphorisms WHERE grades = {mark}')
        table = self.fetchall()
        i = 1
        if len(table) == 0:
            print("Nie ma aforyzmów z taką oceną.")
        print("=" * 40)
        for row in table:
            print(f'\n{i}.{row[0]} \n\n{row[1]}\n')
            i += 1
        print("=" * 40)

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
            self.execute(f'UPDATE date SET year = {current_day.year}, month = {current_day.month}, '
                             f'day = {current_day.day}')
            return 1

    def interface(self, id):
        interaction = input('\nJeśli chcesz ocenić aforyzm wpisz - "o"\n'
                                'Jeśli chcesz wyświtlić aforyzmy z daną oceną wpisz - "w"\n'
                                'Jeśli chesz zakończyć pracę programu wpisz - "k"\n')
        while not (interaction == 'k'):
            while not ((interaction == 'k') or (interaction == 'o') or (interaction == 'w')):
                interaction = input('Nie ma takiej komendy spróbuj ponownie')
            if interaction == "o":
                self.grade_aphorism(id)
            elif interaction == "w":
                self.favourites()
            interaction = input('\nJeśli chcesz ocenić aforyzm wpisz - "o"\n'
                                    'Jeśli chcesz wyświetlić aforyzmy z daną oceną wpisz - "w"\n'
                                    'Jeśli chesz zakończyć pracę programu wpisz - "k"\n')

