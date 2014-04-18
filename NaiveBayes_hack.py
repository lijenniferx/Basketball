from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import cross_validation
import random
random.seed()

def cross_validate_Naive_Bayes(Xcont,Xbin,Y,iter_no):
    '''this function takes in a set of continuous features (Xcont), and a set of binary features (Xbin), 
    calculates the posteriors using the built in implementation of Naive Bayes for gaussian and binomial data in sklearn
    and combines the posterior probabilities for the two feature subsets. 
    Y: the outcomes
    iter_no: the number of shuffled datasets to be tested''' 
    
    
    Gmodel=GaussianNB()
    Bmodel=BernoulliNB()

    cv=cross_validation.ShuffleSplit(len(Y),n_iter=iter_no,test_size=0.25,random_state=1)  #### generates cross validation indices 
    accuracy=[]
    
    for train_cv,test_cv in cv: 
        
        #### setting up the training data for each shuffle
        train_Xcont=[Xcont[i] for i in train_cv]
        train_Xbin=[[Xbin[i]] for i in train_cv]
        train_Y=[Y[i] for i in train_cv] 
        
        
        ### setting up the testing data for each shuffle
        test_Xcont=[Xcont[i] for i in test_cv]
        test_Xbin=[[Xbin[i]] for i in test_cv]
        test_Y=[Y[i] for i in test_cv] 
        
        ##### fitting the training data
        model_cont=Gmodel.fit(train_Xcont,train_Y)
        model_bin=Bmodel.fit(train_Xbin,train_Y)
        
        #### combining the posterior probabilities
        denominator=[(sum(train_Y)/len(train_Y))**1,(1-sum(train_Y)/len(train_Y))**1] ### probability of each outcome: P(C)
        numerator=model_bin.predict_proba(test_Xbin)*model_cont.predict_proba(test_Xcont)  ### posterior probabilities: P(C|Xcont), P(C|Xbin)
        prediction=array(map(lambda x: x[1]>x[0],numerator/denominator))  ### combining probabilities and then selecting the appropriate outcome
        
        accuracy.append(sum(abs(prediction-test_Y))/len(test_cv))  ### comparing the predictions with the actual outcomes 
        
    return accuracy
        