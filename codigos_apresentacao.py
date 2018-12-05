import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model

def func1():
    f, ax = plt.subplots(figsize=(7.5, 5))
    x = np.arange(1,21).reshape(-1, 1)
    y = 2*x + 10
    ax.scatter(x, y)
    model = linear_model.LinearRegression().fit(x, y)
    ax.plot(x, model.predict(x), color='red', linewidth=2.)
    ax.legend(['Y = {}*X + {}'.format(int(model.coef_[0][0]), int(model.intercept_[0]))])
    ax.set(xlabel = 'X', ylabel = 'Y', title = "Curva linear")
    plt.show()
    
def func2():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 10*2**x1
    ax1.scatter(x1, y1)
    ax1.legend(['Y = 10*2**X'])
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Curva exponencial")
    
    x2 = x1
    y2 = np.log(y1)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(['Y = {:0.4}*X + {}'.format(model.coef_[0][0], int(model.intercept_[0]))])
    ax2.set(xlabel = 'X', ylabel = 'log(Y)', title = "Curva linear")
    plt.show()
    
def func3():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 5*x1**6
    ax1.scatter(x1, y1)
    ax1.legend(['Y = 5*X**6'])
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Curva de potência")

    x2 = np.log(x1)
    y2 = np.log(y1)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(['Y = {:0.4}*X + {}'.format(model.coef_[0][0], int(model.intercept_[0]))])
    ax2.set(xlabel = 'log(X)', ylabel = 'log(Y)', title = "Curva linear")
    plt.show()

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 2*x1**3 + x1**2 + 10
    ax1.scatter(x1, y1)
    ax1.legend(['Y = 2*X**2 + X**2 + 10'])
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Curva polinomial")

    x2 = np.log(x1)
    y2 = np.log(y1)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(['Y = {:0.4}*X + {}'.format(model.coef_[0][0], int(model.intercept_[0]))])
    ax2.set(xlabel = 'log(X)', ylabel = 'log(Y)', title = "Curva linear")
    plt.show()
    
def func4():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x1 = np.arange(1,21).reshape(-1, 1)
    y1 = 2*x1 + 3
    ax1.scatter(x1, y1)
    model = linear_model.LinearRegression().fit(x1, y1)
    ax1.plot(x1, model.predict(x1), color='red', linewidth=2.)
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Y = 2*X + 3")
    ax1.legend(["R2 = {:0.4}".format(model.score(x1, y1))])

    x2 = x1
    y2 = np.random.random(20)
    ax2.scatter(x2, y2)
    model = linear_model.LinearRegression().fit(x2, y2)
    ax2.plot(x2, model.predict(x2), color='red', linewidth=2.)
    ax2.legend(["R2 = {:0.4}".format(model.score(x2, y2))])
    ax2.set(xlabel = 'X', ylabel = 'Y', title = "Y = aleatório")
    plt.show()
    
def func5():
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    x = np.arange(1,10).reshape(-1, 1)
    y = np.append(2*x[:-1], [1])
    ax1.scatter(x, y)
    model = linear_model.LinearRegression().fit(x, y)
    ax1.set(xlabel = 'X', ylabel = 'Y', title = "Com o outlier")
    ax1.plot(x, model.predict(x), color='red', linewidth=2.)

    x2 = x
    y2 = 2*x[:-1]
    ax2.scatter(x2, np.append(y2, [1]))
    model = linear_model.LinearRegression().fit(x2[:-1], y2)
    ax2.set(xlabel = 'X', ylabel = 'Y', title = "Sem o outlier")
    ax2.plot(x2[:-1], model.predict(x2[:-1]), color='red', linewidth=2.)
    plt.show()
    