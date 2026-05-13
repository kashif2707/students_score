import streamlit as st
import joblib
import pandas as pd
import json
import os

# =========================
# USER FILE
# =========================
USER_FILE = "users.json"

# Create file if not exists
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

# Load users
with open(USER_FILE, "r") as f:
    users = json.load(f)

# =========================
# SESSION STATE
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# =========================
# LOGIN / SIGNUP PAGE
# =========================
if not st.session_state.logged_in:

    st.title("🔐 Login & Signup")

    menu = st.selectbox("Select", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # ================= LOGIN =================
    if menu == "Login":

        if st.button("Login"):

            if username in users and users[username] == password:
                st.success("Login Successful ✅")
                st.session_state.logged_in = True
                st.rerun()

            else:
                st.error("Invalid Username or Password")

    # ================= SIGNUP =================
    else:

        if st.button("Signup"):

            if username in users:
                st.warning("Username already exists")

            else:
                users[username] = password

                with open(USER_FILE, "w") as f:
                    json.dump(users, f)

                # AUTO LOGIN AFTER SIGNUP
                st.session_state.logged_in = True

                st.success("Account Created Successfully ✅")

                st.rerun()

# =========================
# MAIN APP
# =========================
# =========================
# MAIN APP
# =========================
else:

    # =========================
    # LOAD MODEL
    # =========================
    model = joblib.load("student_model.pkl")
    columns = joblib.load("model_columns.pkl")

    # =========================
    # TITLE
    # =========================
    st.title("🎓 Student Score Predictor")

    # =========================
    # INPUT FIELDS
    # =========================
    hours = st.number_input("Hours Studied", 0.0, 24.0)
    attendance = st.number_input("Attendance", 0.0, 100.0)
    previous = st.number_input("Previous Score", 0.0, 100.0)
    sleep = st.number_input("Sleep Hours", 0.0, 12.0)

    motivation = st.selectbox("Motivation Level", ["Low", "Medium", "High"])
    teacher = st.selectbox("Teacher Quality", ["Poor", "Average", "Good"])
    school = st.selectbox("School Type", ["Public", "Private"])
    internet = st.selectbox("Internet Access", ["Yes", "No"])
    income = st.selectbox("Family Income", ["Low", "Medium", "High"])
    parent = st.selectbox("Parental Involvement", ["Low", "Medium", "High"])
    education = st.selectbox("Parent Education", ["School", "College"])
    peer = st.selectbox("Peer Influence", ["Negative", "Neutral", "Positive"])
    resources = st.selectbox("Learning Resources", ["Low", "Medium", "High"])
    activities = st.selectbox("Extracurricular Activities", ["Yes", "No"])

    # =========================
    # PREDICTION BUTTON
    # =========================
    if st.button("Predict Score"):

        data = {
            "Hours_Studied": hours,
            "Attendance": attendance,
            "Previous_Scores": previous,
            "Sleep_Hours": sleep,

            "Motivation_Level": motivation,
            "Teacher_Quality": teacher,
            "School_Type": school,
            "Internet_Access": internet,
            "Family_Income": income,
            "Parental_Involvement": parent,
            "Parental_Education_Level": education,
            "Peer_Influence": peer,
            "Learning_Resources": resources,
            "Extracurricular_Activities": activities
        }

        input_df = pd.DataFrame([data])

        input_df = pd.get_dummies(input_df)

        input_df = input_df.reindex(columns=columns, fill_value=0)

        prediction = model.predict(input_df)

        final_score = max(40, min(100, prediction[0]))

        final_score = int(round(final_score))

        st.success(f"🎯 Predicted Exam Score: {final_score}")

    # =========================
    # SPACE
    # =========================
    st.write("")
    st.write("")
    st.write("")

    # =========================
    # LOGOUT BUTTON AT BOTTOM
    # =========================
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()