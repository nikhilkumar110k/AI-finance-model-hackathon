import yfinance as yf
from sklearn.preprocessing import StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import datetime as dt
from tensorflow.keras.models import load_model

company = 'AAPL'
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

Ntrain = len(input_data) * 2//3
scaler = StandardScaler()
scaler.fit(input_data[: Ntrain + T])
input_data = scaler.transform(input_data)

X_test = np.zeros((N - Ntrain, T, D))
Y_test = np.zeros((N - Ntrain))

for u in range(N - Ntrain):
    t = u + Ntrain
    X_test[u, :, :] = input_data[t:t + T]
    Y_test[u] = (targets[t + T] > 0)

model = load_model('model.h5')
p_pred = model.predict(X_test)

binary_predictions = (p_pred > 0.5).astype(int)
last_prediction = binary_predictions[-1][0]
if last_prediction > 0.5:
    print("The graph is subjected to rise.")
if last_prediction == 0.5:
    print("The graph is subjected to stay constaint.")
if last_prediction < 0.5:
    print("The graph is subjected to fall")


fig, ax = plt.subplots()
ax.plot(df.index[T + Ntrain:], binary_predictions, label='Predictions')
ax.legend()

img_buf = io.BytesIO()
plt.savefig(img_buf, format='png')
img_buf.seek(0)
img_data = base64.b64encode(img_buf.read()).decode('utf8')

plt.show()