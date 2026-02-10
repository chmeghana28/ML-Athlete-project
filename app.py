import streamlit as st
from logic import recommend_from_input

st.set_page_config(page_title="Athlete Nutrition & Fitness Recommender", page_icon="🏋️")
st.title("🏋️ Athlete Nutrition & Fitness Recommender")

st.header("Enter Athlete Details")

sex = st.selectbox("Sex", ["Male", "Female"])
age = st.number_input("Age", min_value=10, max_value=100, value=25)
height_cm = st.number_input("Height (cm)", min_value=100, max_value=250, value=175)
weight_kg = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
sport = st.text_input("Sport", "Soccer")

activity_level = st.selectbox("Activity Level", ["Low", "Medium", "High"])
activity_map = {"Low": 1, "Medium": 2, "High": 3}
activity_level_num = activity_map[activity_level]

# ------------------ BUTTON ------------------
if st.button("Get Recommendations"):
    try:
        result = recommend_from_input(
            sex,
            height_cm,
            weight_kg,
            age,
            sport,
            activity_level_num
        )

        st.subheader("🏆 Recommendations")
        st.write(f"**Sport:** {result['Sport']}")
        st.write(f"**Athlete Type:** {result['Athlete_Type']}")
        st.write(f"**BMI:** {result['BMI']}")
        st.write(f"**Daily Calories:** {result['Daily_Calories']} kcal")
        st.write(f"**Hydration:** {result['Hydration_ml']} ml/day")
        st.write(f"**Exercise:** {result['Exercise']}")
        st.write(f"**Injury Guidance:** {', '.join(result['Injury_Guidance'])}")

        st.subheader("🍽️ Nutrition Plan (Food Recommendations)")
        st.dataframe(result["Food_Recommendations"])

    except Exception as e:
        st.error(f"Error: {e}")
