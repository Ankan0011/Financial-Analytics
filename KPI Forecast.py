#!/user/bin/env python
#coding=utf-8

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pmdarima.arima import auto_arima


kpi_name_list = ['GrossProfit', 'NetIncomeLoss']
company_name_list = ['ABBOTT LABORATORIES', 'BRISTOL MYERS SQUIBB CO', 'JOHNSON & JOHNSON']


data_dict = {}
for file_name in os.listdir(os.getcwd()):
    if file_name.endswith('.csv'):
        with open(file_name, encoding='utf-8') as f:
            data = np.loadtxt(f, str, delimiter=',', skiprows=1, usecols=(1, 3, 4, 5))  # read specified column, tag, datetime, value, company_name
    
        for kpi_name in kpi_name_list:
            for company_name in company_name_list:
                if (kpi_name, company_name) not in data_dict.keys():
                    # print(kpi_name, company_name)
                    data_dict[(kpi_name, company_name)] = set()
                
                mask1 = np.where(data[:, 0] == kpi_name)
                mask2 = np.where(data[:, 3] == company_name)
                inter_index = np.intersect1d(mask1, mask2)
                
                tmp_set = data_dict[(kpi_name, company_name)]
                # print(tmp_set)
                for index in inter_index:
                    flag = False
                    ddate = data[index][1]
                    for item in tmp_set:
                        if ddate in item:
                            flag = True
                    if not flag:
                        tmp = tuple(data[index])
                        tmp_set.add(tmp)
                data_dict[(kpi_name, company_name)] = tmp_set

def draw_data(time_axis, v, pred_x=None, pred_y=None):
    xlabels = time_axis #[for plot(x, y)]
    fig, ax = plt.subplots()
    ax.set_xticklabels(xlabels, rotation=90)
    
    
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('{}, {}'.format(key[0], key[1]))
    
    # plt.plot(v, label='data')
    pred_x.insert(0, time_axis[-1])
    pred_y.insert(0, v[-1])
    plt.plot(time_axis, v, label = 'data')
    plt.plot(pred_x, pred_y, label = 'prediction')
    plt.legend()
    plt.grid()
    plt.show()

useful_data_dict = {}
for key, v in data_dict.items():
    v = list(v)
    v.sort()
    v = np.asarray(v)
    time_axis = v[:, 1].tolist()
    v = list(map(int, v[:, 2].tolist()))
    useful_data_dict[key] = v

    # draw_data(time_axis, v)
    # plt.show()

    x_input = list(range(len(time_axis)))
    data = pd.DataFrame({'value': v, 'time_index': x_input})
    data = data.set_index('time_index')
    model = auto_arima(data, trace=True, error_action='ignore', suppress_warnings=True)
    model.fit(data)
    gdp_pre = model.predict(n_periods=3)
    print(gdp_pre)

    draw_data(time_axis, v, ['20200331', '20200630', '20200930'], gdp_pre.tolist())
