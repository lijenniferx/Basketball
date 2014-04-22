Basketball
==========

Python code for extracting and analyzing basketball stats

* The webscraping code are contained in 'get_html.py' and 'get_data.py'. 
* 'get_data.py' packages the cleaned data and stores it in a local directory. 

* 'NaiveBayes_hack.py' and 'naive_bayes_mixed.py' are for fitting Naive Bayes classification models 
when the features are a mixture of gaussian and binomial variables.

* 'NaiveBayes_hack.py' is built on top of the naive_bayes module.

* 'naive_bayes_mixed.py' implements the solution directly by creating a new subclass of BaseNB, MixedNB. Thus, it should play better with the rest of the sklearn package. You can drop it into the sklearn directory and import it instead of the standard naive_bayes module.
