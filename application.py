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
1) - Calculate Average Salary by Sector\n\n'
                )
            
            desired_query = int(desired_query)

            if desired_query == 0:
                break
            
            with open('test_query.sql') as f:
                query_file = f.read()
                queries = query_file.split(';')
                curs.execute(queries[desired_query - 1])
                rows = curs.fetchall()
                if not rows:
                    print('No results for this research!')
                else:
                    print('Here are the results of your research:')
                    print([x for x in rows])
                    time.sleep(1)

queries(user = 'root', password=main.psw)
print('Goodbye')