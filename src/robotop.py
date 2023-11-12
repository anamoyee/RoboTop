if True: # \/ # PyVersion // assert sys.version_info[:2] == (3, 11)
  if __import__('sys').version_info[:2] != (3, 11):
    msg = "Use py311"
    raise ValueError(msg)

if True: # \/ # Imports
  from db import backup_all_databases, db
  from imports import *