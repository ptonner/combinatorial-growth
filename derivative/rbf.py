from GPy import RBF
import numpy as np

class RBFDerivative(RBF):

    def K(self,X,X2):
        k = super(RBFDerivative, self).K(X,X2)
        if X2 is None:
            diff = np.zeros((X.shape[0],X.shape[0]))
            for i in range(X.shape[0]):
                for j in range(X.shape[0]):
                    diff[i,j] = X[i,0] - X[j,0]
                    #diff[i,j] = -X[i,0] + X[j,0]

            return (1./(self.lengthscale[0]))*(1-(1./(self.lengthscale[0]))*(diff**2))*k
            #return k * (-1./(self.lengthscale[0]))*diff
        else:
            #X2 is derivative obs

            diff = np.zeros((X.shape[0],X2.shape[0]))
            for i in range(X.shape[0]):
                for j in range(X2.shape[0]):
                    diff[i,j] = X[i,0] - X2[j,0]
                    #diff[i,j] = -X[i,0] + X[j,0]

            return k * (1./(self.lengthscale[0]))*diff
            #return (1./(self.lengthscale[0]))*(1-(1./(self.lengthscale[0]))*(diff**2))*k
