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

vect, tags, movies, ratings = td.vectTagMovRat()
tens = td.vectToTens(vect)
print("The tag-movie-ratings tensor:\n",tens, "\n\nshape of tensor: ",tens.shape)
factors = td.tensDecomp(tens, numSemantics)

#for i in range(len(factors)):
#	print(tl.unfold(factors[i],1))
tagSemantics = tl.unfold(factors[0],1)
movieSemantics = tl.unfold(factors[1],1)
rateSemantics = tl.unfold(factors[2],1)

print("\n\nTag Semantics:")
for sem in tagSemantics:
	print("\n\n",utils.rankSem(sem, tags))
print("\n\nMovie Semantics:")
for sem in movieSemantics:
	print("\n\n",utils.rankSem(sem, movies))
print("\n\nRating Semantics:")
for sem in rateSemantics:
	print("\n\n",utils.rankSem(sem, ratings))

tagList = di.getAllTagNames()
movList = di.getAllMovieNames()
rates = di.getAllRatings()

tagGroups = utils.form_groups_semantics(factors[0], tagList, numGroups)
movGroups = utils.form_groups_semantics(factors[1], movList, numGroups)
rtngGroups = utils.form_groups_semantics(factors[2], rates, numGroups)

print("\n\n5 Non overlapping Tag groups:")
for grp in tagGroups.keys():
	print("\n\n",grp, ":", tagGroups[grp])
print("\n\n5 Non overlapping Movie groups:")
for grp in movGroups.keys():
	print("\n\n",grp, ":", movGroups[grp])
print("\n\n5 Non overlapping Rating groups:")
for grp in rtngGroups.keys():
	print("\n\n",grp, ":", rtngGroups[grp])
