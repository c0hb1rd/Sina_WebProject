#!/usr/bin/python
# coding=utf-8
import MySQLdb


class database():
    def __init__(self, database):
        self.dbConn = MySQLdb.connect('localhost', 'root', 'hackingme?233333+1s', database)
        self.cursor = self.dbConn.cursor()
        self.eff_count = 0

    def select(self, ls):
        self.eff_count = self.cursor.execute("SELECT * FROM %s", ls)
        return self.cursor.fetchall()

    def insert(self, query):
        pass

    def update(self, query):
        pass

    def delete(self, query):
        pass

    @property
    def getColumns(self):
        return [i[0] for i in self.cursor.description]

    @property
    def getEffCount(self):
        return self.eff_count
