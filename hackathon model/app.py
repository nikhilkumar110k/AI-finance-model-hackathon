import yfinance as yf 
from flask import request,render_template, jsonify, Flask
import tensorflow as tf
from tensorflow.keras.layers import Input, LSTM, GRU, SimpleRNN, Dense, GlobalMaxPool1D, Dropout
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.optimizers import Adam,SGD
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
from sklearn.preprocessing import StandardScaler
import numpy as np
import io
import base64

from flask_cors import CORS

app= Flask(__name__, template_folder='templates',static_url_path='/static')
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stock_data',methods=['POST'])

def get_stock_data():
    ticker= request.json['ticker']
    company=ticker
    start = dt.datetime(2018, 1, 1)
    end = dt.datetime.now()
    df = yf.download(company, start, end)
    df['prevclose'] = df['Close'].shift(1)
    df['Return'] = (df['Close'] - df['prevclose']) / df['prevclose']
    df['Return'].hist()
    input_data = df[['Open', 'High', 'Low', 'Close', 'Volume']].values
    targets = df['Return'].values

    T = 10
    D = input_data.shape[1]
    N = len(input_data) - T

    Ntrain = len(input_data) * 2 // 3
    scaler = StandardScaler()
    scaler.fit(input_data[: Ntrain + T])
    input_data = scaler.transform(input_data)

    X_test = np.zeros((N - Ntrain, T, D))
    Y_test = np.zeros((N - Ntrain))

    for u in range(N - Ntrain):
      t = u + Ntrain
      X_test[u, :, :] = input_data[t:t + T]
      Y_test[u] = (targets[t + T] > 0)

    model = load_model('../model.h5') 
    p_pred = model.predict(X_test)

    binary_predictions = (p_pred > 0.5).astype(int)
    last_prediction = binary_predictions[-1][0]
    if last_prediction > 0.5:
       print("The graph is subjected to rise.")
       output= "The graph is subjected to rise."
    if last_prediction == 0.5:
       print("The graph is subjected to stay constaint.")
       output="The graph is subjected to stay constaint."
    if last_prediction < 0.5:
       print("The graph is subjected to fall")
       output= "The graph is subjected to fall"


    fig, ax = plt.subplots()
    ax.plot(df.index, df['Return'], label='Returns')
    ax.legend()

    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.read()).decode('utf8')
    return jsonify({'currentPrice': df.iloc[:-1]['Close'].tolist()[-1],
                    'Openprice': df.iloc[-1]['Open'],
                    'output': output,
                    'plot': img_data})
    

if __name__ == '__main__':
    app.run(debug=True)