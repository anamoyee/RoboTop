if __import__('sys').version_info[:2] != (3, 11): raise ValueError("Use py311")

import hikari
import lightbulb
import miru

import db
from imports import *

tcr.timeit.start('uwu')

@tcr.timeit
def test():
  kon(db.keys())

test()

tcr.timeit.stop('uwu')