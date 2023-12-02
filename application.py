import mysql.connector as mysql
import time
import getpass

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
            print(
'\nSelect the query you want to execute:\n \
===========================================\n \
0) - Quit\n \
1) - Calculate Average Salary and Average required experience by gender for a selected role\n \
2) - Display Job Offers available in a specific Country'
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
                        print(f'\nHere are the results for "{selected_country}":\n')

                    for element in rows:
                        print(f'>Job Title: {element[2]}\n Company name: {element[3]}\n Job Id: {element[0]}\n Job posting date: {element[1]}\n')
                    print(f"∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾\n {len(rows)} job offers found!\n∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾∾")
                    time.sleep(1)

                except Exception as e:
                    print(e)


                     
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
print('\nGoodbye')