import dbInfo as di

movies = di.getAllMovies()
movYrs = di.getAllMovieYrs()
delMovies = []
for mv in movYrs:
	if(mv[1]<2004):
		delMovies.append(mv[0])
print("del movies",len(delMovies))

for mov in delMovies:
	di.delRows("mlmovies","movie_id",mov)
	print("movie =",mov)
	di.delRows("mlratings","movie_id",mov)
	di.delRows("mltags","movie_id",mov)
	di.delRows("movie_actor","movie_id",mov)
	di.delRows("movie_info","movie_id",mov)

allUsers = di.getAllUsers()
delUsers = []
for usr in allUsers:
	if(int(usr[0]) <= 71550):
		delUsers.append(usr[0])
print("delUsers", len(delUsers))
for usr in delUsers:
	di.delRows("mlratings","user_id",usr)
	di.delRows("mltags","user_id",usr)
	di.delRows("mlusers","user_id",usr)
	print("usr =",usr)
allTags = di.getAllTags()
allActors = di.getAllActors()
mlTags = di.getMLtags()
mvActors = di.getMvActors()
mvActs = []
mlTg = []
for act in mvActors:
	mvActs.append(act[0])
for tg in mlTags:
	mlTg.append(tg[0])
for act in allActors:
	if(act[0] not in mvActs):
		print("actor = ",act[0])
		di.delRows("imdb_actor_info","actor_id",act[0])
for tag in allTags:
	if(tag[0] not in mlTg):
		print("tag =",tag[0])
		di.delRows("genome_tags","tag_id",tag[0])
allTags = di.getAllTags()
allActors = di.getAllActors()
movies = di.getAllMovies()
allUsers = di.getAllUsers()
print(len(allActors),len(allTags),len(movies),len(allUsers))