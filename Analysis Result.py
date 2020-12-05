#!/user/bin/env python
#coding=utf-8

import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

with open('./2019.csv', encoding='utf-8') as f:
    # data = np.loadtxt(f, str, delimiter=',')    # if there is no str,the number will be read by default；
    # data = np.loadtxt(f, str, delimiter=',', skiprows=1)    # skip the first line
    data = np.loadtxt(f, str, delimiter=',', skiprows=1, usecols=(1, 3, 4, 5))   # read specified column, tag, datetime, value, company_name
# print(data)
data = data[data[:, 3].argsort()]
# print(data[:, 0])
# mask = np.where(data[:, 0] == 'SalesRevenueNet')    # find an item
# print(mask)
# print(data[mask])

def get_kpi_name_and_company_name(data):
    kpi_name_list = []
    company_name_list = []
    for item in data:
        if item[0] not in kpi_name_list:
            kpi_name_list.append(item[0])
        if item[3] not in company_name_list:
            company_name_list.append(item[3])
    kpi_name_list.sort()
    company_name_list.sort()
    return kpi_name_list, company_name_list

def change_kpi_name(data, kpi_name, kpi_name1):
    error1_mask = np.where(data[:, 0] == kpi_name1)
    # print(data[error1_mask[0]])
    for item in error1_mask[0]:
        data[item][0] = kpi_name
    # print(data[error1_mask[0]])
    return data

kpi_name_list, company_name_list = get_kpi_name_and_company_name(data)
# print(kpi_name_list)
# print(company_name_list)

# data = change_kpi_name(data, 'CostOfGoodsSold', 'CostOfGoodsAndServicesSold')
# data = change_kpi_name(data, 'SalesRevenueNet', 'SalesRevenueGoodsNet')

# kpi_name_list, company_name_list = get_kpi_name_and_company_name(data)
# print(kpi_name_list)
# print(company_name_list)


useful_list = []
useful_data = []
for kpi_name in kpi_name_list:
    for company_name in company_name_list:
        mask1 = np.where(data[:, 0] == kpi_name)
        # print(mask1[0])
        mask2 = np.where(data[:, 3] == company_name)
        # print(mask2[0])
        inter_index = np.intersect1d(mask1, mask2)
        if len(inter_index) >= 8:
            tmp_list = []
            for index in inter_index:
                """ tag, ddate, value, name is not enough
                # if data[index].tolist() in tmp_list:
                #     pass
                # else:
                #     tmp_list.append(data[index].tolist())
                """
                
                """ddate is not align with version
                # ddate = data[index].tolist()[1][:4]
                # version = data[index].tolist()[4][-4:]
                # if ddate == version:
                #     tmp_list.append(data[index].tolist())
                """
                
                """ rough process data """
                flag = False
                ddate = data[index][1]
                for item in tmp_list:
                    if ddate in item:
                        flag = True
                if not flag:
                    tmp_list.append(data[index].tolist())
            if len(tmp_list) >= 8:
                useful_data.append(tmp_list)
                useful_list.append([kpi_name, company_name])
for item in useful_list:
    print(item)
# for item in useful_data:
#     print(len(item), item)
# print(useful_list)
        
# print(data[inter_index])
