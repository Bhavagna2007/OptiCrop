from flask import Flask, render_template, request
from pathlib import Path
import os
import pickle
import pandas as pd

try:
    import joblib
except ModuleNotFoundError:
    joblib = None

# ----------------------------
# Flask App Configuration
# ----------------------------
base_dir = Path(__file__).resolve().parent
template_dir = base_dir / "templates"
static_dir = base_dir / "static"

app = Flask(
    __name__,
    template_folder=str(template_dir),
    static_folder=str(static_dir),
)

# ----------------------------
# Load Trained Model
# ----------------------------
model_candidates = [
    base_dir / "crop_model.pkl",
    base_dir / "dataset" / "notebook" / "crop_model.pkl",
]
model_path = next((path for path in model_candidates if path.exists()), None)

if model_path is None:
    raise FileNotFoundError("Model file not found. Expected crop_model.pkl in the project root or dataset/notebook.")

if joblib is not None:
    try:
        model = joblib.load(model_path)
    except Exception:
        with open(model_path, "rb") as f:
            model = pickle.load(f)
else:
    with open(model_path, "rb") as f:
        model = pickle.load(f)

# ----------------------------
# Crop Descriptions
# ----------------------------
crop_info = {
    "rice": "Rice grows best in warm and humid climates with abundant rainfall and fertile soil.",
    "maize": "Maize prefers well-drained fertile soil with moderate rainfall and good sunlight.",
    "chickpea": "Chickpea grows best in cool climates with well-drained loamy soil.",
    "kidneybeans": "Kidney beans require moderate temperatures and fertile soil rich in organic matter.",
    "pigeonpeas": "Pigeon pea grows well in tropical climates with medium rainfall.",
    "mothbeans": "Moth beans are drought-resistant and grow well in sandy soils.",
    "mungbean": "Mung bean grows best in warm climates with well-drained soil.",
    "blackgram": "Blackgram prefers loamy soil and warm weather conditions.",
    "lentil": "Lentils grow best in cool weather with fertile, well-drained soil.",
    "pomegranate": "Pomegranate requires warm temperatures and well-drained soil.",
    "banana": "Banana grows well in tropical climates with high humidity and rich soil.",
    "mango": "Mango prefers warm climates with moderate rainfall and deep soil.",
    "grapes": "Grapes require sunny weather and well-drained soil.",
    "watermelon": "Watermelon grows best in warm temperatures with sandy loam soil.",
    "muskmelon": "Muskmelon thrives in warm climates with fertile, well-drained soil.",
    "apple": "Apple grows best in cool climates with fertile, well-drained soil.",
    "orange": "Orange requires subtropical climates and well-drained soil.",
    "papaya": "Papaya grows well in tropical climates with plenty of sunlight.",
    "coconut": "Coconut prefers coastal tropical climates with sandy soil.",
    "cotton": "Cotton grows best in black soil under warm climatic conditions.",
    "jute": "Jute requires high humidity, warm temperatures and heavy rainfall.",
    "coffee": "Coffee grows best in cool tropical climates with rich, well-drained soil.",
}

# ----------------------------
# Home Route
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    prediction = ""
    description = ""

    N = ""
    P = ""
    K = ""
    temperature = ""
    humidity = ""
    ph = ""
    rainfall = ""

    if request.method == "POST":
        try:
            N = float(request.form["N"])
            P = float(request.form["P"])
            K = float(request.form["K"])
            temperature = float(request.form["temperature"])
            humidity = float(request.form["humidity"])
            ph = float(request.form["ph"])
            rainfall = float(request.form["rainfall"])

            sample = pd.DataFrame(
                [[N, P, K, temperature, humidity, ph, rainfall]],
                columns=[
                    "N",
                    "P",
                    "K",
                    "temperature",
                    "humidity",
                    "ph",
                    "rainfall",
                ],
            )

            prediction = str(model.predict(sample)[0]).strip()
            description = crop_info.get(
                prediction.lower(),
                "No information available for this crop.",
            )
        except Exception as e:
            prediction = "Error"
            description = str(e)

    return render_template(
        "index.html",
        prediction=prediction,
        description=description,
        N=N,
        P=P,
        K=K,
        temperature=temperature,
        humidity=humidity,
        ph=ph,
        rainfall=rainfall,
    )


# ----------------------------
# Run Flask App
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
