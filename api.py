from flask import Flask,render_template,request
import pandas as pd
from tqdm import tqdm
import numpy as np
from nltk.sentiment import SentimentIntensityAnalyzer
import pickle
import math
app=Flask(__name__)


wine_quotes=["Drinking good wine with good food in good company is one of life’s most civilized pleasures.","The best way to learn about wine is by drinking.","Life is too short to drink bad wine.","With wine and hope, anything is possible","Wine and friends are a great blend."]
def add_column(X):
    data={}
    sia=SentimentIntensityAnalyzer()
    for i,row in tqdm(enumerate(X.iterrows()),total=len(X)):
        id=row[0]
        description=row[1]['remainder__description']
        data[id]=sia.polarity_scores(description)
    new_data=pd.DataFrame(data).T
    X.drop(['remainder__description'],axis=1,inplace=True)
    X=pd.merge(X,new_data,left_index=True,right_index=True)  
    X=X[['Encoding__country','Encoding__province','Encoding__variety','remainder__price','neg','neu','pos','compound']]
    return X

regressor=pickle.load(open('pipe.pkl','rb'))
all_country,all_province,all_variety=regressor.named_steps['Encoder'].named_transformers_['Encoding'].categories_

@app.route("/results",methods=['POST'])
def results():
    cou=request.form['country']
    prov=request.form['province']
    price=request.form['price']
    var=request.form['wine-type']
    description=request.form['description']
    x=pd.DataFrame({"country":cou,"price":float(price),"province":prov,"variety":var,"description":description},index=[0])
    res=math.ceil(regressor.predict(x)[0])
    return render_template("new.html",points=res,country=cou,province=prov,quote=np.random.choice(wine_quotes,size=1)[0],variety=var)

@app.route('/')
def reviewer():
    return render_template("predict.html",countries=all_country,provinces=all_province,varities=all_variety)
   

if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000)