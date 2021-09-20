import sys

path = '/home/namnhatpham1995/MainApp'
if path not in sys.path:
    sys.path.insert(0, path)

from MainApp import app, routes
