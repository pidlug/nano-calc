#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Pango

import ast
import operator as op

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}

def calc(expr):
  """
  >>> eval_expr('2^6')
  4
  >>> eval_expr('2**6')
  64
  >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
  -5.0
  """
  return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
  if isinstance(node, ast.Num): # <number>
    return node.n
  elif isinstance(node, ast.BinOp): # <left> <operator> <right>
    return operators[type(node.op)](eval_(node.left), eval_(node.right))
  elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
    return operators[type(node.op)](eval_(node.operand))
  else:
    raise TypeError(node)

# ----------------------------------------

css = b"""

#button {
    color: #ffffff;
    background: #e80606;
}
entry {
    color: #101010;
    background: #b09090;
}

"""

sp = Gtk.CssProvider()
sp.load_from_data(css)

# ----------------------------------------

class callbacks:

  def equal(self,widget):
    # get expression text to calulate, replace "^" with "**" which is understood as pow by ast module
    m=tb.get_text().replace("^","**")
    try:
      res=str(calc(m))
    except:
      res="ERR"
    tb.set_text(res)
    tb.set_position(9999)

  def button(self,widget):
    m=tb.get_text()
    if m[0:3] == "ERR":
      tb.set_text("")
    tb.insert_text(widget._value,tb.get_position())
    tb.set_position(tb.get_position()+1)

  def negation(self,widget):
    m=tb.get_text()
    if m == "":
      tb.set_text("-")
    elif m == "-":
      tb.set_text("")
    elif m[0] == "-":
      m=m[1:]
      if m[0]=="(" and m[-1]==")":
        tb.set_text(m)
      elif any(elem in m for elem in "+-*/()"):
        tb.set_text("-(" + m + ")")
      else:
        tb.set_text(m)
    else:
      if m[0]=="(" and m[-1]==")":
        tb.set_text("-" + m)
      elif any(elem in m for elem in "+-*/()"):
        tb.set_text("-(" + m + ")")
      else:
        tb.set_text("-" + m)
    tb.set_position(9999)

  def reverse(self,widget):
    m=tb.get_text()
    if m[0]=="(" and m[-1]==")":
      tb.set_text("1/"+m)
    elif any(elem in m for elem in "+-*/()"):
      tb.set_text("1/(" + m + ")")
    else:
      tb.set_text("1/"+m)
    tb.set_position(9999)

  def clear(self,widget):
    tb.set_text("")

  def back(self,widget):
    tb.delete_text(tb.get_position()-1,tb.get_position())

x=callbacks()

# ----------------------------------------

def create_button(label,grid,posx,posy,sizex=None,sizey=None,value=None,callback=None,color=None,markup=None):
  btn=Gtk.Button(label=label)
  btn.set_hexpand(True)
  btn.set_vexpand(True)
  if sizex is None:
    sizex=1
  if sizey is None:
    sizey=1
  if not value is None:
    btn._value=value
  else:
    btn._value=label
  grid.attach(btn,posx,posy,sizex,sizey)
  if not callback is None:
    btn.connect("clicked",callback)

g1=Gtk.Grid()

tb=Gtk.Entry()
tbcontext = tb.get_style_context()
tbcontext.add_provider(sp,Gtk.STYLE_PROVIDER_PRIORITY_USER)

t1=Gtk.Grid()
t2=Gtk.Grid()

w=Gtk.Window()
w.add(g1)

tb.modify_font(Pango.FontDescription("sans,monospace condensed bold 24"))

create_button(label="7", callback=x.button, grid=t1, posx=0, posy=0)
create_button(label="8", callback=x.button, grid=t1, posx=1, posy=0)
create_button(label="9", callback=x.button, grid=t1, posx=2, posy=0)
create_button(label="4", callback=x.button, grid=t1, posx=0, posy=1)
create_button(label="5", callback=x.button, grid=t1, posx=1, posy=1)
create_button(label="6", callback=x.button, grid=t1, posx=2, posy=1)
create_button(label="1", callback=x.button, grid=t1, posx=0, posy=2)
create_button(label="2", callback=x.button, grid=t1, posx=1, posy=2)
create_button(label="3", callback=x.button, grid=t1, posx=2, posy=2)
create_button(label="0", callback=x.button, grid=t1, posx=0, posy=3)
create_button(label=".", callback=x.button, grid=t1, posx=1, posy=3)
create_button(label="=", callback=x.equal, grid=t1, posx=2, posy=3, sizex=2, color="green")

create_button(label="<-", callback=x.back, grid=t2, posx=0, posy=0, color="red")
create_button(label="(", callback=x.button, grid=t2, posx=0, posy=1, color="blue")
create_button(label="^", callback=x.button, grid=t2, posx=0, posy=2, color="blue")
create_button(label="/", callback=x.button, grid=t2, posx=0, posy=3, color="blue")
create_button(label="*", callback=x.button, grid=t2, posx=0, posy=4, color="blue")
create_button(label="-", callback=x.button, grid=t2, posx=0, posy=5, color="blue")
create_button(label="C", callback=x.clear, grid=t2, posx=1, posy=0, color="red")
create_button(label=")", callback=x.button, grid=t2, posx=1, posy=1, color="blue")
create_button(label="+/-", callback=x.negation, grid=t2, posx=1, posy=2, color="blue")
create_button(label="1/", callback=x.reverse, grid=t2, posx=1, posy=3, color="blue")
create_button(label="+", callback=x.button, grid=t2, posx=1, posy=4, sizey=2, color="blue")


tb.set_property("margin",12)
t1.set_property("margin",10)
t2.set_property("margin",6)

g1.set_row_homogeneous(False)
g1.set_column_homogeneous(False)
g1.set_column_spacing(10)
g1.set_row_spacing(10)
g1.set_halign(Gtk.Align.FILL);

t1.set_hexpand(True);
t1.set_vexpand(True);
t1.set_halign(Gtk.Align.FILL);
t2.set_hexpand(True);
t2.set_vexpand(True);
t2.set_halign(Gtk.Align.FILL);

t1.set_column_spacing(10)
t1.set_row_spacing(10)
t2.set_column_spacing(8)
t2.set_row_spacing(8)

t1.set_row_homogeneous(False)
t1.set_column_homogeneous(False)
t2.set_row_homogeneous(True)
t2.set_column_homogeneous(False)

g1.attach(tb,0,0,20,1)
g1.attach(t1,0,1,16,1)
g1.attach(t2,16,1,4,1)

w.show_all()
w.connect("delete-event",Gtk.main_quit)
Gtk.main()
