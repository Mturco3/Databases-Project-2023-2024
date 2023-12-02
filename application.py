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
            desired_query = input(
'\nSelect the query you want to execute:\n \
===========================================\n \
0) - Quit\n \
1) - Calculate Average Salary and Average required experience by gender for a selected role\n\n'
                )
            
            desired_query = int(desired_query)

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
                    desired_query = int(input("Enter the number corresponding to the role you prefer: "))
                    if 1 <= desired_query <= len(roles):
                        desired_role = roles[desired_query - 1]
                        # Read the SQL queries from the file
                        with open('test_query.sql') as f:
                            query_file = f.read()
                        # Replace the placeholder with the desired role
                        query = query_file.replace(":user_role", desired_role)
                        curs.execute(query)
                        rows = curs.fetchall()
                         # Display results
                        if not rows:
                            print('No results for this research!')
                        else:
                            print(f'Here are the results for the role "{desired_role}":')
                            for element in rows:
                                print(f'Selected Role: {element[0]} ,\nAverage male salary: {element[1]} £, Average experience required to apply: {element[2]} years,\nAverage female salary: {element[3]} £, Average experience required to apply: {element[4]} years')
                            time.sleep(1)
                    else:
                         print("Invalid input!") 
                except ValueError:
                    print("Invalid input!")    

            #elif desired_query == 2:   
                     

            
            
queries(user = 'root', password=main.psw)
print('Goodbye')