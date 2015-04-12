from numbapro import vectorize
import sys
from numpy import arange
import numpy as np
from scipy import stats
import pandas as pd
import mysql.connector
import MySQLdb


mysql_cn= MySQLdb.connect(host='128.193.185.85', 
                user='xiaoxi', passwd='dfdongr8j1ko6', 
                db='ifng.akk.glucose')
df_mysql = pd.read_sql('select * from gene_expressiondata_microarray_nov_2014_ko_rifng;', con=mysql_cn)    
print 'loaded dataframe from MySQL. records:', len(df_mysql)
mysql_cn.close()

stats.pearsonr(df_mysql['microarray_Nov_2014_IFNg_KO_rIFNg_17'],df_mysql['microarray_Nov_2014_IFNg_KO_rIFNg_9'])


tt = df_mysql.transpose()
stats.pearsonr(tt.iloc[2:,1],tt.iloc[2:,2])




#cnx = mysql.connector.connect(user='xiaoxi', password='dfdongr8j1ko6',
#                              host='128.193.185.85',
#                              database='ifng.akk.glucose')

#cursor = cnx.cursor()
#query = ("select * from gene_expressiondata_microarray_nov_2014_ko_rifng")
#cursor.execute(query)
#for (GeneID) in cursor:
#	print GeneID
#	sys.exit()


@vectorize(['float32(float32, float32)'], target='gpu') # default to 'cpu'
def add2(a, b):
#    a = a+1
#    b = b+1
    print ">>>>>>>>>>>>>>>>>>>\nprinting a"
    print a
    #print tt.iloc[2:,a]
   #myS = stats.pearsonr(tt.iloc[2:,a],tt.iloc[b:,2])
    #print myS
    print "\n\n\n"
    return a + b
    
#myM = np.random.rand(30,30)
x = arange(1,14, dtype='float32')
y = arange(15,28, dtype='float32')

add2(x, y)



#stats.pearsonr(myM[:,4],myM[:,22])

#stats.pearsonr(myM[4,:],myM[22,:])

#stats.pearsonr(X,Y)

