import main
import mysql.connector as mysql
import time

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
1) - Calculate Average Salary and Average required experience by gender for a selected role\n'
)
                        
            desired_query = int(input('\nYour choice -> '))

            with open('queries.sql') as f:
                query_file = f.read().split(";")

            if desired_query == 0:
                break
            
            elif desired_query == 1:
                curs.execute("SELECT DISTINCT role FROM Offer")
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
                ...
                     

            
queries(user = 'root', password=main.psw)
print('Goodbye')