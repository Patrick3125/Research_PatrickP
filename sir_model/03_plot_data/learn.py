import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split

# Part 1: Generating the dataset
def diff_equations(y, t, b, k):
    s, i, r = y
    ds_dt = -b*s*i
    di_dt = b*s*i - k*i
    dr_dt = k*i
    return np.array([ds_dt, di_dt, dr_dt])

def runge_kutta(func, y0, t, args=()):
    dt = t[1] - t[0]
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        k1 = dt * np.array(func(y[i], t[i], *args))
        k2 = dt * np.array(func(y[i] + k1 / 2., t[i] + dt / 2., *args))
        k3 = dt * np.array(func(y[i] + k2 / 2., t[i] + dt / 2., *args))
        k4 = dt * np.array(func(y[i] + k3, t[i] + dt, *args))
        y[i + 1] = y[i] + 1 / 6. * (k1 + 2 * k2 + 2 * k3 + k4)
    return y

N = 1000  # number of data samples to generate
t = np.arange(0, 45, 0.005)

b_values = np.random.uniform(0, 1, N)
k_values = np.random.uniform(0, 1, N)

X = np.zeros((N, 2))  # features (max I and max R)
y = np.zeros((N, 2))  # targets (b and k)

for i in range(N):
    y0 = np.array([1, 0.0008, 0])
    sir = runge_kutta(diff_equations, y0, t, args=(b_values[i], k_values[i]))
    X[i, 0] = np.max(sir[:, 1])  # max I(t)
    X[i, 1] = np.max(sir[:, 2])  # max R(t)
    y[i, 0] = b_values[i]
    y[i, 1] = k_values[i]

# Part 2: Machine learning model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

# Test the model
print("Model score: ", model.score(X_test, y_test))

# Predict for a new infection rate and recovery rate
new_X = np.array([[0.05, 0.02]])  # replace with your values
predicted_b, predicted_k = model.predict(new_X)[0]
print(f"Predicted b: {predicted_b}, Predicted k: {predicted_k}")
