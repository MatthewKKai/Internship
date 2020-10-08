import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Normalizer
from prepocessing.preprocess import *

class encoder():
    def __init__(self, file_path):
        self.file_path = file_path
        self.ohEncdoer = OneHotEncoder()
        self.labelEncoder = LabelEncoder()
        self.TfIDVectorizer = TfidfVectorizer()
        self.CountVectorizer = CountVectorizer()

    def get_dump_data(self):
        return prepprocess(self.file_path).dump_dic2csv()

    def VCEncdoe(self):
        data = self.get_dump_data()
        for column in data.columns:
            tempVC = pd.DataFrame(data[column].value_counts())
            indexName = list(tempVC)
            for index, name in enumerate(indexName):
                for i in range(len(data[column])):
                    if data[column][i]==name:
                        data[column][i]=index
        feature = data.drop(["category"], axis=1)
        label = data["category"]
        return feature, label

    def TFiDFEncoder(self):
        pass



