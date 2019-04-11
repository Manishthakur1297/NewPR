from flask import Flask, jsonify, request;
import pickle;
import os
import re
import numpy as np
import pandas as pd
import hashlib
from collections import OrderedDict
import itertools as it
from file_titles import titles

app = Flask(__name__)

@app.route("/", methods=['GET'])

def first():
    return jsonify({"Welcome": "Here"})

@app.route("/readFile/", methods = ['POST'])
def ReadFile():
    global resList
    text = request.data
    ff = text.decode('utf-8').split(",")
    file_name = ''.join(ff[0][4:]).replace("\"",'').strip()
    file_format = ff[1].replace("\\n",'').replace("\"",'').strip()
    file_text = ''.join(ff[2:]).replace("\\r","")
    file_text = str(file_text.replace("\\n","\n").replace("\"",'').strip())
    file_text1 = file_text.strip().split("\n")
    del file_text1[len(file_text1)-1]

    format = titles[file_format]['log_format']
    rex =  titles[file_format]['regex'][0]

    mainList = []
    for line in file_text1:
        l = re.findall(rex, line)
        size = len(format)
        size1 = len(l)
        if(size1<size):
            pass
        else:
            l[size-1] = ' '.join(l[size-1:])
            del l[size:]
        
        d = OrderedDict()
        for k ,v in it.zip_longest(format,l):
            d[k] = v
        mainList.append(d)
        resList = mainList

    #     df = pd.DataFrame(mainList, columns=format)
    #     df.to_csv(file_name+"_structured.csv", sep=',', encoding='utf-8', index=False)
   
    return jsonify(mainList,format)


@app.route("/search", methods = ['GET'])
def SearchFile():
    text = request.args
    print (text) # For debugging    
    key = text['key1']
    col = text['key2']

    print()
    df  = pd.DataFrame(resList)
    #print(df.head(5))
    data = df.loc[df[col] == key]
    #print(dict(data))
    return jsonify(data.to_dict('records'))


@app.route("/sort", methods = ['GET'])
def SortFile():
    text = request.args
    print (text) # For debugging    
    col = text['key1']

    df  = pd.DataFrame(resList)
    data = df.sort_values(by=[col])
    #print(dict(data))
    return jsonify(data.to_dict('records')) 


if __name__=='__main__':
    app.run(debug=True)
