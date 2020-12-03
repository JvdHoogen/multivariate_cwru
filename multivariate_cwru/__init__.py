import os,re
import glob
import errno
import random
import urllib.request 
import numpy as np
from scipy.io import loadmat
from sklearn.utils import shuffle
import sys
    
# Filtering values of three sensors    
def keyfilter(dictionary_keys,sens):
    keylist = []
    #print(sens)
    for key in dictionary_keys:
        if "DE_time" in str(key):
            keylist.append(key)
        if "FE_time" in str(key) and (sens == 2 or sens == 3):
            keylist.append(key)
        if "BA_time" in str(key) and sens == 3:
            keylist.append(key)           
    if sens == 2:
        return keylist[0],keylist[1]
    if sens == 3:
        return keylist[0],keylist[1],keylist[2] 
    else:
        return keylist[0]   


 
class CWRU:
    # Experiment = experiment name, length = length of sequence, trainsplit = division of train and testsplit,
    # Seed = seed for random shuffle, sens = the amount of sensors to use in the preprocessing, 
    # Rpm = rotations per minute (four different options are available) multiple inputs are possible, normal_condition = boolean operator to include normal conditions or not
    def __init__(self, experiment, length, trainsplit, seed,sens, *rpm, normal_condition = True):
        if experiment not in ('12DriveEndFault', '12FanEndFault', '48DriveEndFault'):
            print("wrong experiment name: {}".format(experiment))
            sys.exit(1) 
        for i in rpm:
            if i not in ('1797', '1772', '1750', '1730'): 
                print("wrong rpm value: {}".format(rpm))
                sys.exit(1)
        # Root directory of all data and loading in text file
        rdir = os.path.join(os.path.expanduser('~'), 'Datasets/CWRU')
        cur_path = os.path.dirname(__file__)
        fmeta = os.path.join(cur_path, "datafiles.txt")

        # Read text file and load all separate http addresses
        all_lines = open(fmeta).readlines() 
        lines = []
        if normal_condition == True:
            for line in all_lines:
                l = line.split()
                if (l[0] in experiment or l[0] == 'NormalBaseline') and l[1] in rpm:
                    lines.append(l)    
        else: 
            for line in all_lines:
                l = line.split()
                if l[0] in experiment and l[1] in rpm:
                    lines.append(l)

        self.sens = sens
        self.length = length  # sequence length
        self.seed = seed
        self.trainsplit = trainsplit
        self._sequence_data(rdir, lines)
        self._shuffle() # shuffle training and test arrays
        self.labels = tuple(line[2] for line in lines) # Label names 
        self.nclasses = len(self.labels)  # Number of classes
 
    # Create directories for the download files to store
    def _mkdir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                print("can't create directory '{}''".format(path))
                exit(1)
 
    # Download files from corresponding HTML addresses from 'metadata.txt'
    def _download(self, fpath, link):
        print("Downloading to: '{}'".format(fpath))
        urllib.request.urlretrieve(link, fpath)
        
    # Extract data from .mat files and preprocess them into sequences datasets
    def _sequence_data(self, rdir, infos):
        self.x_train = np.zeros((0, self.length, self.sens))
        self.x_test = np.zeros((0, self.length, self.sens))
        self.y_train = []
        self.y_test = []
        for idx, info in enumerate(infos):
            # Directory of this file
            fdir = os.path.join(rdir, info[0], info[1])
            self._mkdir(fdir)
            fpath = os.path.join(fdir, info[2] + '.mat')
            if not os.path.exists(fpath):
                self._download(fpath, info[3])
            
            # Load in files and combine into one time series
            mat_dict = loadmat(fpath)
            if self.sens == 2:
                key1,key2 = keyfilter(mat_dict.keys(),self.sens)
                time_series = np.hstack((mat_dict[key1],mat_dict[key2]))
            if self.sens == 3:
                key1,key2,key3 = keyfilter(mat_dict.keys(),self.sens)
                time_series = np.hstack((mat_dict[key1],mat_dict[key2],mat_dict[key3]))
            if self.sens == 1:
                key1 = keyfilter(mat_dict.keys(),self.sens)
                time_series = np.array((mat_dict[key1]))
            #key1,key2 = keyfilter(mat_dict.keys(),2)
            #time_series = np.hstack((mat_dict[key1],mat_dict[key2]))
            


            # Remove leftover datapoints based on sequence length
            idx_last = -(time_series.shape[0] % self.length)
            if idx_last < 0:    
                clips = time_series[:idx_last].reshape(-1, self.length,self.sens)
            else:
                clips = time_series[idx_last:].reshape(-1, self.length,self.sens)                

            #print(time_series.shape)
            

            # Partition train and test set in separate arrays
            n = clips.shape[0]
            #print(n)
            n_split = int(self.trainsplit * n)
            self.x_train = np.vstack((self.x_train, clips[:n_split]))
            self.x_test = np.vstack((self.x_test, clips[n_split:]))
            self.y_train += [idx] * n_split
            self.y_test += [idx] * (clips.shape[0] - n_split)

    def _shuffle(self):
        # Shuffle training samples
        index = list(range(self.x_train.shape[0]))
        random.Random(self.seed).shuffle(index)
        self.x_train = self.x_train[index]
        self.y_train = np.array(tuple(self.y_train[i] for i in index))
 
        # Shuffle test samples
        index = list(range(self.x_test.shape[0]))
        random.Random(self.seed).shuffle(index)
        self.x_test = self.x_test[index]
        self.y_test = np.array(tuple(self.y_test[i] for i in index))





