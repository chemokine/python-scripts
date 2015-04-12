import os
import pandas as pd
import time
import sys
import pylab as pl
from sklearn import metrics
from sklearn.metrics import roc_curve, auc
resultFolder = "/global/scratch/xiaoxi/projects/GEO/scripts/result/network/cancer/Homo_sapiens__numberOfSimulation-100__numberOfDatasetsToSample-150__correlationMethod-"
def createPairName (pairName):
    pairNameOut = sorted(pairName[[0,1]])
    pairNameOut = pairNameOut[0]+"<==>"+pairNameOut[1]
    return(pairNameOut)
def generateROC (correlationFolder,pvalue):
    FilteredNetwork = []
    goldStandard ="/global/scratch/xiaoxi/projects/GEO/scripts/data/CervicalCancer/3161.GenePairs_0.1_and_0.001_and_tumor.csv"
    files = os.listdir(correlationFolder)
    n=0
    goldStandardData = pd.io.parsers.read_csv(goldStandard)[["name1","name2","t.median.corr"]]
    pairNames = goldStandardData.apply (createPairName,axis=1)
    goldStandardData.index = pairNames
    for file in files:
        n+=1
        file = file.rstrip()
        print file
        # read in data
        table = pd.io.parsers.read_csv(correlationFolder+"/"+file)
        # get significant pairs , extract name1, name2, correlation coefficient, pvalue
        table = table[table["Homo_sapiens.count.pvalue"]<pvalue].iloc[:,[1,2,4,5]]
        # some subset dose not have any significant pair, so move on to next pair, otherwise, the empty dataframe will cause error
        if table.shape[0]<1:
            continue
        # set rownames, use them to find correlation coefficient in gold standard
        myPairNames = table.apply (createPairName,axis=1)
        table.index = myPairNames
        #  find correlation coefficient in gold standard
        goldStandardCorrelation = goldStandardData.loc[myPairNames,"t.median.corr"]
        # for each pair in our network, label it as possitive based on 1) this pair exist in gold standard and 2)correlation directions in our network should be the same as that in gold standard 
        label = goldStandardCorrelation*table["Homo_sapiens.count.correlation.Coefficient"]/abs(goldStandardCorrelation*table["Homo_sapiens.count.correlation.Coefficient"])  # the pairs with different correlation direction will be labeled -1
        # the NAs are those pairs in our network but not in gold standard, so change the label to -1
        label[label!=label] = -1
        # concatenate subsets
        if len(FilteredNetwork)==0:
            FilteredNetwork = table
            outLable = pd.DataFrame({"a":label})
        else:
            FilteredNetwork = FilteredNetwork.append(table, ignore_index=False, verify_integrity=False)
            outLable = outLable.append(pd.DataFrame({"a":label}), ignore_index=False, verify_integrity=False)
    # calculate ROC    
    FilteredNetwork["label"] = outLable
    fpr, tpr, thresholds = metrics.roc_curve(FilteredNetwork["label"], FilteredNetwork["Homo_sapiens.count.pvalue"], pos_label=1)
    roc_auc = auc(fpr, tpr)
    print "Area under the ROC curve : %f" % roc_auc
    # get how many pairs are predicted under this pvalue cutoff
    numberPredicted = FilteredNetwork.shape[0]
    # Plot ROC curve
    pl.clf()
    pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
    pl.plot([0, 1], [0, 1], 'k--')
    pl.xlim([0.0, 1.0])
    pl.ylim([0.0, 1.0])
    pl.xlabel('False Positive Rate')
    pl.ylabel('True Positive Rate')
    pl.title('under pvalue'+str(pvalue)+'numberPredicted is:'+str(numberPredicted)+"\nCancerPaperHas 3162")
    pl.legend(loc="lower right")
    #pl.show()
    pl.savefig(correlationFolder+'-pvalue'+str(pvalue)+'.png')
    
#for folder in ["kendall","spearman","pearson"]:
for folder in ["useBinary-0.67-1.5"]:
    for pvalue in [0.00001,0.0001,0.001,0.01,0.05,0.1]:
        generateROC (resultFolder+folder,pvalue)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
