"""
Usage: Coalitional Game, Approximating the contribution of the i-th feature’s value
Python version: 3.9.X
Author: rauls19
"""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import datetime


MODEL_AVAILABLE: list = [type(LinearRegression())]

class miniCoalitionalGame:

    def __init__(self) -> None:
        self.__fi_i_contributions:list = []


    def check_model_availability(self, model):
        if type(model) in MODEL_AVAILABLE:
                return True
        return False


    def __get_pre_i_o(self, O, target):
        idx = np.where(O == target)[0][0]
        return O[:idx+1]
        

    def __extractValue(self, val):
        value = val
        if isinstance(value, np.ndarray):
            value = self.__extractValue(value[0])
        return value


    def __calculusContribution(self, target, model, data_x, data_y, m):
        fi_i = 0
        counter_No_Preivalues = 0
        for j in range(1, (m+1)):
            try:
                O = np.random.permutation(data_x.columns)
                y = data_x.sample()
                pre_i_O = self.__get_pre_i_o(O, target)
                if pre_i_O[0] == target:
                    counter_No_Preivalues = counter_No_Preivalues + 1
                    continue
                # INI SUBSET - PREPARE DATA WITH SELECTED COLUMNS
                x = data_x[pre_i_O]
                y = y[pre_i_O]
                # END
                model.fit(x, data_y)
                v1 = model.predict(y)
                pre_i_O = np.delete(pre_i_O, pre_i_O.size-1)
                # INI SUBSET - PREPARE DATA WITHOUT THE TARGET
                x = data_x[pre_i_O]
                y = y[pre_i_O]
                # END
                model.fit(x, data_y)
                v2 = model.predict(y)
                fi_i = fi_i + (v1 - v2)
            except Exception as e:
                logf = open('Error.log', 'a')
                er = {'exception:': e, 'O': O, 'Pre^i(O)': pre_i_O, 'fi_i': fi_i, 'target': target, 'x_shape' : x.shape, 'y_shape': y.shape} 
                logf.write('\n ###################################'+datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S')+'################################### \n')
                logf.write(str(er))
                logf.close()
                raise('\n Unexpected error, please check the file called Error.log for further information')
        if (m - counter_No_Preivalues) == 0:
            final_fi_i = 0
        else:
            final_fi_i = fi_i / (m - counter_No_Preivalues)
        self.__fi_i_contributions.append({target: self.__extractValue(final_fi_i)})


    def explainerContribution(self, model, data_x: pd.DataFrame, data_y: pd.DataFrame, m = 50, spec_feat = []):
        if not self.check_model_availability(model):
            raise Exception('Model not supported')
        if spec_feat == []:
            spec_feat = data_x.columns
        for player in spec_feat:
            self.__calculusContribution(player, model, data_x, data_y, m)
        return self.__fi_i_contributions
