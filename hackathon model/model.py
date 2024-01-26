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


company='AAPL'
start= dt.datetime(2011,1,1)
end= dt.datetime.now()
df= yf.download(company , start, end)

df['prevclose']= df['Close'].shift(1)
df['Return']= (df['Close'] - df['prevclose'])/ df['prevclose']
df['Return'].hist()
input_data= df[['Open','High','Low','Close','Volume']].values
targets= df['Return'].values
print(input_data)


T=10
D=input_data.shape[1]
N=len(input_data) - T

Ntrain= len(input_data)* 2//3
scaler= StandardScaler()
scaler.fit(input_data[: Ntrain + T])
input_data= scaler.transform(input_data)


X_train=np.zeros((Ntrain, T, D))
Y_train=np.zeros(Ntrain)
for t in range(Ntrain):
  X_train[t, :, :]= input_data[t: t+T]
  Y_train[t]=(targets[t+T]>0)


X_test= np.zeros((N- Ntrain, T, D))
Y_test= np.zeros((N- Ntrain))
for u in range(N - Ntrain):
  t= u + Ntrain
  X_test[u, : , :] = input_data[t:t+T]
  Y_test[u]= (targets[t+T]>0)



i= Input(shape=(T, D))
x=LSTM(50)(i)
x=Dropout(0.2)
x=LSTM(50)(i)
x=Dropout(0.3)
x=LSTM(50)(i)
x=Dropout(0.4)
x=LSTM(50)(i)
x=Dense(1, activation='sigmoid')(x)
model= Model(i, x)
model.compile(loss='binary_crossentropy',optimizer=Adam(lr=0.0001), metrics='accuracy')




r = model.fit(
    X_train, Y_train,
    batch_size=32,
    epochs=300,
    validation_data=(X_test, Y_test),
)



plt.plot(r.history['loss'],label='loss')
plt.plot(r.history['val_loss'], label='val_loss')
plt.legend()


plt.plot(r.history['accuracy'],label='accuracy')
plt.plot(r.history['val_accuracy'], label='val_accuracy')
plt.legend()
plt.show()






