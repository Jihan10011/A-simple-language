#!/usr/bin/env python3
import math

class TokenType:
  NUM = "NUM"
  PLUS = "PLUS"
  ID = "ID"
  KEY = "KEY"
  SC = "SC";
  EQ = "EQ"
  MINUS = "MINUS"
  MUL = "MUL"
  DIV = "DIV"
  SQRT = "SQRT"
  LPAREN = "LPAREN"
  RPAREN = "RPAREN"
  CLPAREN = "CLPAREN"
  CRPAREN = "CRPAREN"
  EOF = "EOF"

END = -1

# NonTerminals

class G:
  def __init__(self, l, A, next, r):
    self.left = l
    self.A = A
    self.next = next
    self.right = r

class GP:
  def __init__(self, A, next):
    self.A = A
    self.next = next

class A:
  class A1:
    def __init__(self, num, name, S):
      self.num = num
      self.name = name
      self.S = S
  class A2:
    def __init__(self, name, S):
      self.name = name
      self.S = S
  class A3:
    def __init__(self, l, S, r):
      self.left = l
      self.S = S
      self.right = r

class S:
  def __init__(self, opr, M, next):
    self.opr = opr
    self.M = M
    self.next = next

class SP:
  def __init__(self, opr, M, next):
    self.opr = opr
    self.M = M
    self.next = next

class M:
  def __init__(self, V, next):
    self.V = V
    self.next = next

class MP:
  def __init__(self, opr, O, V, next):
    self.opr = opr
    self.O = O
    self.V = V
    self.next = next

class V:
  class V1:
    def __init__(self, num):
      self.num = num
  class V2:
    def __init__(self, r, next, l):
      self.right = r
      self.next = next
      self.left = l
  class V3:
    def __init__(self, name):
      self.name = name



class Token:
  def __init__(self, type, value, pos):
    self.type = type
    self.value = value
    self.pos = pos
  def __repr__(self):
    return f"Token({self.type}, {repr(self.value)}, {self.pos})"



class Lexer:
  def __init__(self, text):
    self.text = text
  def lex(self):
    txt = self.text
    length = len(txt)
    pos = 0
    
    tokens = []
    
    while pos < length:
      currPos = pos
      
      if txt[pos] in " \t\n":
        pos += 1
      elif txt[pos] == "#":
        while pos < length and txt[pos] != "\n":
          pos += 1
      elif txt[pos] == "(":
        tokens.append(Token(TokenType.LPAREN, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "√":
        tokens.append(Token(TokenType.SQRT, txt[pos], currPos))
        pos += 1
      elif txt[pos] == ")":
        tokens.append(Token(TokenType.RPAREN, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "{":
        tokens.append(Token(TokenType.CLPAREN, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "}":
        tokens.append(Token(TokenType.CRPAREN, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "+":
        tokens.append(Token(TokenType.PLUS, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "-":
        tokens.append(Token(TokenType.MINUS, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "*":
        tokens.append(Token(TokenType.MUL, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "/":
        tokens.append(Token(TokenType.DIV, txt[pos], currPos))
        pos += 1
      elif txt[pos] == ";":
        tokens.append(Token(TokenType.SC, txt[pos], currPos))
        pos += 1
      elif txt[pos] == "=":
        tokens.append(Token(TokenType.EQ, txt[pos], currPos))
        pos += 1
      elif txt[pos].isalpha():
        id = ""
        while pos < length and (txt[pos].isalpha() or txt[pos].isdigit()):
          id += txt[pos]
          pos += 1
        if id == "num":
          tokens.append(Token(TokenType.KEY, id, currPos))
        else:
          tokens.append(Token(TokenType.ID, id, currPos))
      elif txt[pos].isdigit() or txt[pos] == ".":
        num = ""
        while pos < length and (txt[pos].isdigit() or txt[pos] == "."):
          num += txt[pos]
          pos += 1
        if num.count(".") == 0:
          tokens.append(Token(TokenType.NUM, int(num), currPos))
        elif num.count(".") == 1:
          tokens.append(Token(TokenType.NUM, float(num), currPos))
        else:
          raise SyntaxError(f"Unknown Syntax: {num} at position {currPos}")
      else:
        raise TypeError(f"Unexpected Character: '{txt[pos]}' at position {pos+1}")
    tokens.append(Token(TokenType.EOF, "<EOF>", pos))
    return tokens

class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.lookahead = self.tokens[0]
  def parse(self):
    res = self.GF()
    self.eat(TokenType.EOF)
    #self.eat(TokenType.EOF)
    return res
  def GF(self):
    l = self.eat(TokenType.CLPAREN)
    a = self.AF()
    gp = self.GPF()
    r = self.eat(TokenType.CRPAREN)
    res = G(l.value, a, gp, r.value)
    return res
  def GPF(self):
    if self.lookahead.type in [TokenType.KEY, TokenType.ID, TokenType.SC]:
      a = self.AF()
      gp = self.GPF()
      res = GP(a, gp)
      return res
    else:
      return END
  def AF(self):
    if self.lookahead.type == TokenType.KEY:
      k = self.eat(TokenType.KEY)
      name = self.eat(TokenType.ID)
      self.eat(TokenType.EQ)
      s = self.SF()
      self.eat(TokenType.SC)
      res = A.A1(k.value, name.value, s)
      return res
    elif self.lookahead.type == TokenType.ID:
      name = self.eat(TokenType.ID)
      self.eat(TokenType.EQ)
      s = self.SF()
      self.eat(TokenType.SC)
      res = A.A2(name.value, s)
      return res
    elif self.lookahead.type == TokenType.SC:
      l = self.eat(TokenType.SC)
      s = self.SF()
      r = self.eat(TokenType.SC)
      res = A.A3(l.value, s, r.value)
      return res
    else:
      raise TypeError(f"Unexpected Type: {self.lookahead.type} at position {self.lookahead.pos}")
  def SF(self):
    o = self.OF()
    m = self.MF()
    sp = self.SPF()
    res = S(o, m, sp)
    return res
  def SPF(self):
    if self.lookahead.type in [TokenType.PLUS, TokenType.MINUS]:
      op = self.OPF()
      m = self.MF()
      sp = self.SPF()
      res = SP(op, m, sp)
      return res
    else:
      return END
  def MF(self):
    v = self.VF()
    mp = self.MPF()
    res = M(v, mp)
    return res
  def MPF(self):
    if self.lookahead.type in [TokenType.MUL, TokenType.DIV]:
      p = self.PF()
      o = self.OF()
      v = self.VF()
      mp = self.MPF()
      res = MP(p, o, v, mp)
      return res
    else:
      return END
  def VF(self):
    if self.lookahead.type == TokenType.NUM:
      num = self.eat(TokenType.NUM)
      res = V.V1(num.value)
      return res
    elif self.lookahead.type == TokenType.LPAREN:
      l = self.eat(TokenType.LPAREN)
      S = self.SF()
      r = self.eat(TokenType.RPAREN)
      res = V.V2(l.value, S, r.value)
      return res
    elif self.lookahead.type == TokenType.ID:
      name = self.eat(TokenType.ID)
      res = V.V3(name.value)
      return res
    else:
      raise TypeError(f"Unexpected Type: {self.lookahead.type} at position {self.lookahead.pos}")
  def PF(self):
    if self.lookahead.type == TokenType.MUL:
      res = self.eat(TokenType.MUL)
      return res.value
    elif self.lookahead.type == TokenType.DIV:
      res = self.eat(TokenType.DIV)
      return res.value
    elif self.lookahead.type == TokenType.SQRT:
      res = self.eat(TokenType.SQRT)
      return res.value
    else:
      raise TypeError(f"Unexpected Type: {self.lookahead.type} at position {self.lookahead.pos}")
  def OF(self):
    if self.lookahead.type == TokenType.PLUS:
      res = self.eat(TokenType.PLUS)
      return res.value
    elif self.lookahead.type == TokenType.MINUS:
      res = self.eat(TokenType.MINUS)
      return res.value
    else:
      return END
  def OPF(self):
    if self.lookahead.type == TokenType.PLUS:
      res = self.eat(TokenType.PLUS)
      return res.value
    elif self.lookahead.type == TokenType.MINUS:
      res = self.eat(TokenType.MINUS)
      return res.value
    else:
      raise TypeError(f"Unexpected Type: {self.lookahead.type} at position {self.lookahead.pos}")
  def eat(self, type):
    res = self.lookahead # self.tokens.pop(0)
    if res.type != type:
      raise TypeError(f"Expected Type: {type} got {res.type} and value {res.value} at position {res.pos}")
    self.tokens.pop(0)
    if self.tokens:
      self.lookahead = self.tokens[0]
      return res
    else:
      return self.lookahead

class Interpreter:
  def __init__(self, tree):
    self.tree = tree
    self.vartab = {"e": math.e, "pi": math.pi, "tau": math.tau}
  def interpreat(self):
    self.eval_G(self.tree)
  def eval_G(self, tree):
    while tree != END:
      a = tree.A
      self.eval_A(a)
      tree = tree.next
  def eval_A(self, a):
    if type(a) == A.A1:
      if a.name in self.vartab:
        raise NameError(f"variable {a.name} already exists")
      self.vartab[a.name] = self.eval_S(a.S)
    elif type(a) == A.A2:
      if a.name not in self.vartab:
        raise NameError(f"variable {a.name} does not exists")
      self.vartab[a.name] = self.eval_S(a.S)
    elif type(a) == A.A3:
      res = self.eval_S(a.S)
      print(res)
  def eval_S(self, s):
    res = 1 if s.opr == "+" or s.opr == END else -1
    res *= self.eval_M(s.M)
    s = s.next
    while s != END:
      if s.opr == "+":
        res += self.eval_M(s.M)
      if s.opr == "-":
        res -= self.eval_M(s.M)
      s = s.next
    return res
  def eval_M(self, m):
    v = self.eval_V(m.V)
    res = v
    m = m.next
    while m != END:
      a = 1 if m.O == "+" or m.O == END else -1
      a *= self.eval_V(m.V)
      if m.opr == "*":
        res *= a
      elif m.opr == "/":
        res /= a
      elif m.opr == "√":
        res *= math.sqrt(a)
      m = m.next
    return res
  def eval_V(self, v):
    if type(v) == V.V1:
      num = v.num
      return num
    elif type(v) == V.V2:
      res = self.eval_S(v.next)
      return res
    elif type(v) == V.V3:
      name = v.name
      if name not in self.vartab:
        raise NameError(f"variable {name} not found")
      res = self.vartab[name]
      return res
    else:
      raise TypeError(f"Unexpected Type: {type(v)}")
    
tokens = Lexer(open("my.sml").read()).lex()
tree = Parser(tokens).parse()
Interpreter(tree).interpreat()

"""
while tree != END:
  print(tree.M.V.num)
  tree = tree.next



while True:
  try:
    txt = input(">>> ")
    if txt == "q":
      break
    elif txt == "": continue
    tokens = Lexer(txt).lex()
    tree = Parser(tokens).parse()
    res = Interpreter(tree).interpreat()
    print(res)
  except Exception as e:
    if type(e) == EOFError:
      print()
      break
    print(f"Error: {str(e)}")
"""




