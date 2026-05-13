import joblib
import pandas as pd

# Load model and columns
model = joblib.load("student_model.pkl")
columns = joblib.load("model_columns.pkl")

# Take input
data = {
    "Hours_Studied": float(input("Hours Studied: ")),
    "Attendance": float(input("Attendance: ")),
    "Previous_Scores": float(input("Previous Score: ")),
    "Sleep_Hours": float(input("Sleep Hours: ")),

    "Motivation_Level": input("Motivation Level (Low/Medium/High): "),
    "Teacher_Quality": input("Teacher Quality (Poor/Average/Good): "),
    "School_Type": input("School Type (Public/Private): "),
    "Internet_Access": input("Internet Access (Yes/No): "),
    "Family_Income": input("Family Income (Low/Medium/High): "),
    "Parental_Involvement": input("Parental Involvement (Low/Medium/High): "),
    "Parental_Education_Level": input("Parent Education (School/College): "),
    "Peer_Influence": input("Peer Influence (Negative/Neutral/Positive): "),
    "Learning_Resources": input("Resources (Low/Medium/High): "),
    "Extracurricular_Activities": input("Activities (Yes/No): ")
}

# Convert to DataFrame
input_df = pd.DataFrame([data])

# Apply encoding
input_df = pd.get_dummies(input_df)

# Match training columns
input_df = input_df.reindex(columns=columns, fill_value=0)

# Predict
prediction = model.predict(input_df)

print("\n🎯 Predicted Exam Score:", round(prediction[0], 2))