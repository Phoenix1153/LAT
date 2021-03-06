'''
@author: liuaishan
@contact: liuaishan@buaa.edu.cn
@file: utils.py
@time: 2018/10/28 12:30
@desc:
'''

import os
import numpy as np
import pickle
import torch

# read data from files
# @return (numpy array) data, label, len

def read_data(file_path):

    if not os.path.exists(file_path):
        return None, None, 0

    with open(file_path, 'rb') as fr:
        data_set = pickle.load(fr)
        size = len(data_set[0])
        list_data = []
        list_label = []
        # illegal data
        if not len(data_set[0]) == len(data_set[1]):
            return None, None, 0

        data = torch.unsqueeze(data_set[0], dim=1).type(torch.FloatTensor)[:size]
        label = data_set[1][:size]
        #data = data_set[0]
        #label = data_set[1]
        data = np.asarray(data)
        label = np.asarray(label)
        return data, label, size
'''
def read_data(file_path):

    if not os.path.exists(file_path):
        return None, None, 0

    with open(file_path, 'rb') as fr:
        data_set = pickle.load(fr)
        size = len(data_set)
        list_data = []
        list_label = []
        for item in data_set:
            list_data.append(item[0].numpy())
            list_label.append(item[1].cpu().numpy())

        data = np.asarray(list_data)
        label = np.asarray(list_label)
        return data, label, size
'''