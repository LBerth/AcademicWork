def stochastic_gradient_descent(X,Y,lr,eps):
    a = [0]*X.shape[1]
    result = [a.copy()]
    n = 1
    
    grad = loss_gradient(a,X,Y)
    a[0] = a[0] - lr/n * grad[0]
    a[1] = a[1] - lr/n * grad[1]
    result.append(a.copy())
    n += 1
    
    while np.sqrt((loss(result[-2])-loss(result[-1]))**2) > eps :
        grad = loss_gradient(a, X, Y)
        a[0] = a[0] - lr/n * grad[0]
        a[1] = a[1] - lr/n * grad[1]
        result.append(a.copy())
        n += 1
        
    return result

result = stochastic_gradient_descent(X,Y,0.01,0.0005)

print("Le minimum obtenu est : ", round(loss(result[-1]),5), " pour a = ", result[-1])

display_func(result, loss)
