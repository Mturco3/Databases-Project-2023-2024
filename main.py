import mysql.connector as mysql
from mysql.connector import Error

# MySQL DB credentials
user = "root"
password = "password"


def createdb(user:str, passw:str):
    db = mysql.connect(host="localhost", user=user, passwd=passw)
    curs = db.cursor()

    databasecreation = "CREATE DATABASE Chess"

    curs.execute(databasecreation)


def creattables(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw, 
        database="chess")
    
    curs = db.cursor()

    company = "CREATE TABLE Location(" \
                       "longitude FLOAT(6,4) NOT NULL" \
                       "latitude FLOAT(6,4) NOT NULL" \
                       "location VARCHAR(100) NOT NULL," \
                       "country VARCHAR(100) NOT NULL" \
                       "PRIMARY KEY (longitude, latitude)" \
                       ");"
    
    curs.execute(company)

