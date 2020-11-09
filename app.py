from flask import Flask, render_template, request, logging, redirect, url_for, Response, g
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import csv
import os
import cleaner
import linreg



app = Flask(__name__)


x = 'this is x'
y = 'this is y'
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    global x
    global y
    if request.method == 'POST':

        file = request.files['file']
        y = request.form['t']
        y = cleaner.fix_target(y)
        data = pd.read_csv(file)
        data = cleaner.clean(data)
        x = data
        
        # return render_template('data.html', data=data)
        return render_template(
            'data.html',
            tables=[data.head().to_html()],
            # titles=data.columns.values,
            nulls=g.nulls,
            duplicates=g.duplicates,
            outliers=g.outliers,
            memory=g.memory)

@app.route('/getPlotCSV', methods=['GET', 'POST'])
def getPlotCSV():
    global x

    return Response(
        x.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})

@app.route('/linearRegression', methods=['GET','POST'])
def linearRegression():
    global x
    global y



    linreg_model = linreg.linreg(x,y)
    print(linreg_model.coef_)
    print(linreg_model.intercept_)


    ans = ''
    if np.sign(linreg_model.coef_) > 0:
        ans = '+ ' + g.selected_features + ' * ' + str(linreg_model.coef_[0])
    else:
        ans = '- ' + g.selected_features + ' * ' + str(linreg_model.coef_[0])



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
