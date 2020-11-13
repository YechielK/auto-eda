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
    if request.method == 'GET':

        return render_template('index.html')

    return 'diddnt owrk0'


@app.route('/eda', methods=['GET', 'POST'])
def eda():
    if request.method == 'GET':
        return render_template('eda.html')

    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']

        session['filename'] = file.filename

        data = pd.read_csv(file)
        data = cleaner.clean(data)
        data.to_pickle(session['filename'])
        return render_template('eda.html',
            tables=[data.head().to_html()],
            nulls=g.nulls,
            duplicates=g.duplicates,
            outliers=g.outliers,
            memory=g.memory)

@app.route('/getPlotCSV', methods=['GET', 'POST'])
def getPlotCSV():

    data = pd.read_pickle(session['filename'])
    os.remove(session['filename'])
    return Response(
        data.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})

@app.route('/linearRegression', methods=['GET','POST'])
def linearRegression():
    
    if request.method == 'POST' and 'file' in request.files and 'target' in request.form:
        file = request.files['file']

        session['filename'] = file.filename

        data = pd.read_csv(file)


        data = cleaner.clean(data)
        session['target'] = request.form['target']
        session['target'] = cleaner.fix_target(session['target'])

        linreg_model = linreg.linreg(data,session['target'])
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

    if request.method == 'POST' and 'get_target' in request.form:

        session['target'] = request.form['get_target']
        session['target'] = cleaner.fix_target(session['target'])
        data = pd.read_pickle(session['filename'])
        linreg_model = linreg.linreg(data,session['target'])

            
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

    if request.method == 'GET':
        if not os.path.isfile(session['filename']): 
            return render_template('linearreg.html')
        else:
            print('from get')
            return render_template('linearreg.html', get_target=True)

       


if __name__ == '__main__':
    app.run(debug=True)
