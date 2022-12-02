from pkgutil import ModuleInfo
import pandas
from sklearn import linear_model

def analyzefile(file):
    df = pandas.read_csv(file)
    X = df[['use [kW]','gen [kW]']]
    y = df['time']
    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    # predicting the dishwasher time where use is 0.934333333 and gen is 0.003466667
    predictedtime = regr.predict([[0.934333333, 0.003466667]])
    return predictedtime[0]
