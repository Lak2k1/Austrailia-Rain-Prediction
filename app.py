from flask import *
app = Flask(__name__) 
import pickle
import numpy as np
with open('rainpredxgb_pkl', 'rb') as f:
    xgb=pickle.load(f)

dic=xgb[2].copy()

xgb[2]['WindGustDir']=list(xgb[2]['WindGustDir'].keys())
xgb[2]['WindDir9am']=list(xgb[2]['WindDir9am'].keys())
xgb[2]['WindDir3pm']=list(xgb[2]['WindDir3pm'].keys())

@app.route('/') 
def home():  
    return render_template("rp.html",pr='',xgb=xgb)

@app.route('/pred',methods=['GET','POST']) 
def pred():
    MinTemp=float([request.form['MinTemp']][0])
    MaxTemp=float([request.form['MaxTemp']][0])
    Rainfall=float([request.form['Rainfall']][0])
    WindGustDir=[request.form['WindGustDir']][0]
    WindGustSpeed=float([request.form['WindGustSpeed']][0])
    WindDir9am=[request.form['WindDir9am']][0]
    WindDir3pm=[request.form['WindDir3pm']][0]
    WindSpeed9am=float([request.form['WindSpeed9am']][0])
    WindSpeed3pm=float([request.form['WindSpeed3pm']][0])
    Humidity9am=float([request.form['Humidity9am']][0])
    Humidity3pm=float([request.form['Humidity3pm']][0])
    Pressure9am=float([request.form['Pressure9am']][0])
    Pressure3pm=float([request.form['Pressure3pm']][0])
    Cloud9am=float([request.form['Cloud9am']][0])
    Cloud3pm=float([request.form['Cloud3pm']][0])
    Temp9am=float([request.form['Temp9am']][0])
    Temp3pm=float([request.form['Temp3pm']][0])
    RainToday=int([request.form['RainToday']][0])
    
    for var in dic['WindGustDir'].keys():
        if var==WindGustDir:
            WindGustDir=dic['WindGustDir'][var]
    
    for var in dic['WindDir9am'].keys():
        if var==WindDir9am:
            WindDir9am=dic['WindDir9am'][var]

    for var in dic['WindDir3pm'].keys():
        if var==WindDir3pm:
            WindDir3pm=dic['WindDir3pm'][var]
    
    l=[MinTemp,MaxTemp,Rainfall,WindGustDir,WindGustSpeed,WindDir9am,WindDir3pm,WindSpeed9am,WindSpeed3pm,Humidity9am,Humidity3pm,Pressure9am,Pressure3pm,Cloud9am,Cloud3pm,Temp9am,Temp3pm,RainToday]
    l=np.array(l)
    p=xgb[0].predict([l])
    if(p==1):
        pr="Yes, it will rain tomorrow."
    else:
        pr="No, it won't rain tomorrow."
    return render_template("rp.html",pr=pr,xgb=xgb)

if __name__ =='__main__':  
    app.run(debug = True)