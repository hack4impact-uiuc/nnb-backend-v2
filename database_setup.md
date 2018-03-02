# Database Setup

## Prerequisites
This setup assumes you have already completed the Flask-Boilerplate setup.

For mac: https://github.com/alvin-wu/flask-boilerplate/blob/master/docs/regular-setup.md

For windows: https://github.com/alvin-wu/flask-boilerplate/blob/master/docs/WSL-setup.md 

(todo: change the links above once we fork the boiler plate on the h4i repo)

## Setting up your database
In the guides above, we setup of Postgres and created a user as well as setup a database called testdb. However, even though the database is setup, we still need to populate it with our own tables!

The tables are defined in models.py. This file only _defines_ the schema. We need to run some commands to create the tables locally on your machine.

### Step 1: Connect to PSQL

For mac:

Start your postgres server(Ctrl-C to stop):
```
$ postgres -D /usr/local/var/postgres
```
In another terminal:
```
$psql -h localhost
```

For windows:
```
$ psql -p 5432 -h localhost -U postgres
```

You should see this:
```
postgres=#
```

### Step 2: Check that your database exists

In your postgres terminal, type \list which should list out your databases. You should see testdb in here if you followed the steps in the prereqs.
```
postgres=# \list
```

Next, connect to your testdb by typing the command \connect testdb:
```
postgres=# \connect testdb
```

You should now see your terminal change to:
```
testdb=# 
```

Finally, run the \dt command which will display tables. You should see something about having no relations (this means you don't have any tables yet).
```
testdb=# \dt 
```

### Create the tables!
This is the important part. Open a new terminal and change to the backend directory. Now we will run the following commands:

```
$ python manage.py db init
$ python manage.py db migrate
$ python manage.py db upgrade
```

You should see your tables being "detected".

Now, in your psql terminal check your tables and you should see them there!

```
testdb=# \dt 
```
