from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import db, app
import pandas as pd
import os 
import glob


manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    app.run(debug=True, host='0.0.0.0', port=5000, ssl_context='adhoc')


@manager.command
def runworker():
    app.run(debug=False, ssl_context='adhoc')


@manager.command
def test():
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()

@manager.command
def backup_db():
    """
    Backups all tables into csv files.
    """

    #Create directory to hold backup tables
    #note: can't have any csv open or will get permission denied
    backup_tables_dir = 'backup_tables'
    if not os.path.exists(backup_tables_dir):
        os.makedirs(backup_tables_dir)
    else:
        #Flush table files if they exist
        files = glob.glob(backup_tables_dir+'/*')
        for file in files:
            os.remove(file)
            
    #Get list of table names
    table_names = []
    for table_data in db.metadata.tables.items():
        table_names.append(table_data[0])
        
    #Query all tables and write to csv
    for table_name in table_names:
        query_string = 'SELECT * FROM {};'.format(table_name)
        table = pd.read_sql(query_string,db.engine)
        table.to_csv(backup_tables_dir+'/'+table_name+'.csv',index=False)


if __name__ == '__main__':
    manager.run()