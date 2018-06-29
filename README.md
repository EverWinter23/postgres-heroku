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

You can either do this via the heroku dashboard or the heroku-cli. Navigate to the
heroku app dir, and enter the following cmd.

    $ heroku addons:create heroku-postgresql:hobby-dev
    Creating heroku-postgresql:hobby-dev on ⬢ sushi... free
    Database has been created and is available

### Important Stuff

Once you've created the database, to make effective use of Heroku Postgres databases
outside of a Heroku application, keep in mind the following:

+ **Credentials**: Do not copy and paste database credentials to a separate environment
  or into your application’s code. The database URL is managed by Heroku and will change under some circumstances such as:
    + User initiated database credential rotations using heroku pg:credentials:rotate.
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

### PostgreSQL Python: Connect To PostgreSQL Database Server

