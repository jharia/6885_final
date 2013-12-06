# @author Jesika Haria
# @date December 3, 2013

import re
import string 
import sys 

import psycopg2

import db_connection as dbc
import concept as cpt

# Strip punctuations from string (tokenize)
def strip_punctuation(s): 
  punc = string.punctuation
  s = list(s)
  return ''.join([o if not o in string.punctuation else ' ' for o in s]).split()

def find_col_attr(all_col_names):

  for col_name in all_col_names:
    print 'column ', col_name
    print cpt.common_relations(col_name)

if __name__ == '__main__':
  dbname = 'world'
  usr = 'postgres'
  pw = 'postgres'
  
  con = dbc.connect(dbname, usr, pw)
  
  tables = dbc.list_tables(con)
  all_col_names = [dbc.list_column_names(con, table) for table in tables]
  # print all_col_names
  find_col_attr(all_col_names)

  dbc.disconnect(con)