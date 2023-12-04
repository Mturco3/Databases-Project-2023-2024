import mysql.connector as mysql
import time
import getpass
from rich import print
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

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
4) - Discover the maximum and minimum salary for a given university degree\n \
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
                table = Table(title=f"Available roles", box=box.ASCII)
                table.add_column("Role Name")
                for i, role in enumerate(roles, start=1):
                    table.add_row(f"{i}. {role}")
                console.print(table)
                
                # Get user input for the desired role
                try:
                    choice = int(input("\nEnter the number corresponding to the role you prefer: "))
                    if 1 <= choice <= len(roles):
                        desired_role = roles[choice - 1]
                        # Replace the placeholder with the desired role
                        query = query_file[0].replace(":user_role", desired_role)
                        curs.execute(query)
                        rows = curs.fetchall()
                        
                    if not rows:
                        print('No results for this research!')
                    else:
                        table = Table(title=f"Results for {desired_role}:")
                        table.add_column("Role", justify="center", no_wrap=True)
                        table.add_column("Average Male Salary", justify="center", no_wrap=True)
                        table.add_column("Average Male required Experience", justify="center", no_wrap=True)
                        table.add_column("Average Female Salary", justify="center", no_wrap=True)
                        table.add_column("Average Female required Experience", justify="center", no_wrap=True)

                        for element in rows:
                            table.add_row(element[0], str(element[1]), str(element[2]), str(element[3]) , str(element[4]))

                        with console.pager():
                            console.print(table)

                except Exception as e:
                    print(e) 

            elif desired_query == 2:
                curs.execute("SELECT DISTINCT country FROM Location ORDER BY country ASC")
                countries = [row[0] for row in curs.fetchall()]
                table = Table(title=f"Available countries", box=box.ASCII)
                table.add_column("Country Name")
                for country in countries:
                    table.add_row(country)
                console.print(table)
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
                table = Table(title=f"Available companies", box=box.ASCII)
                table.add_column("Company Name")
                for i, company in enumerate(companies, start=1):
                    table.add_row(f"{i}. {company}")
                console.print(table)
                
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
                            table = Table(title=f"{len(rows)} results for {desired_company}:")
                            table.add_column("Job Portal", justify="center", no_wrap=True)
                            table.add_column("Number of Job Offers", justify="center", no_wrap=True)
                        
                        for element in rows:
                            table.add_row(element[1], str(element[2]))

                        with console.pager():
                            console.print(table) 
                except Exception as e:
                    print(e) 

            elif desired_query == 4:
                curs.execute("SELECT DISTINCT qualifications FROM Offer ORDER BY qualifications ASC")
                job_titles = [row[0] for row in curs.fetchall()]
                table = Table(title=f"University Degrees:", box=box.ASCII)
                table.add_column("Job Titles")
                for i, job_title in enumerate(job_titles, start=1):
                    table.add_row(f"{i}. {job_title}")
                console.print(table)
                try:
                    selected_degree = input("\nSelect your university degree: ")
                    query = query_file[3].replace(':user_input', selected_degree)
                    curs.execute(query)
                    rows = curs.fetchall()
                     # Display results
                    if not rows:
                        print('No results for this research!')
                    else:
                        table = Table(title=f"Results for {selected_degree}:")
                        table.add_column("Role", justify="center", no_wrap=True)
                        table.add_column("Max Salary", justify="center", no_wrap=True)
                        table.add_column("Min Salary", justify="center", no_wrap=True)
                        table.add_column("Max Experience", justify="center", no_wrap=True)
                        table.add_column("Min Experience", justify="center", no_wrap=True)

                        for element in rows:
                            table.add_row(str(element[1]), str(element[2]), str(element[3]), str(element[4]), str(element[5]))

                        with console.pager():
                            console.print(table)

 
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
console.print("Goodbye 👋", style = 'bold #96EFFF')