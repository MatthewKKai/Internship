#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import re
import csv
import codecs

data_path = r"/Users/loaferzk/LoaferZK/internship/soundwise/data/乳腺2020.01.01到2020.05.30.xlsx"
breastXslData = pd.read_excel(data_path, encoding = "utf-8")

breastData = breastXslData.query('开单科室 == "乳腺肿瘤内科" | 开单科室 == "乳腺外科一" | 开单科室 == "乳腺外科二"')

save_path = r"/Users/loaferzk/LoaferZK/internship/soundwise/data/breastData_need.csv"
breastData.to_csv(save_path,encoding = "utf-8-sig")

target_path = r"/Users/loaferzk/LoaferZK/internship/soundwise/data/result.csv"
file_path = r"/Users/loaferzk/LoaferZK/internship/soundwise/data/breastData/breastData_need.csv"
class preprocess(object):
    def __init__(self, file_path):
        # regex for data
        self.file_path = file_path
        self.pattern_location = re.compile(r'((?:于)[\u4e00-\u9fa5]*(?:乳).*m(?:团块))')  # 乳腺团块位置regex
        self.pattern_massSize = re.compile(r'\d*\.*\d*×\d*\.*\d*×\d*\.*\d*mm')  # 乳腺团块大小
        self.pattern_shape = re.compile(r'呈不规则形|呈椭圆形|呈类圆形')  # 团块形状
        self.pattern_blood = re.compile(r'CDFI示[\u4e00-\u9fa5]*血流信号')  # 血流状况
        self.pattern_echo = re.compile(r'内部呈[\u4e00-\u9fa5][\u4e00-\u9fa5]?回声')  # 回声(不必要)
        self.pattern_rearEcho = re.compile(r'后方伴?回?声[\u4e00-\u9fa5]*')  # 后方回声
        self.pattern_boundary = re.compile(r'边缘界限[\u4e00-\u9fa5]*')  # 结节边缘界限
        self.pattern_calcification = re.compile(r'[\u4e00-\u9fa5]*钙化灶[\u4e00-\u9fa5]*')  # 钙化灶
        self.pattern_category = re.compile(r'拟[^\u4e00-\u9fa5]*类')  # 获取拟诊断类别

    def get_file(self):
        fileData = pd.read_excel(self.file_path, encoding="utf-8-sig")
        return fileData

    def dump_dic2csv(self, dump_path = r"../data.csv"):
        headers = ['num', 'location', 'massSize', 'vh_ratio', 'shape', 'blood', 'echo', 'rearEcho', 'boundary',
                   'calcification', 'category']
        dump_data = self.rexExtraction()
        with codecs.open(dump_path, "r", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, headers)
            for item in dump_data:
                writer.writerow(item)
        return pd.read_csv(dump_path, encoding="gbk")

    def rexExtraction(self):
        # headers = ['num', 'location', 'massSize', 'vh_ratio', 'shape', 'blood', 'echo', 'rearEcho', 'boundary',
        #            'calcification', 'category']
        # print(len(fileData["超声所见"]))
        # with open(target_path, "w", newline="") as f:
        #     f_csv = csv.DictWriter(f, headers)
        #     f_csv.writeheader()
        fileData = self.get_file()
        dump_data = []
        for i in range(len(fileData["超声所见"])):
            location = []
            massSize = []
            vh_ratio = []
            shape = []
            blood = []
            echo = []
            rearEcho = []
            boundary = []
            calcification = []
            try:
                category = self.pattern_category.findall(fileData["超声诊断"][i].replace("\xa0","_").replace("－","-"))
            except Exception as e:
                print(e)
                continue
            info_dict = {}
            reportList = fileData["超声所见"][i].strip(" ").split("。")
            for sentence in reportList:
                # 乳腺位置匹配
                temp_location = self.pattern_location.search(sentence)
                if temp_location is None:
                    pass
                else:
                    if "左" in temp_location.group():
                        location.append("左部")
        #                 info_dict["location"] = "左部"
                    elif "右" in temp_location.group():
                        location.append("右部")
        #                 info_dict["location"] = "右部"
                    else:
                        pass
        #             info_dict["location"] = temp_location.group()
                # 乳腺位置中团块的大小匹配
                temp_massSize = self.pattern_massSize.search(sentence)
                if temp_massSize is None:
                    pass
                else:
                    massSize.append(temp_massSize.group())
        #             info_dict["massSize"] = temp_massSize.group()
                    num_list = temp_massSize.group().split("×")
                    try:
                        vh_ratio.append(float(num_list[1])/float(num_list[0]))
                    except Exception as e:
                        print(num_list)
        #             info_dict["vh_ratio"] = int(num_list[1])/int(num_list[0])
        #             info_dict["massSize"] = pattern_massSize 在信息获取完毕后再添加至info_dict
                # 乳腺形状描述提取
                temp_shape = self.pattern_shape.search(sentence)
                if temp_shape is None:
                    pass
                else:
                    shape.append(temp_shape.group())
        #             info_dict["shape"] = temp_shape.group()
                # 血流情况文本匹配
                temp_blood = self.pattern_blood.search(sentence)
                if temp_blood is None:
                    pass
                else:
                    blood.append(temp_blood.group())
        #             info_dict["blood"] = temp_blood.group()
                # 回声情况匹配（回声不重要，文本中有多处描述
                temp_echo = self.pattern_echo.search(sentence)
                if temp_echo is None:
                    pass
                else:
                    echo.append(temp_echo.group())
        #             info_dict["echo"] = temp_echo.group()
                # 后方回声情况匹配
                temp_rearEcho = self.pattern_rearEcho.search(sentence)
                if temp_rearEcho is None:
                    pass
                else:
                    rearEcho.append(temp_rearEcho.group())
        #             info_dict["rearEcho"] = temp_rearEcho.group()
                temp_boundary = self.pattern_boundary.search(sentence)
                if temp_boundary is None:
                    pass
                else:
                    boundary.append(temp_boundary.group())
                temp_calcification = self.pattern_calcification.search(sentence)
                if temp_calcification is None:
                    pass
                else:
                    calcification.append(temp_calcification.group())
            num = len(location) # 团块数量
            if num > 1:
                info_dict["num"] = "多发"
            elif num == 1:
                info_dict["num"] = "单发"
            else:
                pass
            for i in range(num):
                try:
                    info_dict["location"] = location[i]
                except Exception as e:
                    info_dict["location"] = "None"
                try:
                    info_dict["massSize"] = massSize[i]
                except Exception as e:
                    info_dict["massSize"] = "None"
                try:
                    info_dict["vh_ratio"] = vh_ratio[i]
                except Exception as e:
                    info_dict["vh_ratio"] = "0"
                try:
                    info_dict["shape"] = shape[i]
                except Exception as e:
                    info_dict["shape"] = "None"
                try:
                    info_dict["blood"] = blood[i]
                except Exception as e:
                    info_dict["blood"] = "None"
                try:
                    info_dict["echo"] = echo[i]
                except Exception as e:
                    info_dict["echo"] = "None"
                try:
                    info_dict["rearEcho"] = rearEcho[i]
                except Exception as e:
                    info_dict["rearEcho"] = "None"
                try:
                    info_dict["boundary"] = boundary[i]
                except Exception as e:
                    info_dict["boundary"] = "None"
                try:
                    info_dict["calcification"] = calcification[i]
                except Exception as e:
                    info_dict["calcification"] = "None"
                try:
                    info_dict["category"] = category[i]
                except Exception as e:
                    info_dict["category"] = "None"
                # with codecs.open(target_path, "a", "gbk") as f:
                #     print(info_dict)
                #     f.write(codecs.BOM_UTF8)
                #     writer = csv.DictWriter(f, headers)
                #     data = list(info_dict.values())
                #     writer.writerow(info_dict)
                dump_data.append(info_dict)
                continue
        return dump_data