import pickle
import pandas as pd

model = pickle.load(open("notebook/crop_model.pkl", "rb"))

N = float(input("Enter Nitrogen: "))
P = float(input("Enter Phosphorus: "))
K = float(input("Enter Potassium: "))
temperature = float(input("Enter Temperature: "))
humidity = float(input("Enter Humidity: "))
ph = float(input("Enter pH value: "))
rainfall = float(input("Enter Rainfall: "))

sample = pd.DataFrame(
    [[N, P, K, temperature, humidity, ph, rainfall]],
    columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
)

prediction = model.predict(sample)

print("Recommended Crop:", prediction[0])