import mysql.connector as mysql
import time
import getpass
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def queries(user, password):
    db = mysql.connect(
            host="localhost", 
            user=user, 
            passwd=password)

    if db.is_connected():
        curs = db.cursor()
        curs.execute('Use Jobs')
        db.commit()

        while True:
            print(Panel(
' 0) - Quit\n \
1) - Calculate Average Salary and Average required experience by gender for a selected role\n \
2) - Display Job Offers available in a specific Country\n \
3) - Search by company name the job portals where the company is present and how many job offers are available\n \
4) - Search by key word a job description to discover correlated benefits and responsabilities\n \
5) - Title of study',
title = "[bold yellow]Select the query you want to execute"
     )
)
                        
            desired_query = int(input('\nYour choice -> '))
            print("")

            with open('queries.sql') as f:
                query_file = f.read().split(";")

            if desired_query == 0:
                break

            elif desired_query == 1:
                curs.execute("SELECT DISTINCT role FROM Offer ORDER BY role ASC")
                roles = [row[0] for row in curs.fetchall()]
                print("Available roles:")
                for i, role in enumerate(roles, start=1):
                    print(f"{i}. {role}")
                # Get user input for the desired role
                try:
                    choice = int(input("\nEnter the number corresponding to the role you prefer: "))
                    if 1 <= choice <= len(roles):
                        desired_role = roles[choice - 1]
                        # Replace the placeholder with the desired role
                        query = query_file[0].replace(":user_role", desired_role)
                        curs.execute(query)
                        rows = curs.fetchall()
                         # Display results
                        if not rows:
                            print('No results for this research!')
                        else:
                            print(f'\nHere are the results for the role "{desired_role}":')
                            for element in rows:
                                print(f'Selected Role: {element[0]} ,\nAverage male salary: {element[1]} £, Average experience required to apply: {element[2]} years,\nAverage female salary: {element[3]} £, Average experience required to apply: {element[4]} years')
                            time.sleep(1)
                    else:
                         print("Invalid input!") 
                except ValueError:
                    print("Invalid input!")    

            elif desired_query == 2:
                curs.execute("SELECT DISTINCT country FROM Location ORDER BY country ASC")
                countries = [row[0] for row in curs.fetchall()]
                for country in countries:
                    print("- " + country)
                try:
                    selected_country = input("\nSelect your Country: ")
                    query = query_file[1].replace(":user_country", selected_country)
                    curs.execute(query)
                    rows = curs.fetchall()

                    if not rows:
                        print('No results for this research!')
                    else:
                        table = Table(title=f"{len(rows)} results for {selected_country}:")
                        table.add_column("Job Title", justify="center", no_wrap=True)
                        table.add_column("Company name", justify="center", no_wrap=True)
                        table.add_column("Job Id", justify="center", no_wrap=True)
                        table.add_column("Job posting date", justify="center", no_wrap=True)

                        for element in rows:
                            table.add_row(element[2], element[3], str(element[0]), str(element[1]))

                        with console.pager():
                            console.print(table)

                except Exception as e:
                    print(e)

            elif desired_query == 3:
                curs.execute("SELECT DISTINCT company FROM Company ORDER BY company ASC")
                companies = [row[0] for row in curs.fetchall()]
                print("Available companies:")
                for i, company in enumerate(companies, start=1):
                    print(f"{i}. {company}")
                # Get user input for the desired role
                try:
                    choice = int(input("\nEnter the number corresponding to the company you prefer: "))
                    if 1 <= choice <= len(companies):
                        desired_company = companies[choice - 1]
                        # Replace the placeholder with the desired role
                        query = query_file[2].replace(":user_company", desired_company)
                        curs.execute(query)
                        rows = curs.fetchall()
                         # Display results
                        if not rows:
                            print('No results for this research!')
                        else:
                            print(f'\nHere are the results for the company "{desired_company}":')
                            for element in rows:
                                print(f'Job Portal: {element[1]} ,\nNumber of job offers: {element[2]}')
                            time.sleep(1)
                    else:
                         print("Invalid input!") 
                except ValueError:
                    print("Invalid input!")  

            elif desired_query == 4:
                curs.execute("SELECT DISTINCT job_description FROM Offer LIMIT 6")
                job_descriptions = [row[0] for row in curs.fetchall()]
                print("Here some hints:")
                for i, job_description in enumerate(job_descriptions, start=1):
                    print(f"{i}. {job_descriptions}")
                try:
                    choice = int(input("\nEnter the key word that you want to match a job description with: "))
                    if 1 <= choice <= len(job_descriptions):
                        desired_company = companies[choice - 1]
                        # Replace the placeholder with the desired role
                        query = query_file[2].replace(":user_company", desired_company)
                        curs.execute(query)
                        rows = curs.fetchall()
                         # Display results
                        if not rows:
                            print('No results for this research!')
                        else:
                            print(f'\nHere are the results for the company "{desired_company}":')
                            for element in rows:
                                print(f'Job Portal: {element[1]} ,\nNumber of job offers: {element[2]}')
                            time.sleep(1)
                    else:
                         print("Invalid input!") 
                except ValueError:
                    print("Invalid input!")  

                    

                     
print("""
     ██╗ ██████╗ ██████╗ ███████╗    ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗      █████╗ ██████╗ ██████╗ 
     ██║██╔═══██╗██╔══██╗██╔════╝    ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔══██╗
     ██║██║   ██║██████╔╝███████╗    █████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝    ███████║██████╔╝██████╔╝
██   ██║██║   ██║██╔══██╗╚════██║    ██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    ██╔══██║██╔═══╝ ██╔═══╝ 
╚█████╔╝╚██████╔╝██████╔╝███████║    ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║    ██║  ██║██║     ██║     
 ╚════╝  ╚═════╝ ╚═════╝ ╚══════╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝     ╚═╝     
                                                                                                              """)
password = getpass.getpass('Insert password for localhost --> ')

queries(user = 'root', password=password)
console.print("Goodbye", style = 'bold #96EFFF')