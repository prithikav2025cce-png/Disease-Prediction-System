from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Mock disease models - weighting different symptoms for different diseases
# Symptoms mapping to disease weights
DISEASE_WEIGHTS = {
    "COVID-19": {
        "Loss of taste or smell": 0.35,
        "Difficulty breathing": 0.25,
        "Fever": 0.15,
        "Cough": 0.10,
        "Fatigue": 0.05,
        "Body aches": 0.05,
        "Headaches": 0.05
    },
    "Flu": {
        "Fever": 0.25,
        "Body aches": 0.20,
        "Fatigue": 0.15,
        "Headaches": 0.15,
        "Cough": 0.10,
        "Sore throat": 0.10,
        "Runny nose": 0.05
    },
    "Common Cold": {
        "Runny nose": 0.25,
        "Sneezing": 0.25,
        "Sore throat": 0.20,
        "Cough": 0.15,
        "Fatigue": 0.10,
        "Itchy eyes": 0.05
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json() or {}
    symptoms = data.get('symptoms', [])
    
    if not symptoms:
        return jsonify([
            {"disease": "COVID-19", "confidence": 0.0},
            {"disease": "Flu", "confidence": 0.0},
            {"disease": "Common Cold", "confidence": 0.0}
        ])

    results = []
    
    # Calculate weighted scores
    for disease, weights in DISEASE_WEIGHTS.items():
        score = 0.0
        for symptom in symptoms:
            if symptom in weights:
                score += weights[symptom]
        
        # Add a tiny bit of random variation so it feels "AI"-like
        noise = random.uniform(-0.02, 0.05)
        # Cap score between 0 and 0.98 + noise to avoid perfect 100% just from simplistic model
        final_score = min(max(score + noise, 0.01), 0.98) 
        
        results.append({
            "disease": disease,
            "confidence": round(final_score * 100, 1)
        })

    # Sort results by confidence descending
    results.sort(key=lambda x: x['confidence'], reverse=True)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
