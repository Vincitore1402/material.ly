
from time import time

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn import manifold, datasets

# Next line to silence pyflakes. This import is needed.
Axes3D


# # Points from DB
# data = getVisData()
# print (data[0])

def startLearning(myX):
    n_points = 1000
    X = myX
    print (type(X))
    #color = datasets.samples_generator.make_s_curve(n_points, random_state=0)

    # X, color = datasets.samples_generator.make_s_curve(n_points, random_state=0)
    # print (X[0])
    # print (myX[0])
    # print (len(X[0]))
    n_neighbors = 10
    n_components = 2

    fig = plt.figure(figsize=(15, 8))
    plt.suptitle("Manifold Learning with %i points, %i neighbors"
                 % (1000, n_neighbors), fontsize=14)

    ax = fig.add_subplot(251, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], cmap=plt.cm.Spectral)
    ax.view_init(4, -72)

    methods = ['standard', 'ltsa', 'hessian', 'modified']
    labels = ['LLE', 'LTSA', 'Hessian LLE', 'Modified LLE']

    for i, method in enumerate(methods):
        try:
            t0 = time()
            Y = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
                                              eigen_solver='auto',
                                              method=method).fit_transform(X)
            t1 = time()
            print("%s: %.2g sec" % (methods[i], t1 - t0))

            ax = fig.add_subplot(252 + i)
            plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
            plt.title("%s (%.2g sec)" % (labels[i], t1 - t0))
            ax.xaxis.set_major_formatter(NullFormatter())
            ax.yaxis.set_major_formatter(NullFormatter())
            plt.axis('tight')
        except:
            pass

    t0 = time()
    Y = manifold.Isomap(n_neighbors, n_components).fit_transform(X)
    t1 = time()
    print("Isomap: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(257)
    plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
    plt.title("Isomap (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    t0 = time()
    mds = manifold.MDS(n_components, max_iter=100, n_init=1)
    Y = mds.fit_transform(X)
    t1 = time()
    print("MDS: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(258)
    plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
    plt.title("MDS (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    t0 = time()
    se = manifold.SpectralEmbedding(n_components=n_components,
                                    n_neighbors=n_neighbors)
    Y = se.fit_transform(X)
    t1 = time()
    print("SpectralEmbedding: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(259)
    plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
    plt.title("SpectralEmbedding (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')

    t0 = time()
    tsne = manifold.TSNE(n_components=n_components, init='pca', random_state=0)
    Y = tsne.fit_transform(X)
    t1 = time()
    print("t-SNE: %.2g sec" % (t1 - t0))
    ax = fig.add_subplot(2, 5, 10)
    plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
    plt.title("t-SNE (%.2g sec)" % (t1 - t0))
    ax.xaxis.set_major_formatter(NullFormatter())
    ax.yaxis.set_major_formatter(NullFormatter())
    plt.axis('tight')
    plt.savefig('pic {0}.png'.format(n_neighbors))

    # plt.show()

    return {
        'x': Y[:, 0],
        'y': Y[:, 1]
    }

# startLearning()


# res = np.loadtxt('numpyData.csv', dtype=float, delimiter=';')

# mask = np.any(np.not_equal(res, 0.), axis=0)
# arr = res[:,mask]

# arr = np.unique(arr, axis=0)

# arr = arr[:]

# print arr



# startLearning(arr)

#np.savetxt('test.csv', arr, delimiter=';')