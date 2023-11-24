import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd

user = '...'
password = '...'

def createdatabase(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw)
    curs = db.cursor()
    curs.execute("CREATE DATABASE Jobs")

def creattables(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw, 
        database="Jobs")
    
    curs = db.cursor()

    location = "CREATE TABLE Location(" \
                    "longitude FLOAT(6,4) NOT NULL," \
                    "latitude FLOAT(6,4) NOT NULL," \
                    "location VARCHAR(255) NOT NULL," \
                    "country VARCHAR(255) NOT NULL," \
                    "PRIMARY KEY (longitude, latitude)" \
                    ");"
    
    role = "CREATE TABLE Role("\
                    "responsibilities VARCHAR(255) NOT NULL," \
                    "skills VARCHAR(300) NOT NULL," \
                    "job_description VARCHAR(500) NOT NULL," \
                    "job_title VARCHAR(255) NOT NULL," \
                    "role VARCHAR(255) NOT NULL PRIMARY KEY" \
                    ");"

    # No unique values in this table
    company = "CREATE TABLE Company("\
                    "company VARCHAR(255)," \
                    "city VARCHAR(255)," \
                    "state VARCHAR(255)," \
                    "industry VARCHAR(255)," \
                    "sector VARCHAR(255)," \
                    "zip VARCHAR(100)," \
                    "website VARCHAR(255)," \
                    "ticker VARCHAR(100)," \
                    "ceo VARCHAR(255)" \
                    ");"
    
    offer = "CREATE TABLE Offer("\
                    "job_id INT AUTO_INCREMENT PRIMARY KEY," \
                    "work_type VARCHAR(100)," \
                    "qualifications VARCHAR(100)," \
                    "preference VARCHAR(100)," \
                    "benefits VARCHAR(255)," \
                    "experience VARCHAR(100)," \
                    "salary_range VARCHAR(100)," \
                    "contact VARCHAR(100)," \
                    "contact_person VARCHAR(100)," \
                    "company_size MEDIUMINT" \
                    ");"
    

    
    curs.execute(location)
    curs.execute(role)
    curs.execute(company)
    curs.execute(offer)
    

def dataload(user:str, password:str):
    data = pd.read_csv('jobs_clean.csv', index_col=0)
    data = data.where(pd.notna(data), None)
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=password, 
        database="Jobs")
    
    curs = db.cursor()
    

    for _, row in data.iterrows():
        try:
            curs.execute("""
                INSERT INTO Company (company, city, state, industry, sector, zip, ceo, website, ticker)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (row['Company'], row['City'], row['State'], row['Industry'], row['Sector'], row['Zip'], row['CEO'], row['Website'], row['Ticker']))
            db.commit()
        except Error as err:
            db.rollback()
            print(f"Error: '{err}'")



try:
    print("Creating the database...\n")
    createdatabase(user=user, passw=password)
    print("Defining tables...\n")
    creattables(user=user, passw=password)
    print("Loading the dataset into the database...\n")
    dataload(user=user, password=password)
except Error as e:
    print(e)