# -*- coding: utf-8 -*-
from peewee import Model, SqliteDatabase
from peewee import CharField, IntegerField, ForeignKeyField, DateField, BooleanField
import os

db = SqliteDatabase('music.db')


class Song(Model):
    name = CharField()
    duration = IntegerField()
    path = CharField()

    class Meta:
        database = db


class Vote(Model):
    song = ForeignKeyField(Song, related_name="votes")
    datetime = DateField()

    class Meta:
        database = db


class Config(Model):
    running = BooleanField()

    class Meta:
        database = db

if not os.path.isfile("music.db"):
    Song.create_table()
    Vote.create_table()
