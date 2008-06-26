import codecs, re
from StringIO import StringIO
from sxp.symbol import intern

class ReaderError(Exception): pass
class EndOfInput(ReaderError): pass
class EndOfList(ReaderError): pass

class Reader(object):
  "S-expression reader"

  FLOAT           = re.compile(ur'^[+-]?(?:\d+)?\.\d*$')
  INTEGER_BASE_2  = re.compile(ur'^[+-]?[01]+$')
  INTEGER_BASE_8  = re.compile(ur'^[+-]?[0-7]+$')
  INTEGER_BASE_10 = re.compile(ur'^[+-]?\d+$')
  INTEGER_BASE_16 = re.compile(ur'^[+-]?[\da-z]+$', re.I)
  RATIONAL        = re.compile(ur'^([+-]?\d+)\/(\d+)$')
  ATOM            = re.compile(ur'^[^\s()]+')
  WHITESPACE      = re.compile(ur'\s+')
  ESCAPED_CHARS   = { '"': u'"', '\\': u'\\', '/': u'/', 'b': u'\b', 'f': u'\f', 'n': u'\n', 'r': u'\r', 't': u'\t' }

  def __init__(self, input):
    self.input = StringIO(input)
    self.input = input
    self.lookahead = None
    self.eof = False
    if not hasattr(self.input, 'read'):
      raise ParseError('Item to parse must be a file-like object.')

  def __iter__(self):
    return self

  def next(self):
    try:
      return self.read()
    except EndOfInput:
      raise StopIteration

  def read_all(self):
    list = []
    for value in self:
      list.append(value)
    return list

  def read(self):
    """Reads one S-expression."""
    token, value = self.read_token()
    if token == 'list':
      if value == '(':
        return self.read_list()
      else:
        raise EndOfList('unexpected list terminator: )')
    else:
      return value

  def skip(self):
    self.read()

  def read_token(self):
    self.skip_comments()
    char = self.peek_char()
    if char == '(' or char == ')':
      return ['list', self.read_char()]
    if char == '#':
      return ['atom', self.read_sharp()]
    if char == '"':
      return ['atom', self.read_string()]
    else:
      return ['atom', self.read_atom()]

  def read_list(self):
    list = []
    try:
      while not self.eof:
        list.append(self.read())
    except EndOfList:
      pass
    return list

  def read_sharp(self):
    self.skip_char() # '#'
    char = self.read_char()
    if char == 'n':
      return None
    if char == 'f':
      return False
    if char == 't':
      return True
    if char == 'b':
      return self.read_integer(2)
    if char == 'o':
      return self.read_integer(8)
    if char == 'd':
      return self.read_integer(10)
    if char == 'x':
      return self.read_integer(16)
    if char == '\\':
      return self.read_character()
    if char == ';':
      self.skip()
      return self.read()
    else:
      raise ReaderError('invalid sharp-sign read syntax: %s' % char)

  def read_integer(self, base = 10):
    buffer = self.read_literal()
    if True: # TODO
      int(buffer, base)
    else:
      raise ReaderError('illegal base-%d number syntax: %s' % (base, buffer))

  def read_atom(self):
    buffer = self.read_literal()
    if self.FLOAT.match(buffer):
      return float(buffer)
    if self.INTEGER_BASE_10.match(buffer):
      return int(buffer)
    if self.RATIONAL.match(buffer):
      return None # FIXME
    else:
      return intern(buffer)

  def read_string(self):
    buffer = ''
    self.skip_char() # '"'
    while self.peek_char() != '"':
      char = self.read_char()
      if char == '\\':
        buffer += self.read_character()
      else:
        buffer += char
    self.skip_char() # '"'
    return buffer

  def read_character(self):
    char = self.read_char()
    if self.ESCAPED_CHARS.has_key(char):
      return self.ESCAPED_CHARS[char]
    else:
      return char

  def read_literal(self):
    buffer = ''
    while self.ATOM.match(self.peek_char()):
      buffer += self.read_char()
    return buffer

  def skip_comments(self):
    while not self.eof:
      char = self.peek_char()
      if char == ';':
        while not self.eof:
          if self.read_char() == '\n':
            break
      elif self.WHITESPACE.match(char):
        self.skip_char()
      else:
        break

  def read_chars(self, count=1):
    buffer = ''
    for i in range(count):
      buffer += self.read_char()
    return buffer

  def read_char(self):
    if self.lookahead is not None:
      char = self.lookahead
      self.lookahead = None
    else:
      char = self.input.read(1)
      if char == '':
        self.eof = True
        raise EndOfInput('unexpected end of input')
    return char

  def skip_char(self):
    self.read_char()

  def peek_char(self):
    if self.lookahead is None:
      self.lookahead = self.read_char()
    return self.lookahead
