import pickle
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import warnings
import shap
import google.generativeai as genai
import os
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
warnings.filterwarnings('ignore')

amount = 0.0;
transaction_type = "";
location = "";
account_id = "";

gemini = genai.GenerativeModel("gemini-1.5-flash")

FILE_PATH = os.getcwd()

subset_df = pd.read_csv(FILE_PATH+'/server/model/dataset/subset_df.csv')
subset_df_2 = pd.read_csv(FILE_PATH+'/server/model/dataset/subset_df.csv')

# Label encoder
label_encoders = {}

def get_label_encoders():
    for col in ['TransactionType', 'Location', 'AccountID']:
        le = LabelEncoder()
        subset_df[col] = le.fit_transform(subset_df[col])
        label_encoders[col] = {
            'encoder': le,
            'mapping': dict(zip(le.classes_, le.transform(le.classes_)))
        }

def apply_and_update_encoding(new_df):
    """
    Memproses DataFrame baru dengan label encoding.
    Jika ditemukan nilai baru pada kolom, nilai tersebut akan ditambahkan ke LabelEncoder.
    """
    df_copy = new_df.copy()

    for col, encoder_dict in label_encoders.items():
        if col in df_copy.columns:
            le = encoder_dict['encoder']

            # Identifikasi nilai baru yang belum ada di encoder
            current_classes = set(le.classes_)
            new_classes = set(df_copy[col].unique()) - current_classes

            if new_classes:
                # Tambahkan nilai baru ke encoder
                le.classes_ = np.append(le.classes_, list(new_classes))

            # Encode data menggunakan encoder yang diperbarui
            df_copy[col] = le.transform(df_copy[col])

            # Perbarui mapping
            encoder_dict['mapping'] = dict(zip(le.classes_, le.transform(le.classes_)))

    return df_copy

# Fungsi untuk covert variable menjadi 1 baris DataFrame
def convert_to_dataframe(amount, transaction_type, location, account_id):
    data = {
        'Amount': [amount],
        'TransactionType': [transaction_type],
        'Location': [location],
        'AccountID': [account_id]
    }
    df = pd.DataFrame(data)
    return df

# Function ambil variable dari prompt user
def process_user_prompt(prompt):
    global amount, transaction_type, location, account_id
    try:
        response = gemini.generate_content(f"""
        Extract the following information from this transaction description: '{prompt}'
        - Amount (as a number)
        - Transaction Type
        - Location
        - Account ID
        Format your response exactly like this:
        amount: [number]
        type: [text]
        location: [text]
        account: [text]
        """)

        lines = response.text.strip().split('\n')
        for line in lines:
            if line.startswith('amount:'):
                amount = float(line.split(':')[1].strip())
            elif line.startswith('type:'):
                transaction_type = line.split(':')[1].strip()
            elif line.startswith('location:'):
                location = line.split(':')[1].strip()
            elif line.startswith('account:'):
                account_id = line.split(':')[1].strip()

        return True
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return False

def convert_to_dataframe(amount, transaction_type, location, account_id):
    data = {
        'Amount': [amount],
        'TransactionType': [transaction_type],
        'Location': [location],
        'AccountID': [account_id]
    }
    df = pd.DataFrame(data)
    return df


def load_models(file_path):
    with open(file_path, 'rb') as file:
        models = pickle.load(file)
    return models

    # Create MinMaxScaler instance for 'Amount' column

def scale_amount(df):
    amount_scaler = MinMaxScaler()
    amount_scaler.fit(df[['Amount']])

    df_copy = df.copy()
    df_copy['Amount'] = amount_scaler.transform(df_copy[['Amount']])
    return df_copy

# GEMINI
# GEMINI
# Anomaly = df asli sebelum di encode dll
# Shap output df = df hasil shap
# data = subset_df atau yang lain (pokok yang masih ori aja tanpa encode)
def gemini_explanation(data, anomaly_df, shap_output_df, user_input):
    anomaly = anomaly_df.iloc[0]  # Ambil baris pertama jika ada banyak baris

    total_contribution = shap_output_df['total_contribution'].iloc[0]

    if total_contribution > 0:
        def check_outlier(df):
            features = df[['Amount', 'TransactionType', 'Location', 'AccountID']]
            max_feature = features.abs().sum().idxmax()
            return max_feature

        feature_name = check_outlier(shap_output_df)
        print(feature_name)

        if feature_name == "Amount":
            non_anomaly_avg_amount = data[
                (data['Location'] == anomaly['Location']) &
                (data['AccountID'] == anomaly['AccountID']) &
                (data['TransactionType'] == anomaly['TransactionType'])
            ]['Amount'].mean()

            non_anomaly_avg_amount = non_anomaly_avg_amount if not pd.isna(non_anomaly_avg_amount) else 0

            reason = (
                f"The transaction amount of {anomaly['Amount']} is significantly "
                f"different from the average transaction amount ({non_anomaly_avg_amount:.2f}) for "
                f"similar accounts ({anomaly['AccountID']}), locations ({anomaly['Location']}), "
                f"and transaction types ({anomaly['TransactionType']}). "
            )
        elif feature_name == "Location":
            usual_location = data[
                (data['AccountID'] == anomaly['AccountID']) &
                (data['TransactionType'] == anomaly['TransactionType'])
            ]['Location'].mode().iloc[0]

            reason = (
                f"The transaction originated from a location ({anomaly['Location']}) that is "
                f"inconsistent with the usual locations ({usual_location}) for similar accounts ({anomaly['AccountID']}). "
                f"This anomaly in location contributes to its classification as an outlier."
            )
        else:
            reason = (
                f"The transaction deviates significantly in terms of {feature_name}. "
                f"This deviation suggests it does not align with expected behavior for similar transactions."
            )

        base_prompt = (
            f"Explain why the transaction is considered an anomaly. "
            f"{reason}"
            f"Where, this transaction is one of several financial transaction records on the ERP Website System. "
            f"Provide a detailed explanation to justify why this transaction is anomalous."
        )

        if user_input:
            base_prompt += f" User asked: '{user_input}'"

        print(base_prompt)

        response = gemini.generate_content(base_prompt)
        file_name = f"response_{anomaly['AccountID']}.txt"
        with open(file_name, "w") as file:
            file.write(response.text)

        print(response.text)
        return response.text

    else:
        # Jika total_contribution negatif, tidak ada anomaly
        message = (
            f"No ERP anomaly detected. All transactions appear normal based on the SHAP values {total_contribution:.3f}."
        )
        file_name = f"response_{anomaly['AccountID']}.txt"
        with open(file_name, "w") as file:
            file.write(message)

        print(message)
        return message


file_path = FILE_PATH+ '/server/model/trained_models.pkl'
models = load_models(file_path)
model1, model2, model3, model4, model5 = models

# Calculate SHAP values for each model
shap_values_list = []

def generate_shap_values(final_df):
    for fold, model in enumerate(models):
        explainer = shap.Explainer(model)
        shap_values = explainer(final_df)  # SHAP values for test set in this fold
        shap_values_list.append(shap_values)

    # Aggregate SHAP values (mean across folds)
    shap_values_mean_3 = np.mean([shap_values.values for shap_values in shap_values_list], axis=0)

    shap_values_mean_df_3 = pd.DataFrame(
        shap_values_mean_3,
        columns=final_df.columns  # Nama fitur
    )
    shap_values_mean_df_3['total_contribution'] = shap_values_mean_3.sum(axis=1)  # Total kontribusi per baris
    return shap_values_mean_df_3

def __init__(self, name):
    self.name = name

def Generative_AI(prompt):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    genai.configure(api_key=gemini_api_key)

    get_label_encoders()

    process_user_prompt(prompt)

    df_row = convert_to_dataframe(amount, transaction_type, location, account_id)
    print(df_row)

    encoded_df = apply_and_update_encoding(df_row)
    print(encoded_df)

    encoded_subset_df = apply_and_update_encoding(subset_df_2)

    final_df = encoded_df.copy()

    mms = MinMaxScaler(feature_range=(0, 1))
    mms.fit(encoded_subset_df[['Amount']])  # Fit hanya sekali pada subset_df

    final_df['Amount'] = mms.transform(final_df[['Amount']])

    print(final_df)
    print(subset_df_2)

    shap_values_mean_df = generate_shap_values(final_df)

    message = gemini_explanation(subset_df_2, df_row, shap_values_mean_df, "")

    return message
