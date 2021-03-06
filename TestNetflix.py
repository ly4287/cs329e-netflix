#!/usr/bin/env python3

# -------
# imports
# -------
from Netflix import netflix_eval
from unittest import main, TestCase
from math import sqrt
from io import StringIO
from numpy import sqrt, square, mean, subtract

# -----------
# TestNetflix
# -----------

class TestNetflix (TestCase):

    # ----
    # eval
    # ----

    def test_eval_1(self):
        r = StringIO("1:\n30878\n2647871\n1283744\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "1:\n3.6\n3.5\n3.6\n0.49\n")

    def test_eval_2(self):
        r = StringIO("15652:\n2407795\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "15652:\n2.8\n1.21\n")

    def test_eval_3(self):
        r = StringIO("15657:\n1504956\n335395\n2111659\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "15657:\n2.9\n3.8\n3.4\n1.98\n")

    def test_eval_4(self):
        r = StringIO("10049:\n1430873\n555892\n2082280\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "10049:\n2.9\n2.6\n2.8\n0.63\n")

    def test_eval_5(self):
        r = StringIO("1:\n30878\n2647871\n1283744\n2488120\n317050\n1904905\n1989766\n14756\n1027056\n1149588\n1394012\n1406595\n2529547\n1682104\n2625019\n2603381\n1774623\n470861\n712610\n1772839\n1059319\n2380848\n548064\n")
        w = StringIO()
        netflix_eval(r, w)
        self.assertEqual(
            w.getvalue(), "1:\n3.6\n3.5\n3.6\n4.2\n3.7\n3.8\n3.5\n3.7\n3.8\n3.6\n3.1\n3.6\n3.9\n3.8\n3.2\n3.9\n3.7\n4.1\n3.9\n3.9\n3.4\n4.4\n3.6\n0.81\n")



# ----
# main
# ----			
if __name__ == '__main__':
    main()

""" #pragma: no cover
% coverage3 run --branch TestNetflix.py >  TestNetflix.out 2>&1



% coverage3 report -m                   >> TestNetflix.out



% cat TestNetflix.out
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Name             Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------
Netflix.py          27      0      4      0   100%
TestNetflix.py      13      0      0      0   100%
------------------------------------------------------------
TOTAL               40      0      4      0   100%

"""
