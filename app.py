from flask import Flask, render_template, request, logging, redirect, url_for, Response, g, session
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import csv
import os
import cleaner
import linreg
import pickle
import bayesian


app = Flask(__name__)

app.config["SECRET_KEY"] = "open secret"




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')



# Explatory Data Analysis
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

# Returns cleaned csv
@app.route('/getPlotCSV', methods=['GET', 'POST'])
def getPlotCSV():
    data = pd.read_pickle(session['filename'])
    os.remove(session['filename'])
    return Response(
        data.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})



# 
@app.route('/linearRegression', methods=['GET','POST'])
def linearRegression():
    
    if request.method == 'POST': 
        # if user presses submit after uploading dataset and target
        if 'file' in request.files and 'target' in request.form:
            file = request.files['file']
            session['filename'] = file.filename
            data = pd.read_csv(file)
            data = cleaner.clean(data)
            session['target'] = request.form['target']
            session['target'] = cleaner.fix_target(session['target'])

        # if user only needs to uplaod target and presses submit
        elif 'get_target' in request.form:
    
            session['target'] = request.form['get_target']
            session['target'] = cleaner.fix_target(session['target'])
            data = pd.read_pickle(session['filename'])
        
        # perform linear regression
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

    # if user needs to uplaod csv and target
    if request.method == 'GET':
        if not os.path.isfile(session['filename']): 
            return render_template('linearreg.html')
        else:
            # if user only needs to upload target
            return render_template('linearreg.html', get_target=True)

@app.route('/logistic_regression', methods=['GET', 'POST'])
def logistic_regression():

    if request.method == 'POST': 
    # if user presses submit after uploading dataset and target
        if 'file' in request.files and 'target' in request.form:
            file = request.files['file']
            session['filename'] = file.filename
            data = pd.read_csv(file)
            data = cleaner.clean(data)
            session['target'] = request.form['target']
            session['target'] = cleaner.fix_target(session['target'])

        # if user only needs to uplaod target and presses submit
        elif 'get_target' in request.form:

            session['target'] = request.form['get_target']
            session['target'] = cleaner.fix_target(session['target'])
            data = pd.read_pickle(session['filename'])
        
        # perform linear regression
        logreg_model = logreg.logreg(data,session['target'])
        return render_template('linearreg.html')


    # if user needs to uplaod csv and target
    if request.method == 'GET':
        if not os.path.isfile(session['filename']): 
            return render_template('linearreg.html')
        else:
            # if user only needs to upload target
            return render_template('linearreg.html', get_target=True)


@app.route('/bayesian_calculator', methods=['GET', 'POST'])
def bayesian_calculator():
    if request.method == 'GET':
        return render_template('bayes.html')



@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        x = request.args.get("a")
        y = request.args.get("bga")
        z = request.args.get("bgna")
        bayesian.calculate(x,y,z)
        return render_template('bayes.html')
    if request.method == 'POST':
        print("tester posr")
        # bayesian.calculate(request.args.get("a"))
        return render_template('bayes.html')


if __name__ == '__main__':
    app.run(debug=True)