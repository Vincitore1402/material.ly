"""
=========================================
 Comparison of Manifold Learning methods
=========================================

An illustration of dimensionality reduction on the S-curve dataset
with various manifold learning methods.

For a discussion and comparison of these algorithms, see the
:ref:`manifold module page <manifold>`

For a similar example, where the methods are applied to a
sphere dataset, see :ref:`sphx_glr_auto_examples_manifold_plot_manifold_sphere.py`

Note that the purpose of the MDS is to find a low-dimensional
representation of the data (here 2D) in which the distances respect well
the distances in the original high-dimensional space, unlike other
manifold-learning algorithms, it does not seeks an isotropic
representation of the data in the low-dimensional space.
"""

# Author: Jake Vanderplas -- <vanderplas@astro.washington.edu>


from time import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import NullFormatter

from sklearn import manifold, datasets
import numpy as np

# Next line to silence pyflakes. This import is needed.
Axes3D


def start_manifold_learning(input):
  # res = np.loadtxt('numpyData.csv', dtype=float, delimiter=';')

  # todo check mask
  # mask = np.any(np.not_equal(input, 0.), axis=0)
  # arr = input['numpyArr'][:,mask]
  #
  # arr = np.unique(arr, axis=0)
  #
  # arr = arr[:]

  n_points = 1000
  X = input['numpyArr']
  print(type(X))
  color = datasets.samples_generator.make_s_curve(n_points, random_state=0)

  # X, color = datasets.samples_generator.make_s_curve(n_points, random_state=0)
  # print (X[0])
  # print (input[0])
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

  res = {}
  # try:
  #     for i, method in enumerate(methods):
  #         t0 = time()
  #         Y = manifold.LocallyLinearEmbedding(n_neighbors, n_components,
  #                                             eigen_solver='auto',
  #                                             method=method).fit_transform(X)
  #         t1 = time()
  #         print("%s: %.2g sec" % (methods[i], t1 - t0))

  #         ax = fig.add_subplot(252 + i)
  #         plt.scatter(Y[:, 0], Y[:, 1], cmap=plt.cm.Spectral)
  #         plt.title("%s (%.2g sec)" % (labels[i], t1 - t0))
  #         ax.xaxis.set_major_formatter(NullFormatter())
  #         ax.yaxis.set_major_formatter(NullFormatter())
  #         plt.axis('tight')
  #         res[method] = {
  #             'x' : Y[:, 0].tolist(),
  #             'y' : Y[:, 1].tolist()
  #           }
  # except:
  #     pass
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

  res['Isomap'] = {
    'x': Y[:, 0].tolist(),
    'y': Y[:, 1].tolist(),
    'ids': input['ids'],
    'matInfo': input['matInfo']
  }
  print('Learning data: ')
  print('x: ' + str(len(res['Isomap']['x'])))
  print('y: ' + str(len(res['Isomap']['y'])))
  print('ids: ' + str(len(res['Isomap']['ids'])))
  print('matInfo: ' + str(len(res['Isomap']['matInfo'])))

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

  res['MDS'] = {
    'x': Y[:, 0].tolist(),
    'y': Y[:, 1].tolist(),
    'ids': input['ids'],
    'matInfo': input['matInfo']
  }

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

  res['Spectral Embedding'] = {
    'x': Y[:, 0].tolist(),
    'y': Y[:, 1].tolist(),
    'ids': input['ids'],
    'matInfo': input['matInfo']
  }

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

  res['TSNE'] = {
    'x': Y[:, 0].tolist(),
    'y': Y[:, 1].tolist(),
    'ids': input['ids'],
    'matInfo': input['matInfo']
  }

  # plt.show()
  # return plt
  # np.savetxt('X.csv', X)
  # np.savetxt('Y.csv', Y)

  # res = {
  #     'x': Y[:,0],
  #     'y': Y[:,1]
  # }

  return res


def start_regression_learning(input):
  import numpy as np
  from sklearn.linear_model import LinearRegression
  X = input['x']
  y = input['y']

  # X = np.array([[1, 1], [1, 2], [2, 2], [2, 3]])
  # # y = 1 * x_0 + 2 * x_1 + 3
  # y = np.dot(X, np.array([1, 2])) + 3

  # todo Errors is here
  reg = LinearRegression().fit(X, y)
  # reg.score(X, y)
  # reg.intercept_
  predict = reg.predict(np.array([[3, 5]]))
  return predict

# startRegressionLearning()
