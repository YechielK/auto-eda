from flask import Flask, render_template, request, logging, redirect, url_for, Response, g
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as numpy
import csv
import os
import cleaner



app = Flask(__name__)


x = 'this is x'

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET', 'POST'])
def data():
    global x
    if request.method == 'POST':

        file = request.files['file']
        data = pd.read_csv(file)
        data = cleaner.clean(data)
        x = data
        # return render_template('data.html', data=data)
        return render_template(
            'data.html',
            data=data,
            nulls=g.nulls,
            duplicates=g.duplicates,
            outliers=g.outliers,
            memory=g.memory)

@app.route("/getPlotCSV", methods=['GET', 'POST'])
def getPlotCSV():
    global x

    return Response(
        x.to_csv(index=False),
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=myplot.csv"})


if __name__ == '__main__':
    app.run(debug=True)