import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import getpass
import time

# Remove pandas error message
pd.options.mode.chained_assignment = None

def createdatabase(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw)
    if db.is_connected():
        curs = db.cursor()
        curs.execute('SHOW DATABASES')
        result = curs.fetchall()

        for x in result:
            if 'Jobs' == x[0]:
                curs.execute(f'DROP DATABASE Jobs')
                db.commit()
                print('The database already exists. The old one was dropped.')
                time.sleep(1)

        curs.execute("CREATE DATABASE Jobs")
        print('The database was created!')

def creattables(user:str,passw:str):
    db = mysql.connect(
        host="localhost", 
        user=user, 
        passwd=passw, 
        database="Jobs")
    
    curs = db.cursor()

    location = "CREATE TABLE Location(" \
                    "longitude FLOAT(7,4) NOT NULL," \
                    "latitude FLOAT(7,4) NOT NULL," \
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
                    "job_id BIGINT NOT NULL PRIMARY KEY," \
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
    
    # Add data to the Company table
    ## The Company column is the primary key; we don't want to insert duplicates
    company = data.iloc[:,21:]
    company.drop_duplicates(subset='Company', inplace = True)
    curs.executemany("""
    INSERT INTO Company (company, city, state, industry, sector, zip, ceo, website, ticker)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
""", [tuple(row[['Company', 'City', 'State', 'Industry', 'Sector', 'Zip', 'CEO', 'Website', 'Ticker']]) for _, row in company.iterrows()])
    db.commit()
    print('-Company table loaded! ✅')
    
    # Add data to the Location table
    ## The longitude and latitude columns are the primary key; we don't want to insert duplicates 
    location = data.iloc[:, [6, 7, 5, 4]]
    location.drop_duplicates(subset=['latitude', 'longitude'], inplace=True)
    curs.executemany("""
    INSERT INTO Location (longitude, latitude, location, country)
    VALUES (%s, %s, %s, %s);
    """, [tuple(row[['longitude', 'latitude', 'location', 'Country']]) for _, row in location.iterrows()])
    db.commit()
    print('-Location table loaded! ✅')

    # Add data to the Role table
    role = data.iloc[:, [14, 15 ,17 ,19 ,20]]
    role.drop_duplicates(inplace = True)
    curs.executemany("""
    INSERT INTO Role (role, job_title, job_description, skills, responsibilities)
    VALUES (%s, %s, %s, %s, %s);
    """, [tuple(row[['Role', 'Job Title', 'Job Description', 'skills', 'Responsibilities']]) for _, row in role.iterrows()])
    db.commit()
    print('-Role table loaded! ✅')

    # Add data to the Offer table
    offer = data.iloc[:, [0, 2, 8, 11, 12, 13, 18, 9, 1, 3]]
    curs.executemany("""
    INSERT INTO Offer (job_id, work_type, qualifications, preference, benefits, experience, salary_range, contact, contact_person, company_size)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, [tuple(row[['Job Id', 'Work Type', 'Qualifications', 'Preference', 'Benefits', 'Experience', 'Salary Range', 'Contact', 'Contact Person', 'Company Size']]) for _, row in offer.iterrows()])
    db.commit()
    print(' -Offer table loaded! ✅')


user = 'root'
print("""
    _____       __                ______           _                       _    
   |_   _|     [  |              |_   _ `.        / |_                    / |_  
     | |  .--.  | |.--.   .--.     | | `. \ ,--. `| |-',--.   .--.  .---.`| |-' 
 _   | |/ .'`\ \| '/'`\ \( (`\]    | |  | |`'_\ : | | `'_\ : ( (`\]/ /__\\| |   
| |__' || \__. ||  \__/ | `'.'.   _| |_.' /// | |,| |,// | |, `'.'.| \__.,| |,  
`.____.' '.__.'[__;.__.' [\__) ) |______.' \'-;__/\__/\'-;__/[\__) )'.__.'\__/  
                                                                                """)

password = getpass.getpass('Insert password for localhost --> ')
try:
    print("Creating the database...\n")
    time.sleep(1)
    createdatabase(user=user, passw=password)
    time.sleep(1)
    print("Defining tables...\n")
    creattables(user=user, passw=password)
    time.sleep(1.5)
    print("Filling the database...\n")
    dataload(user=user, password=password)
    print("\nDatabase filled!")
except Error as e:
    print(e)