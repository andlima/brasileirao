# encoding: utf-8

import championship

SEPARATOR = u"–"

#
# Data from Wikipedia:
# http://en.wikipedia.org/wiki/2010_Campeonato_Brasileiro_S%C3%A9rie_A
#
with open("brasileirao-wikipedia-2010.txt", "r") as f:
    data = ''.join(line.decode('utf-8') for line in f.readlines())

matrix = [line.strip().split('\t')
          for line in data.strip().split('\n')][1:]

teams = [line.pop(0) for line in matrix]

matrix = [[i != j and [int(k) for k in cell.split(SEPARATOR)]
           for j, cell in enumerate(line)]
          for i, line in enumerate(matrix)]

championship.process(teams, matrix)
