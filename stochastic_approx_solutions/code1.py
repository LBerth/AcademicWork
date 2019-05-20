
def fixed_step_descent(function, gradient, eps, step_size):
    x = [-1.5,-1.5]
    result = [x.copy()]
    
    g = gradient(x)
    x[0] = x[0] - step_size * g[0]
    x[1] = x[1] - step_size * g[1]
    result.append(x.copy())
    
    while np.sqrt((function(result[-2])-function(result[-1]))**2) > eps :
        g = gradient(x)
        x[0] = x[0] - step_size * g[0]
        x[1] = x[1] - step_size * g[1]
        result.append(x.copy())
    return result

result = fixed_step_descent(function, gradient, 0.00001, 0.001)
print("Le minimum obtenu est : ", round(function(result[-1]),5), " pour a = ", result[-1])

display_func(result, function)
