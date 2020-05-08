from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

X = [
	[1, 18],
	[2, 7],
	[3, 22],
	[4, 12],
	[5, 24]
]
linked = linkage(X, 'single')
print(linked)
labelList = ['A','B','C','D','E']

plt.figure(figsize=(10, 7))
dendrogram(linked,
            orientation='top',
            labels=labelList,
            distance_sort='descending',
            show_leaf_counts=True)
plt.show()