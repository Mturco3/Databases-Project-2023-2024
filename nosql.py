import pandas as pd
from pymongo import MongoClient
import pprint
from bson.objectid import ObjectId
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print

client = MongoClient('localhost', 27017)
jobs_db = client.Jobs
jobs_collection = jobs_db.jobs_collection
printer = pprint.PrettyPrinter()
console = Console()


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
    user_input_company = input("Specify the desired Company Name -> ")  # Replace with the user's input

    pipeline_dynamic = [
        {
            "$match": {
                "Company.company_name": user_input_company
            }
        },
        {
            "$unwind": "$Role.skills"
        },
        {
            "$group": {
                "_id": "$Role.skills",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {"count": -1}
        },
        {
            "$limit": 3
        },
        {
            "$project": {
                "_id": 0,
                "skill": "$_id",
                "count": 1
            }
        }
    ]

    result = jobs_collection.aggregate(pipeline_dynamic)

    table = Table(title=f"Top 3 most common skills required by {user_input_company}", leading=1, show_lines=True)
    table.add_column("Skill Description")
    table.add_column("Count", justify="center")
    for item in result:
        table.add_row(str(item['skill']), str(item['count']))

    with console.pager():
        console.print(table)


def query2():
    user_input_industry= input("Specify the desired Industry Name -> ")  # Replace with the user's input

    # Aggregate pipeline to group by industry and contact_person, and count the jobs
    pipeline = [
        {
            "$match": {
                "Company.industry": user_input_industry
            }
        },
        {
            "$group": {
                "_id": {
                    "industry": "$Company.industry",
                    "contact_person": "$contact_person",
                    "contact": "$contact" 
                },
                "job_count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "industry": "$_id.industry",
                "contact": "$_id.contact",
                "contact_person": "$_id.contact_person",
                "job_count": 1
            }
        }
    ]

    result = jobs_collection.aggregate(pipeline)

    # Display the results
    table = Table(title=f"Contact People for the {user_input_industry} industry", leading=1, show_lines=True)
    table.add_column("Contact", style="dim", width=30)
    table.add_column("Contact Person", style="dim", width=30)
    table.add_column("Job Count", style="dim", width=10)

    for entry in result:
        table.add_row(entry["contact"], entry["contact_person"], str(entry["job_count"]))

    with console.pager():
        console.print(table)




def query3():
    ...


def query4():
    ...

if __name__ == '__main__':
    # Print out existing databases and collections
    print(client.list_database_names())
    print(jobs_db.list_collection_names())

    data = pd.read_csv("jobs_sample.csv", index_col=0)

    # Check if there's the need to load the data
    if jobs_collection.count_documents(filter = {}) == 0:
        load_data(data)

    # Print out the first 5 elements in the database
    # cursor = jobs_collection.find()
    # for document in cursor[:5]:
    #     printer.pprint(document)

    while True:
        print(Panel(
    ' 0) - Quit\n \
1) - Find the top 3 most required skills by company\n \
2) - Discover who you should contact if you want to work in a given sector',
    title = "[bold yellow]Select the query you want to execute"
        )
    )

        desired_query = int(input('\nYour choice -> '))
        
        if desired_query == 0:
            break

        elif desired_query == 1:
            query1()
        
        elif desired_query == 2:
            query2()

    console.print("\nGoodbye 👋", style = 'bold #96EFFF')