def mini_batch_SGD(X,Y,lr, nb_epoch, batch_size):
    a = [0]*X.shape[1]
    result = [a.copy()]
    
    for e in range(nb_epoch):
        c = list(zip(X, Y))
        random.shuffle(c)
        X_train, Y_train = zip(*c)
        X_train, Y_train = np.array(X_train), np.array(Y_train)
        
        for n in range(X_train.shape[0]//batch_size):
            grad = loss_gradient(a, X_train[n*batch_size:(n+1)*batch_size], Y_train[n*batch_size:(n+1)*batch_size])
            for p in range(X.shape[1]):
                a[p] = a[p] - lr /(n+1) * grad[p]
        result.append(a.copy())
    return result

result = mini_batch_SGD(X,Y,0.01,15, 16)

print("Le minimum obtenu est : ", round(loss(result[-1]),5), " pour a = ", result[-1])

display_func(result, loss)
