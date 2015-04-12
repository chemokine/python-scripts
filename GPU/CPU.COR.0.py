from numbapro import vectorize
from numpy import arange
import numpy as np
from scipy import stats


@vectorize(['float32(float32, float32)'], target='gpu') # default to 'cpu'


def add2(a, b):
#    a = a+1
#    b = b+1
#    print ">>>>>>>>>>>>>>>>>>>\nprinting a"
    myS = stats.pearsonr(myM[:,a],myM[:,b])
#    print b
#    print "\n\n\n"
    return myS[1]
    
    
myM = np.random.rand(30,30)
X = arange(1,14, dtype='float32')
Y = arange(15,28, dtype='float32')
#print myM
print "start print"
print add2(X, Y)
print "done print"


stats.pearsonr(myM[:,4],myM[:,22])

stats.pearsonr(myM[4,:],myM[22,:])

stats.pearsonr(X,Y)

