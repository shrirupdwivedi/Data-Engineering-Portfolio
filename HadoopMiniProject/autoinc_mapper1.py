#!/usr/bin/python

import sys
# input comes from STDIN (standard input)
#p = open("data.csv")
for line in sys.stdin: 

    line1 = line.strip()
    data = line1.split(',')

    print('%s\t(%s,%s,%s)' % (data[2],data[1],data[3],data[5]))

#p.close()