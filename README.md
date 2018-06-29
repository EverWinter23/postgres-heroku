# README

Heroku Postgres databases are designed to be used with a Heroku app. However,
except for private and shield tier databases, they are accessible from anywhere
and may be used from any application using standard Postgres clients. 

This README.md focuses on connecting to the PostgresDB from external applications,
or python scripts to manipulate the database and how to reflect the changes on the
heroku web application.

### Getting Started With HerokuPostgres

The very first thing to do is attaching the postgres to your Heroku-app, even if
you don't want use the Heroku app for application code, your database is attached to
it and holds a config var containing the database URL. This variable is managed by
Heroku, and is the primary way they tell you about your database’s network location 
and credentials.

You can either do this via the heroku dashboard or the Heroku CLI. Navigate to the
Heroku app dir, else create one, and enter the following cmd.

    $ heroku addons:create heroku-postgresql:hobby-dev
    Creating heroku-postgresql:hobby-dev on ⬢ sushi... free
    Database has been created and is available

### Important Stuff

Once you've created the database, to make effective use of Heroku Postgres databases
outside of a Heroku application, keep in mind the following:

+ **Credentials**: Do not copy and paste database credentials to a separate environment
  or into your application’s code. The database URL is managed by Heroku and will change under some circumstances such as:
    + User initiated database credential rotations using `heroku pg:credentials:rotate`.
    + Catastrophic hardware failure leading to Heroku Postgres staff recovering your
      database on new hardware.
    + Automated failover events on HA enabled plans.
+ **SSL Secure Socekt Layer**: Applications outside of the Heroku network must 
  support and enable SSL to connect to a Heroku Postgres database. Most clients
  connect over SSL by default, but sometimes it’s necessary to add the`sslmode=require` query parameter to your database URL before connecting.

### HerokuPostgres Python Setup

This section shows you how to work with Postgres database that we have setup using
Python. The very first thing you need to do to interact with the database is to install
a Postgres database driver. Currently, the psycopg is the most popular PostgreSQL
database adapter for the Python language. You can install the driver using pip.

    $ pip install psycopg2-binary

psycopg2 driver supports many Python types out-of-the-box. The psycopg2 matches Python
objects to the PostgreSQL data types e.g., list to the array, tuples to records, and
dictionary to hstore.  If you want to customize and extend the type adaption, you can
use a flexible object adaption system.

### PostgreSQL Python: Connect To HerokuPostgres Database

Since we know that HerokuPostgres credentials are not permanent and are subject to change, the best practice is to always fetch the database URL config var from the
corresponding Heroku app when your python application starts.

For example, you may follow 12Factor application configuration principles by using the
Heroku CLI and **invoke** your process like this:

    DATABASE_URL=$(heroku config:get DATABASE_URL -a your-app) python your-script.py

This way, you ensure your process or application always has correct database credentials.

```python
import psycopg2, os

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')
con = None
try:
    # create a new database connection by calling the connect() function
    con = psycopg2.connect(DATABASE_URL)

    #  create a new cursor
    cur = conn.cursor()
    
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
        print('Database connection closed.')
```

>Now, we'll look into working with Postgres.

### HerkouPostgres Python: Maipulating The Database

Steps for manipulating PostgreSQL tables in Python

+ First, construct a QUERY statement.
+ Next, connect to the PostgreSQL database by calling the connect() function. The 
  connect() function returns a connection object.
+ Then, create a cursor object by calling the cursor() method of the connection object.
+ After that, execute the QUERY by calling the execute() method of the cursor object.
+ Finally, close the communication with the PostgreSQL database server by calling the
  close() methods of the cursor and connection objects.


```python
import psycopg2, os

# read database connection url from the enivron variable we just set.
DATABASE_URL = os.environ.get('DATABASE_URL')

cmd_create_action_table = """CREATE TABLE actions (
                              action VARCHAR(255) NOT NULL,
                              path VARCHAR(255) NOT NULL,
                              status BOOLEAN NOT NULL DEFAULT FALSE
                             )
                          """

con = None
try:
    # create a new database connection by calling the connect() function
    con = psycopg2.connect(DATABASE_URL)

    #  create a new cursor
    cur = conn.cursor()
    cur.execute(cmd_create_action_table)
       
     # close the communication with the HerokuPostgres
    cur.close()
except Exception as error:
    print('Could not connect to the Database.')
    print('Cause: {}'.format(error))

finally:
    # close the communication with the database server by calling the close()
    if con is not None:
        con.close()
        print('Database connection closed.')
```