import tensorDecomp as td
import dbInfo as di
import utils
import tensorly as tl
tl.set_backend('numpy')
import warnings
warnings.filterwarnings("ignore")
#np.set_printoptions(threshold=np.nan)

numGroups = 5
numSemantics = 5

vect, actors, movies, years = td.vectActMovYr()
tens = td.vectToTens(vect)
print("The actor-movie-year tensor:\n",tens, "\n\nshape of tensor: ",tens.shape)
factors = td.tensDecomp(tens, numSemantics)

#for i in range(len(factors)):
#	print(tl.unfold(factors[i],1))
actorSemantics = tl.unfold(factors[0],1)
movieSemantics = tl.unfold(factors[1],1)
yearSemantics = tl.unfold(factors[2],1)

print("\n\nActor Semantics:")
for sem in actorSemantics:
	print("\n\n",utils.rankSem(sem, actors))
print("\n\nMovie Semantics:")
for sem in movieSemantics:
	print("\n\n",utils.rankSem(sem, movies))
print("\n\nYear Semantics:")
for sem in yearSemantics:
	print("\n\n",utils.rankSem(sem, years))

actList = di.getAllActorNames()
movList = di.getAllMovieNames()
years = di.getAllYears()

actGroups = utils.form_groups_semantics(factors[0], actList, numGroups)
movGroups = utils.form_groups_semantics(factors[1], movList, numGroups)
yearGroups = utils.form_groups_semantics(factors[2], years, numGroups)

print("\n\n5 Non overlapping Actor groups:")
for grp in actGroups.keys():
	print("\n\n",grp, ":", actGroups[grp])
print("\n\n5 Non overlapping Movie groups:")
for grp in movGroups.keys():
	print("\n\n",grp, ":", movGroups[grp])
print("\n\n5 Non overlapping Year groups:")
for grp in yearGroups.keys():
	print("\n\n",grp, ":", yearGroups[grp])
