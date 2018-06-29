'''
29th june 2018 friday
connect to heroku-postgres databse
'''

import psycopg2, os

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')
con = None
try:
    # create a new database connection by calling the connect() function
    con = psycopg2.connect(DATABASE_URL)

    #  create a new cursor
    cur = con.cursor()
    
    # execute an SQL statement to get the HerokuPostgres database version
    print('PostgreSQL database version:')
    cur.execute('SELECT version()')

    # display the PostgreSQL database server version
    db_version = cur.fetchone()
    print(db_version)
       
     # close the communication with the HerokuPostgres
    cur.close()
except Exception as error:
    print('Cause: {}'.format(error))

finally:
    # close the communication with the database server by calling the close()
    if con is not None:
        con.close()
        print('Databse connection closed.')