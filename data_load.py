import cPickle
import gzip
import numpy as np

def load_data():
    f=gzip.open('./data/train_data.pkl.gz','rb')
    training_data=Pickle.load(f)
    fclose()
    f=gzip.open('./data/test_data.pkl.gz','rb')
    test_data=Pickle.load(f)
    fclose()
    return (training_data, test_data)
