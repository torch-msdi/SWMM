"""
!/usr/bin/python3.7
-*- coding: utf-8 -*-
@Time    : 2020/10/27
@Author  : MS.torch
@Email   : torch4232@gmail.com
"""
from section_feature import SectionFeature


def deal(sections, excel_data, log=None):
    if log is None:
        log = []
    result_dict = {'时间': [], 'ID': [], '流量': [], '最大水深': [],
                   '平均水深': [], '水面宽度': [], '湿周': [],
                   '过水面积': [], '平均流速': []}
    rec_dict = {}
    for row in range(len(excel_data['ID'])):
        section_name = str(excel_data['ID'][row])
        water_depth = excel_data['水深'][row]
        time = excel_data['时间'][row]
        discharge = excel_data['流量'][row]
        try:
            key_name = section_name + '-' + str(water_depth)
            if rec_dict[key_name]:
                for i in rec_dict[key_name]:
                    result_dict[i].append(rec_dict[key_name][i])
            result_dict['ID'].append(section_name)
            result_dict['最大水深'].append(water_depth)
            result_dict['时间'].append(time)
            result_dict['流量'].append(discharge)
            try:
                result_dict['平均流速'].append(result_dict['流量'][-1] / result_dict['过水面积'][-1])
            except ZeroDivisionError:
                result_dict['平均流速'].append(0)
            rec_dict = {}
        except KeyError:
            try:
                section_data = sections.sections[section_name]
                section_feature = SectionFeature(data=section_data, depth=water_depth)
                rec_dict['过水面积'] = section_feature.section_area()
                rec_dict['平均水深'] = section_feature.avg_water_depth()
                rec_dict['水面宽度'] = section_feature.water_width()
                rec_dict['湿周'] = section_feature.wet_circle()
                rec_dict['ID'] = section_name
                rec_dict['最大水深'] = water_depth
                rec_dict['时间'] = time
                rec_dict['流量'] = discharge
                try:
                    rec_dict['平均流速'] = rec_dict['流量'] / rec_dict['过水面积']
                except ZeroDivisionError:
                    rec_dict['平均流速'] = 0
                for i in rec_dict:
                    result_dict[i].append(rec_dict[i])
            except KeyError:
                word = '请检查INP文件中是否存在{}断面'.format(section_name)
                if word not in log:
                    log.append(word)
    return result_dict, log
