import json
import os
import re

def processJson(filePath,targetPathroot):
    with open(filePath) as f:
         data = json.load(f)
    pattern_x = re.compile(r"[^x]+")
    pattern_y = re.compile(r"[^y]+")
    length = len(data["outputs"]["object"])
    for i in range(length):
        x = []
        y = []
        name = data["outputs"]["object"][i]["name"]
        temp_dic = data["outputs"]["object"][i]["cubic_bezier"]
        for item0,value0 in temp_dic.items():
            for item1,value1 in temp_dic.items():
                if pattern_x.search(item0).group(0)==pattern_y.search(item1).group(0):
                    x.append(value0)
                    y.append(value1)
        targetPath = os.path.join(targetPathroot,os.path.splitext(os.path.split(filePath)[1])[0]+"_"+str(i)+name+".txt")
        with open(os.path.join(targetPath),"w") as f:
            length_ = len(x)
            for i in range(length_):
                f.write("{},{},{}".format(x[i],y[i],name))
                f.write("\n")