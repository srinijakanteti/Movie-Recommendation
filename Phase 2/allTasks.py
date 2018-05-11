import utils
import sqlite3
import tfCalc as tf
import tfIdfCalc as idf
import genreMovieTags as genmov
import similarity as similarity
import genreDiff as gd
import svd as svd

# Take the input from the user
print("Select the task to perform")
print("1. Actor Tag Vector")
print("2. Genre Tag Vector")
print("3. User Tag Vector")
print("4. Differentiate Genres")
print("5. Calculate SVD for genres")
print("6. Generate Movie tags for Genre")
print("7. Find Similarity Matrix")
print("8. Find Personalized Page Rank")
print("9. Find SVD on Similarity Matrix and show Latent Semantics")
print("10.Form non-overlapping groups")
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
elif(searchType == '6'):
	(searchId,model) = input("print_genre_movie_vector ").split(" ")
elif(searchType == '5'):
	(searchId,model) = input("get_svd ").split(" ")
elif(searchType == '7'):
	(searchId,model) = input("get_similarity_matrix ").split(" ")
elif(searchType == '8'):
	(searchId,model) = input("ppr_input_seed_matrix ").split(" ")
elif(searchType == '9'):
	(searchId,model) = input("get_latent semantics_on ").split(" ")
elif(searchType == '10'):
	(searchId,model) = input("form_groups_semantics ").split(" ")
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
		elif(searchType == '6'):
			print(genmov.getGenreMovieTags(searchId))
		elif(searchType == '7'):
			if(searchId=='actor'):
			    print(similarity.getSimilarityMat(searchId))
			elif(searchId=='coactor'):
			    print(similarity.CoactorSimilarity(searchId))
		
	elif(model == 'tf-idf'):
		if(searchType == '1'):
			print(idf.idfActorTag(searchId))
		elif(searchType == '2'):
			print(idf.idfGenreTag(searchId))
		elif(searchType == '3'):
			print(idf.idfUserTag(searchId))
	elif(model == 'svd'):
		if(searchType =='5'):
		   Mat = svd.genSVDMatrix(searchId)
		   svd.Calcsvd(Mat)
	elif(model=='actor'):
		if(searchType =='8'):
		   Sim=similarity.getSimilarityMat(model)
		   Mat = similarity.PersonalizedPageRank(Sim,searchId)
	elif(searchType == '8'):
		if(searchId=='actor-actor'):
			Sim=similarity.getSimilarityMat(searchId)
			u,s,v=svd.Calcsvd(Sim)
			for i in range(1,model):
			    a.append(v[i])
			print(a)
	elif(searchType == '9'):
		if(searchId == 'groups'):
			Sim=similarity.getSimilarityMat(searchId)
			u,s,v=svd.Calcsvd(Sim)
			for i in range(1,model):
			    a.append(v[i])
			print(svd.form_groups_semantics(a,model))

	else:
		#task4
		print(gd.differGenre(g1,g2,model))
getVector(searchType, searchId, model)
