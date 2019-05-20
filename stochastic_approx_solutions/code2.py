
a = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, Y))
print("Solution exacte : ", a)
