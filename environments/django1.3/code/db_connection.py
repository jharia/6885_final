# @author Jesika Haria
# @date December 3, 2013
import sys

import psycopg2

# Connect to database given name and user creds
def connect(dbname,usr='postgres',pw='postgres'):
  con = None
  try:
    con = psycopg2.connect(database=dbname, user=usr, password=usr,host="/tmp") 
    cur = con.cursor()
    cur.execute('SELECT version()')         
    ver = cur.fetchone()
    print ver    
      
  except psycopg2.DatabaseError, e:
    print 'Error %s' % e    
    sys.exit(1)
  return con      

# List all tables in a database
def list_tables(con):
  cur = con.cursor()
  cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
  rows = cur.fetchall()
  rows = [row[0] for row in rows]
  return rows

# Validate table name (for security since cannot be passed as param)
def is_valid_table(con,table): 
  cur = con.cursor()
  sql = ("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s""")
  data = (table, )
  cur.execute(sql, data)
  row = cur.fetchone()
  return True if row else False 

# List column names in a given table
def list_column_names(con, table):
  cur = con.cursor()
  if is_valid_table(con, table):   
    cur.execute('SELECT * FROM ' + table)
    colnames = [desc[0] for desc in cur.description]
    return colnames 
  else: 
    raise ValueError('Table ' + table + ' does not exist in database.')

# Disconnect from database given the connection object
def disconnect(con):
  if con:
    con.close()

# Main method
if __name__ == '__main__':
  # Constants
  dbname = 'template0'
  usr = 'postgres'
  pw = 'postgres'
  table = 'country'

  con = connect(dbname, usr, pw)
  # print list_tables(con)
  # print is_valid_table(con,'city')
  # print list_column_names(con,table)
  disconnect(con)