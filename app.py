from flask import Flask, render_template, request, logging, redirect, url_for, Response, g, session
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import csv
import os
import cleaner
import linreg
import pickle


app = Flask(__name__)
app.config["SECRET_KEY"] = "open secret"


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():

    if request.method == 'POST':

        file = request.files['file']
        session['filename'] = file.filename
        print('filename', session['filename'] )
        session['target'] = request.form['target']
        session['target'] = cleaner.fix_target(session['target'])
        data = pd.read_csv(file)
        data = cleaner.clean(data)

        data.to_pickle(session['filename'])

        return render_template(
            'data.html',
            tables=[data.head().to_html()],
            nulls=g.nulls,
            duplicates=g.duplicates,
            outliers=g.outliers,
            memory=g.memory)

@app.route('/getPlotCSV', methods=['GET', 'POST'])
def getPlotCSV():

    data = pd.read_pickle(session['filename'])
    return Response(
        data.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})

@app.route('/linearRegression', methods=['GET','POST'])
def linearRegression():
    
    data = pd.read_pickle(session['filename'])

    os.remove(session['filename'])

    linreg_model = linreg.linreg(data,session['target'])
    print(linreg_model.coef_)
    print(linreg_model.intercept_)
        


    ans = ''
    eq = g.selected_features + ' * ' + str(linreg_model.coef_[0])

    if np.sign(linreg_model.coef_) > 0:
        ans = '+ ' + eq
    else:
        ans = '- ' + eq

    

    return render_template(
            'linearreg.html',
            intercept=linreg_model.intercept_,
            coef_name=g.selected_features,
            coef_num=linreg_model.coef_,
            r_squared=g.r_squared,
            mae=g.mae,
            eq=ans)



if __name__ == '__main__':
    app.run(debug=True)
