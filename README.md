# Anti-Money Laundering Neural Network Model

This project documents the deployment and usage of the "Anti_ML_model.h5" Neural Network Model designed to detect money laundering activities in transaction data.

## Table of Contents

1. [Introduction](#introduction)
2. [Usage](#usage)
3. [Scripts and Files](#scripts-and-files)
4. [Running the Project](#running-the-project)
5. [Example Usage](#example-usage)
6. [Dependencies](#dependencies)
7. [Model Creation](#model-creation)

## Introduction

This repository contains the necessary files and scripts to deploy and interact with the "Anti_ML_model.h5" Neural Network Model for detecting money laundering transactions. The primary focus is on the deployment and usage of the model using the following key files:

- `A-ML_Demo_Quadcode_hackathon.py`
- `Anti_ML_model.h5`
- `transactions.csv`

## Usage

1. **Initializing the CSV File**:
   - The `initialize_csv` function ensures that the CSV file `transactions.csv` is created with the appropriate headers if it does not already exist or is empty.

2. **Data Consistency**:
   - The `check_csv_consistency` function checks the CSV file for any malformed lines and corrects them to maintain data integrity.

3. **Preprocessing and Prediction**:
   - The `preprocess_and_predict` function preprocesses the transaction data, makes predictions using the trained model, and outputs the results to a new CSV file `transactions_with_fraud_types.csv`.

4. **Marking Related Frauds**:
   - The `mark_related_frauds` function processes the prediction results to mark related transactions as fraudulent, saving the final results to `transactions_with_fraud_final.csv`.

5. **Streamlit UI**:
   - The Streamlit UI allows for adding new transactions, viewing predictions, and analyzing fraud patterns interactively.

## Scripts and Files

- **`A-ML_Demo_Quadcode_hackathon.py`**: Script for loading the model, processing transaction data, making predictions, and interacting via a Streamlit UI.
- **`Anti_ML_model.h5`**: The trained neural network model.
- **`transactions.csv`**: The CSV file containing transaction data.

## Running the Project

![image](https://github.com/andreou00/Anti-ML-Quadcode-hackathon-2024/assets/157217334/8e3a5178-7ba1-4361-bf70-27b1ae254593)

1. **Initialize and Clean Data**:
   - Ensure `transactions.csv` is initialized and consistent by running the relevant functions in the `A-ML_Demo_Quadcode_hackathon.py` script.

2. **Start the Streamlit App**:
   - Use the following command to start the Streamlit app and interact with the model:
   ```bash
   streamlit run A-ML_Demo_Quadcode_hackathon.py





