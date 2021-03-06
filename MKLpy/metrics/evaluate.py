import numpy as np
from cvxopt import matrix,solvers,spdiag

'''SOLO OPERAZIONI CHE DATO 1 KERNEL RESTITUISCONO UNA MISURA CALCOLATA SU UNA CERTA METRICA.
Possono esser utilizzate come euristiche'''

def radius(K,Y=None):
    n = K.shape[0]
    P = 2 * matrix(K)
    p = -matrix([K[i,i] for i in range(n)])
    G = -spdiag([1.0] * n)
    h = matrix([0.0] * n)
    A = matrix([1.0] * n).T
    b = matrix([1.0])
    solvers.options['show_progress']=False
    sol = solvers.qp(P,p,G,h,A,b)
    #return abs(sol['primal objective'])
    return np.sqrt(abs(sol['primal objective']))

def margin(K,Y):
    n = Y.shape[0]
    YY = spdiag(list(Y))
    P = 2*(YY*matrix(K)*YY)
    p = matrix([0.0]*n)
    G = -spdiag([1.0]*n)
    h = matrix([0.0]*n)
    A = matrix([[1.0 if Y[i]==+1 else 0 for i in range(n)],
                [1.0 if Y[j]==-1 else 0 for j in range(n)]]).T
    b = matrix([[1.0],[1.0]],(2,1))
    solvers.options['show_progress']=False
    sol = solvers.qp(P,p,G,h,A,b)
    return np.sqrt(sol['primal objective'])/2.0#prendo la distanza dall'iperpiano


def ratio(K,Y):
    #radius^2/rho^2
    n = Y.shape[0]    
    r2 = radius(K)**2
    m2 = (margin(K,Y)*1)**2
    return (r2/m2)/n
    return ((radius(K)**2)/(margin(K,Y)**2))/n




def trace(K):
    if K.shape[0] != K.shape[1]:
        raise TypeError("the trace is available only for square matrices")
    return sum([K[i,i] for i in range(K.shape[0])])

def frobenius(K):
    return np.sqrt(np.sum(K**2))

def spectral_ratio(K,Y=None,norm=True):
    '''normalized spectral ratio'''
    n = K.shape[0]
    c = trace(K)/frobenius(K)
    if norm:
        return (c-1)/np.sqrt(n)-1
    else:
        return c





