import utils
import sqlite3
import tfCalc as tf
import tfIdfCalc as idf
import genreDiff as gd

# Take the input from the user
print("Select the task to perform")
print("1. Actor Tag Vector")
print("2. Genre Tag Vector")
print("3. User Tag Vector")
print("4. Differentiate Genres")
searchType = input("Your option: ")

g1=""
g2=""
model=""
searchId=""

if(searchType == '1'):
	(searchId,model) = input("print_actor_vector ").split(" ")
elif(searchType == '2'):
	(searchId,model) = input("print_genre_vector ").split(" ")
elif(searchType == '3'):
	(searchId,model) = input("print_user_vector ").split(" ")
else:
	(g1,g2,model) = input("differentiate_genre ").split(" ")

#Print the output here
def getVector(searchType, searchId, model):
	if(model == 'tf'):
		if(searchType == '1'):
			print(tf.tfActorTag(searchId))
		elif(searchType == '2'):
			print(tf.tfGenreTag(searchId))
		elif(searchType == '3'):
			print(tf.tfUserTag(searchId))
	elif(model == 'tf-idf'):
		if(searchType == '1'):
			idfActVector = idf.idfActorTag()
			print(idf.tfIdfActorTag(searchId, idfActVector))
		elif(searchType == '2'):
			idfGenVector = idfGenreTag()
			print(idf.tfIdfGenreTag(searchId, idfGenVector))
		elif(searchType == '3'):
			idfUserVector = idfUserTag()
			print(idf.tfIdfUserTag(searchId, idfUserVector))
	else:
		#task4
		print(gd.differGenre(g1,g2,model))
getVector(searchType, searchId, model)
