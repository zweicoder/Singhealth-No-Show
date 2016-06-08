# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 16:56:27 2016

@author: zhouyunke
"""
import xgboost as xgb
import numpy as np
from parser import Parser

class Oracle:
    def __init__(self, input_file):
        self.bst = xgb.Booster(model_file='0001.model')
        self.parser = Parser(input_file)

    def predict(self):
        inp = np.array(self.parser.parse())
        xg_test = xgb.DMatrix(inp)
        return self.bst.predict(xg_test)
