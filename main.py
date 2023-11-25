import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import getpass

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
    
    # Add data to the Company table
    ## The Company column is the primary key; we don't want to insert duplicates
    company_no_duplicates = data.drop_duplicates(subset='Company')
    for _, row in company_no_duplicates[['Company', 'City', 'State', 'Industry', 'Sector', 'Zip', 'CEO', 'Website', 'Ticker']].iterrows():
        try:
            curs.execute("""
                INSERT INTO Company (company, city, state, industry, sector, zip, ceo, website, ticker)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (row['Company'], row['City'], row['State'], row['Industry'], row['Sector'], row['Zip'], row['CEO'], row['Website'], row['Ticker']))
            db.commit()
        except Error as e:
            db.rollback()
            print(f"Error: '{e}'")
    
    # Add data to the Location table
    ## The longitude and latitude columns are the primary key; we don't want to insert duplicates 
    location_no_duplicates = data.drop_duplicates(subset=['longitude', 'latitude'])
    for _, row in location_no_duplicates[['longitude', 'latitude', 'location', 'Country']].iterrows():
        try:
            curs.execute("""
                INSERT INTO Location (longitude, latitude, location, country)
                VALUES (%s, %s, %s, %s);
            """, (row['longitude'], row['latitude'], row['location'], row['Country']))
            db.commit()
        except Error as e:
            db.rollback()
            print(f"Error: '{e}'")

    # Add data to the Role table
    ## The Role column is the primary key; we don't want to insert duplicates
    role_no_duplicates = data.drop_duplicates(subset='Role')
    for _, row in role_no_duplicates[['Role', 'Job Title', 'Job Description', 'skills', 'Responsibilities']].iterrows():
        try:
            curs.execute("""
                INSERT INTO Role (role, job_title, job_description, skills, responsibilities)
                VALUES (%s, %s, %s, %s, %s);
            """, (row['Role'], row['Job Title'], row['Job Description'], row['skills'], row['Responsibilities']))
            db.commit()
        except Error as e:
            db.rollback()
            print(f"Error: '{e}'")

    # Add data to the Offer table
    for _, row in data[['Job Id', 'Work Type', 'Qualifications', 'Preference', 'Benefits', 'Experience', 'Salary Range', 'Contact', 'Contact Person', 'Company Size']].iterrows():
        try:
            curs.execute("""
                INSERT INTO Offer (job_id, work_type, qualifications, preference, benefits, experience, salary_range, contact, contact_person, company_size)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (row['Job Id'], row['Work Type'], row['Qualifications'], row['Preference'], row['Benefits'], row['Experience'], row['Salary Range'], row['Contact'], row['Contact Person'], row['Company Size']))
            db.commit()
        except Error as e:
            db.rollback()
            print(f"Error: '{e}'")


user = 'root'
password = getpass.getpass('Insert password for localhost --> ')
try:
    print("Creating the database...\n")
    createdatabase(user=user, passw=password)
    print("Defining tables...\n")
    creattables(user=user, passw=password)
    print("Loading the dataset into the database...\n")
    dataload(user=user, password=password)
    print("Database filled!")
except Error as e:
    print(e)