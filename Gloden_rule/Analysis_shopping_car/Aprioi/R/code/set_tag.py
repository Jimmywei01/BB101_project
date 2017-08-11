
import csv
f = open('tag_all_tagc3.csv', 'a')
w = csv.writer(f)
f = open('tag_all_tagc2.csv', 'r')

for i in f.readlines():
    a = set(i.strip('\n').split(';'))
    w.writerow(a)
    print(a)
