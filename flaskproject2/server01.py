import os
import io
import matplotlib as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from sklearn import linear_model
import statsmodels.api as sm
from flask import Flask, render_template, request, Response, url_for, session
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename
from flask_login import *
import uuid
from datetime import datetime,date
# from distutils import log
import analysiss as an
import dbchanger as dbc

 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = 'secretkey'
TBAR = DebugToolbarExtension(app)


@app.route('/home')
def homepage():
	return render_template('home.html')

@app.route('/uploader', methods = ['GET','POST'])
def de():
	if request.method == 'POST':
		uname = request.form['uname']
		phno = request.form['phno']
		csvfile = request.files['file']
		csvfile.save(secure_filename(csvfile.filename))
		csvfile.save(os.path.join(app.config['UPLOAD_FOLDER'],csvfile.filename))
		session['csv_filename'] =  csvfile.filename
		csvfilename = csvfile.filename
		predictval = an.analyzefile(csvfilename)
		# sessionid = flask_login.session['_id']
		sessionid = str(uuid.uuid4())
		logid = "user"+sessionid[0:4]
		userid = sessionid[0:6]
		currenttime = datetime.now().strftime("%H:%M:%S")
		# print(userid,uname,phno,logid,sessionid,date.today().strftime("%Y-%m-%d"),currenttime,predictval)
		dbc.insertdata(userid,uname,phno,logid,sessionid,date.today().strftime("%Y-%m-%d"),currenttime,predictval)
		return "<LINK TYPE='text/css' REL='stylesheet' HREF='static\style.css'> \
			<DIV CLASS='container'><BR><BR><CENTER><H2>Upload successful!</H2> \
			User name: "+uname+"<BR><BR> Phone number: "+phno+"<BR><BR> Filename: "+csvfile.filename+"<BR><BR> \
			Predicted value: "+str(predictval)+"<BR><BR> \
			Userid: "+userid+"<BR>LogID: "+logid+"<BR>SessionID: "+sessionid+"<BR>Date: "+ \
			date.today().strftime("%Y-%M-%D")+"<BR>Time: "+currenttime+"<BR><BR> \
			<A HREF="+url_for('plot_png')+"><INPUT TYPE='BUTTON' VALUE='GRAPH' CLASS='sbutton'></A><BR> \
			<A HREF="+url_for('summary')+"><INPUT TYPE='BUTTON' VALUE='SUMMARY' CLASS='sbutton'></A></CENTER></DIV>"

@app.route('/print-plot', methods = ['GET','POST'])
def plot_png():
	plt.rcParams["figure.figsize"] = [8.50, 4.50]
	plt.rcParams["figure.autolayout"] = True
	csv_file = session.get('csv_filename', None)
	df = pd.read_csv(csv_file)
	X = df[['use [kW]','gen [kW]']]
	y = df['time']
	regr = linear_model.LinearRegression()
	regr.fit(X, y)
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	xs = X
	ys = y
	axis.plot(xs, ys, color = "green")
	axis.set_xlabel('Use & Gen')
	axis.set_ylabel('Time')
	output = io.BytesIO()
	FigureCanvas(fig).print_png(output)
	return Response(output.getvalue(), mimetype='image/png')


@app.route('/print-summary', methods = ['GET','POST'])
def summary():
	csv_file = session.get('csv_filename', None)
	df = pd.read_csv(csv_file)
	x = df[['use [kW]','gen [kW]']]
	y = df['time']
	# using sklearn
	reger = linear_model.LinearRegression()
	reger.fit(x,y)
	# using statsmodels
	x = sm.add_constant(x)
	model = sm.OLS(y,x).fit()
	predictions = model.predict(x)
	summary = model.summary()
	return "<LINK TYPE='text/css' REL='stylesheet' HREF='static\style.css'><DIV CLASS='container'>" \
			+str(summary.tables[0])+str(summary.tables[1])+ \
			"<BR><H2>Intercept: "+str(reger.intercept_)+"<BR>Regression coefficient: "+str(reger.coef_)+ \
				"<H4>Regression coefficient is the amount of relation among two variables.</H4> \
					<BR>Predictions: "+str(predictions)+"</H2></DIV>"

# app.run(debug=True)
app.run(host="0.0.0.0")
