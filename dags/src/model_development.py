import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import os

def get_data_dir():
    # Detect correct base path whether Airflow runs from Lab_3 or dags
    this_file = os.path.abspath(__file__)
    base_dir = os.path.dirname(os.path.dirname(this_file))  # Lab_3/
    data_dir = os.path.join(base_dir, "dags", "data")

    # If airflow already runs inside dags/, fallback to dags/data directly
    if not os.path.exists(data_dir):
        data_dir = os.path.join(base_dir, "data")
    return data_dir

def clean_data():
    data_dir = get_data_dir()
    input_path = os.path.join(data_dir, "health_data.csv")
    output_path = os.path.join(data_dir, "clean_health_data.csv")

    print(f"Reading data from: {input_path}")
    df = pd.read_csv(input_path)
    df.dropna(inplace=True)
    df = df.drop_duplicates().reset_index(drop=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

def train_model():
    data_dir = get_data_dir()
    input_path = os.path.join(data_dir, "clean_health_data.csv")
    df = pd.read_csv(input_path)

    le = LabelEncoder()
    df['status_encoded'] = le.fit_transform(df['status'])

    X = df[['bmi', 'cholesterol', 'blood_pressure']]
    y = df['status_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    clf = RandomForestClassifier(random_state=42)
    clf.fit(X_train_scaled, y_train)

    y_pred = clf.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)

    model_path = os.path.join(data_dir, "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)

    print(f"Model trained and saved to {model_path}")
    print(f"Accuracy: {acc:.2f}")
    return acc

def evaluate_model():
    data_dir = get_data_dir()
    model_path = os.path.join(data_dir, "model.pkl")
    data_path = os.path.join(data_dir, "clean_health_data.csv")

    with open(model_path, "rb") as f:
        model = pickle.load(f)

    df = pd.read_csv(data_path)
    X = df[['bmi', 'cholesterol', 'blood_pressure']]
    le = LabelEncoder()
    df['status_encoded'] = le.fit_transform(df['status'])
    y = df['status_encoded']

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    y_pred = model.predict(X_scaled)
    acc = accuracy_score(y, y_pred)
    print(f"Evaluation complete, accuracy: {acc:.2f}")
    return acc
