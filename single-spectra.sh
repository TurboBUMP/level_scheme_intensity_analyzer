#!/bin/zsh

./sauron.py 1157.0208 --gate 4932.8 --peak 1157.004 --param -0.1 10 1157 2 350
./sauron.py 3357.29 -g 2037.9 -p 2200.1 --param -1 0 2200 2 100 -w 10
./sauron.py 3661.527 -g 1141.1 -p 2504.39 --param -1 0 2504 2 100 -w 4
./sauron.py 3661.527 -g 1839.7 -p 1777.973 --param -1 0 1778 2 100 -w 100
./sauron.py 3676.092 -g 1825.9 -p 1017.5 --param -1 0 1017 2 2e6 --limit 7 5
