import pandas as pd
import numpy as np
import streamlit as st
import os
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler, LabelEncoder
from datetime import datetime

# Load the trained model
model_path = 'Anti_ML_model.h5'  # Ensure this is the correct path to the new model
model = load_model(model_path)

# Initialize the CSV file with headers if it doesn't exist or is empty
def initialize_csv(file_path):
    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        df = pd.DataFrame(columns=['typeofaction', 'sourceid', 'destinationid', 'amountofmoney', 'date'])
        df.to_csv(file_path, index=False)
        st.info(f"Created {file_path} with headers.")

# Check and clean CSV file by removing or correcting malformed lines
def check_csv_consistency(file_path):
    cleaned_lines = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                fields = line.strip().split(',')
                if len(fields) == 5:
                    cleaned_lines.append(line.strip())
    except Exception as e:
        st.error(f"Error reading file {file_path}: {e}")

    try:
        with open(file_path, 'w') as file:
            for line in cleaned_lines:
                file.write(line + '\n')
    except Exception as e:
        st.error(f"Error writing to file {file_path}: {e}")

# Preprocess and predict fraud types
def preprocess_and_predict(input_file_path, output_file_path):
    # Ensure the CSV file exists and has the correct headers
    initialize_csv(input_file_path)

    # Clean the CSV file before processing
    check_csv_consistency(input_file_path)

    # Load the cleaned transactions CSV file
    transactions_df = pd.read_csv(input_file_path)

    if transactions_df.empty:
        # If the DataFrame is empty, create an empty output file with headers
        result_df = pd.DataFrame(columns=['typeofaction', 'sourceid', 'destinationid', 'amountofmoney', 'date', 'fraud_type'])
        result_df.to_csv(output_file_path, index=False)
        st.info("No transactions to process. Created an empty output file with headers.")
        return result_df

    # Convert 'date' to datetime format
    transactions_df['date'] = pd.to_datetime(transactions_df['date'], errors='coerce', infer_datetime_format=True, dayfirst=True)

    # Drop rows with invalid dates
    transactions_df = transactions_df.dropna(subset=['date'])

    # Preserve the original columns for final output
    original_columns = transactions_df[['typeofaction', 'sourceid', 'destinationid', 'amountofmoney', 'date']]

    # Extract features from the 'date' column
    transactions_df['day'] = transactions_df['date'].dt.day
    transactions_df['month'] = transactions_df['date'].dt.month
    transactions_df['year'] = transactions_df['date'].dt.year
    transactions_df['hour'] = transactions_df['date'].dt.hour
    transactions_df['minute'] = transactions_df['date'].dt.minute

    # Encode 'typeofaction' column
    action_label_encoder = LabelEncoder()
    transactions_df['typeofaction'] = action_label_encoder.fit_transform(transactions_df['typeofaction'])

    # Drop the original 'date' column
    transactions_df.drop(columns=['date'], inplace=True)

    # Define the expected feature columns based on the model input shape
    feature_columns = ['typeofaction', 'sourceid', 'destinationid', 'amountofmoney', 'year', 'month', 'day', 'hour', 'minute']

    # Ensure all expected columns are present
    for col in feature_columns:
        if col not in transactions_df.columns:
            transactions_df[col] = 0

    # Reorder the columns to match the expected order
    transactions_df = transactions_df[feature_columns]

    # Standardize the features
    scaler = StandardScaler()
    transactions_df_scaled = scaler.fit_transform(transactions_df)

    # Make predictions
    predictions = model.predict(transactions_df_scaled)
    y_pred_classes = predictions.argmax(axis=-1)

    # Map predictions to fraud types
    fraud_mapping = {0: 'not_fraud', 1: 'fraud'}
    fraud_types = [fraud_mapping[pred] for pred in y_pred_classes]

    # Add fraud type to the original DataFrame
    result_df = original_columns.copy()
    result_df['fraud_type'] = fraud_types

    # Save the results to a new CSV file
    result_df.to_csv(output_file_path, index=False)

    print(f"Results saved to {output_file_path}")
    return result_df

# Ensure the transactions_with_fraud_types.csv is generated at the start
if not os.path.exists('transactions_with_fraud_types.csv'):
    transactions_df = preprocess_and_predict('transactions.csv', 'transactions_with_fraud_types.csv')

# Process the transactions_with_fraud_types.csv file to create transactions_with_fraud_final.csv
def mark_related_frauds(input_file_path, output_file_path):
    df = pd.read_csv(input_file_path)
    fraud_transactions = df[df['fraud_type'] == 'fraud']

    # Mark all transactions with the same sourceid and destinationid as fraud
    for index, fraud_txn in fraud_transactions.iterrows():
        df.loc[(df['sourceid'] == fraud_txn['sourceid']) |  
               (df['destinationid'] == fraud_txn['destinationid']), 'fraud_type'] = 'fraud'

    df.to_csv(output_file_path, index=False)
    print(f"Results saved to {output_file_path}")
    return df

# Function to analyze fraud transactions and print summary messages
def print_fraud_summary(df):
    fraud_transactions = df[df['fraud_type'] == 'fraud']
    if fraud_transactions.empty:
        st.info("No fraudulent transactions found.")
        return

    # Group by sourceid and destinationid to identify patterns
    grouped_by_source = fraud_transactions.groupby('sourceid')['amountofmoney'].sum().reset_index()
    grouped_by_dest = fraud_transactions.groupby('destinationid')['amountofmoney'].sum().reset_index()

    # Determine the fraud type and print appropriate messages
    for source_id, group in fraud_transactions.groupby('sourceid'):
        if len(group['destinationid'].unique()) > 1:
            total_amount = group['amountofmoney'].sum()
            st.markdown(f"<span style='color:yellow'>Total amount ${total_amount:.2f} was sent from source Account ID: {source_id} to {len(group['destinationid'].unique())} accounts.</span>", unsafe_allow_html=True)
    
    for dest_id, group in fraud_transactions.groupby('destinationid'):
        if len(group['sourceid'].unique()) > 1:
            total_amount = group['amountofmoney'].sum()
            st.markdown(f"<span style='color:yellow'>Total amount ${total_amount:.2f} was split and sent by {len(group['sourceid'].unique())} accounts to destination Account ID: {dest_id}.</span>", unsafe_allow_html=True)

# Create transactions_with_fraud_final.csv
final_df = mark_related_frauds('transactions_with_fraud_types.csv', 'transactions_with_fraud_final.csv')

# Streamlit UI
st.title('Money Laundering Detection Live Demo')

# Input fields for new transaction
st.header('Add New Transaction')
typeofaction = st.selectbox('Type of Action', ['cash-in', 'cash-out', 'transfer'])
sourceid = st.number_input('Source ID', min_value=0, step=1)
destinationid = st.number_input('Destination ID', min_value=0, step=1)
amountofmoney = st.number_input('Amount of Money', min_value=0.0, step=0.01)
date = st.date_input('Date', pd.to_datetime('2024-06-15'))
time = st.time_input('Time', datetime.strptime('00:00', '%H:%M').time())

if st.button('Add Transaction'):
    if amountofmoney == 0:
        st.error("Amount of money cannot be zero. Please enter a valid amount.")
    else:
        # Combine date and time
        combined_datetime = pd.to_datetime(f'{date} {time}')
        new_transaction = pd.DataFrame({
            'typeofaction': [typeofaction],
            'sourceid': [sourceid],
            'destinationid': [destinationid],
            'amountofmoney': [amountofmoney],
            'date': [combined_datetime.strftime('%Y-%m-%d %H:%M')]
        })

        # Ensure the CSV file exists and has the correct headers
        initialize_csv('transactions.csv')

        # Check if transactions.csv exists and has the correct columns
        existing_df = pd.read_csv('transactions.csv', on_bad_lines='skip')
        if list(existing_df.columns) != list(new_transaction.columns):
            st.error("The columns of the existing transactions.csv do not match the new transaction.")
        else:
            # Append the new transaction to the CSV file
            new_transaction.to_csv('transactions.csv', mode='a', header=False, index=False)

        # Reprocess the entire CSV and update the results
        transactions_df = preprocess_and_predict('transactions.csv', 'transactions_with_fraud_types.csv')
        final_df = mark_related_frauds('transactions_with_fraud_types.csv', 'transactions_with_fraud_final.csv')

        # Display the result
        st.subheader('Predicted Transaction')
        st.write(final_df.tail(1))

# Button to clear the transactions.csv file and delete related files
if st.button('Clear Transactions'):
    open('transactions.csv', 'w').close()  # Clear the file contents
    initialize_csv('transactions.csv')  # Reinitialize with headers
    if os.path.exists('transactions_with_fraud_types.csv'):
        os.remove('transactions_with_fraud_types.csv')  # Delete the file if it exists
    if os.path.exists('transactions_with_fraud_final.csv'):
        os.remove('transactions_with_fraud_final.csv')  # Delete the file if it exists
    st.success("Transactions and related files have been cleared.")

# Load the processed transactions CSV file
output_file_path = 'transactions_with_fraud_final.csv'
if os.path.exists(output_file_path):
    transactions_with_fraud_final_df = pd.read_csv(output_file_path, on_bad_lines='skip')
else:
    transactions_with_fraud_final_df = pd.DataFrame(columns=['typeofaction', 'sourceid', 'destinationid', 'amountofmoney', 'date', 'fraud_type'])

# Function to highlight fraud transactions
def highlight_fraud(row):
    color = 'red' if row['fraud_type'] == 'fraud' else ''
    return ['background-color: {}'.format(color) for _ in row]

# Display the transactions with fraud types highlighted
st.subheader('Display to Money Laundering Department')
st.dataframe(transactions_with_fraud_final_df.style.apply(highlight_fraud, axis=1))

# Print fraud summary messages
print_fraud_summary(transactions_with_fraud_final_df)
