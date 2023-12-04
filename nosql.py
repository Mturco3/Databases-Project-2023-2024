import pandas as pd
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
jobs_db = client.Jobs
jobs_collection = jobs_db.jobs_collection
printer = pprint.PrettyPrinter()

def load_data(data):
    jobs_dict = data.to_dict(orient = 'records')

    docs = []
    for job in jobs_dict:  
    
        doc = {
        "job_Id": job['Job Id'],
        "work_type": job['Work Type'],
        "qualifications": job['Qualifications'],
        "preference": job['Preference'],
        "benefits": job['Benefits'],
        "experience": job['Experience'],
        "salary_range":job['Salary Range'],
        "contact":job['Contact'],
        "contact_person":job['Contact Person'],
        "company_size": job['Company Size'],
        "job_posting_date": job['Job Posting Date'],
        "job_portal": job['Job Portal'],
        "Role": {
            "role": job['Role'],
            "job_title": job['Job Title'],
            "job_descritpion": job['Job Description'],
            "skills":job['skills'],
            "responsibilities":job['Responsibilities']
        },
        "Company": {
            "company_name":job['Company'],
            "sector": job['Sector'],
            "industry": job['Industry'],
            "city":job['City'],
            "state": job['State'],
            "zip":job['Zip'],
            "CEO":job['CEO'],
            "website":job['Website'],
            "ticker": job['Ticker']
        },
        "Location": {
            "longitude": job['longitude'],
            "latitude": job['latitude'],
            "location": job['location'],
            "country": job['Country']
        }   
    }
        docs.append(doc)

    jobs_collection.insert_many(docs)


def query1():
    ...


def query2():
    ...


def query3():
    ...


def query4():
    ...

# Print out existing databases and collections
print(client.list_database_names())
print(jobs_db.list_collection_names())

# Load the data into the database
data = pd.read_csv("jobs_sample.csv", index_col=0)
load_data(data)

# Print out the first 5 elements in the database
cursor = jobs_collection.find()
for document in cursor[:5]:
    printer.pprint(document)