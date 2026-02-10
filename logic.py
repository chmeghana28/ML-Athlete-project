import pandas as pd
import joblib

# ------------------ Load ML models ------------------
kmeans = joblib.load("kmeans.pkl")
scaler = joblib.load("scaler.pkl")
sport_encoder = joblib.load("sport_encoder.pkl")

cal_model = joblib.load("cal_model.pkl")
hydration_model = joblib.load("hydration_model.pkl")

# ------------------ Load nutrition dataset ------------------
nutrition_df = pd.read_csv(r"C:\Users\deepi\OneDrive\Desktop\ML proj\nutrition.csv")

features = ['sex', 'age', 'height_cm', 'weight_kg', 'sport_encoded']

# ------------------ Helper functions ------------------
def exercise_plan(cluster, bmi):
    if cluster == 0:
        return "Mixed cardio + strength training"
    if cluster == 1:
        return "Endurance training"
    if cluster == 2:
        return "Strength & power training"
    return "Speed & agility training"

def injury_guidance(bmi, age):
    tips = []
    if bmi >= 27:
        tips.append("Avoid high-impact exercises")
    if age >= 30:
        tips.append("Increase recovery & stretching")
    if not tips:
        tips.append("Low injury risk")
    return tips

def food_recommendation(calorie_target):
    foods = nutrition_df[nutrition_df['calories'] <= calorie_target / 3]
    return foods.sample(min(5, len(foods)))[
        ['name', 'calories', 'protein', 'carbohydrate', 'total_fat']
    ]

# ------------------ Main function ------------------
def recommend_from_input(sex, height_cm, weight_kg, age, sport, activity_level):

    sex_map = {"Male": 0, "Female": 1}

    df = pd.DataFrame([{
        "sex": sex_map[sex],
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "sport_encoded": (
            sport_encoder.transform([sport])[0]
            if sport in sport_encoder.classes_ else 0
        )
    }])

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    X_scaled = scaler.transform(df[features])
    cluster = int(kmeans.predict(X_scaled)[0])

    ml_df = pd.DataFrame([{
        "sex": sex_map[sex],
        "age": age,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "duration": activity_level * 20
    }])

    calories = cal_model.predict(ml_df)[0]
    hydration = hydration_model.predict(ml_df)[0]

    foods = food_recommendation(calories)

    return {
        "Sport": sport,
        "Athlete_Type": cluster,
        "BMI": round(bmi, 2),
        "Daily_Calories": int(calories),
        "Exercise": exercise_plan(cluster, bmi),
        "Hydration_ml": int(hydration),
        "Injury_Guidance": injury_guidance(bmi, age),
        "Food_Recommendations": foods
    }
