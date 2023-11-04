if True: # \/ # PyVersion // assert sys.version_info[:2] == (3, 11)
  if __import__('sys').version_info[:2] != (3, 11):
    msg = "Use py311"
    raise ValueError(msg)

if True: # \/ # Imports
  import db
  from imports import *

tcr.timeit.start('uwu')

@tcr.timeit
def test():
  kon(db.keys())

test()

tcr.timeit.stop('uwu')