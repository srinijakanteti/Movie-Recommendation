import utils
import csv
import sqlite3
import dbInfo
import sys
from Movie import Movie

print(utils.wieghtedTime('1234-11-12','23:45:23'));

print(utils.weightedRank(23));

mv = Movie('12321')
#mv.addTag('3123')

'''
print(mv.tags)
conn = sqlite3.connect('test.db')
cur = conn.cursor()

cur.execute("create table if not exists test_table(tagId text, tag text)")

with open('genome-tags.csv', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		#print(row)
		cur.execute("INSERT INTO test_table VALUES(?,?)",[row[0],row[1]])
	conn.commit()
cur.execute("INSERT INTO test_table VALUES(?,?)",["sdfdsfd","ewrdffd"])
cur.execute("select * from test_table where tagId = ?",[116])
cur.execute("select count(*) from test_table")
#print(cur.fetchall())
cur.execute("drop table test_table")
conn.commit()
conn.close()
inp = input("print_actor_vector ")
(searchId, model) = inp.split(" ")
print("given input "+ searchId)
print("fdafsfa " + model)
'''
#print(dbInfo.getActorMovies('177901'))