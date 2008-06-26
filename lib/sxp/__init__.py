__version__ = '0.0.1'
__license__ = 'MIT'
__author__ = 'Arto Bendiken <http://bendiken.net/>'

__all__ = ['symbol', 'reader', 'writer']

from sxp.symbol import *
from sxp.reader import *
from sxp.writer import *

s = intern

def read(input):
  return Reader(input).read()

def read_all(input):
  return Reader(input).read_all()

def read_file(filename):
  try:
    file = open(filename, 'r')
    return read_all(file)
  finally:
    file.close()
