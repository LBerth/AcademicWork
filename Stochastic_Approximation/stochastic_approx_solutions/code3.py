
def loss(a):
    return sum([(Y[i] - a[0]*X[i][0] - a[1]*X[i][1])**2 for i in range(n)])

display_func([], loss)
