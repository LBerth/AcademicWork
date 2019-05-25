
def loss_gradient(a,X,Y):
    grad = [0]*X.shape[1]
    error = [Y[i] - a[0]*X[i][0] - a[1]*X[i][1] for i in range(X.shape[0])]
    grad[0] = 2 * sum([- error[i] for i in range(X.shape[0])])
    grad[1] = 2 * sum([- X[i][1] * error[i] for i in range(X.shape[0])])
    return grad

def gradient_descent(X,Y, eps, step_size):
    a = [0]*X.shape[1]
    result = [a.copy()]
    
    grad = loss_gradient(a,X,Y)
    a[0] = a[0] - step_size * grad[0]
    a[1] = a[1] - step_size * grad[1]
    result.append(a.copy())
    
    while np.sqrt((loss(result[-2])-loss(result[-1]))**2) > eps :
        grad = loss_gradient(a,X,Y)
        a[0] = a[0] - step_size * grad[0]
        a[1] = a[1] - step_size * grad[1]
        result.append(a.copy())
        
    return result

result = gradient_descent(X,Y,0.0001, 0.001)

print("Le minimum obtenu est : ", round(loss(result[-1]),5), " pour a = ", result[-1])

display_func(result, loss)
