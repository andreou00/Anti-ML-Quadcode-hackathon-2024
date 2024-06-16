
Anti-Money Laundering system using Machine learning model Neural Network.

# Anti-Money Laundering Neural Network Model

This project documents the creation and deployment of the "Anti_ML_model.h5" Neural Network Model designed to detect money laundering activities in transaction data.

## Table of Contents

1. [Data Generation](#data-generation)
2. [Model Training](#model-training)
3. [Model Export](#model-export)
4. [Usage](#usage)
5. [Scripts and Files](#scripts-and-files)
6. [Running the Project](#running-the-project)
7. [Example Usage](#example-usage)
8. [Dependencies](#dependencies)

## Data Generation

Due to the lack of suitable real-world datasets, we generated our own transaction data. The final version of the script `generatingTransactions.py` was used to create a dataset that includes both normal and money laundering transactions with added noise to mimic real-world complexities.

## Model Training

We used the generated dataset to train our Neural Network model using the script `A_ML_QuadCodehackathon_Neural_Network.ipynb`. This model achieved an accuracy of 97% in detecting money laundering transactions.

## Model Export

After training, the model was exported as `anti_ML_model.h5` for deployment and further use.

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

- **`generatingTransactions.py`**: Script to generate synthetic transaction data.
- **`A_ML_QuadCodehackathon_Neural_Network.ipynb`**: Jupyter notebook used for training and creating the neural network model.
- **`A-ML_Demo_Quadcode_hackathon.py`**: Script for loading the model, processing transaction data, making predictions, and interacting via a Streamlit UI.
- **`Anti_ML_model.h5`**: The trained neural network model.

## Running the Project

1. **Data Generation**:
   - Run the `generatingTransactions.py` script to create a dataset of transactions.

2. **Model Training**:
   - Use the Jupyter notebook `A_ML_QuadCodehackathon_Neural_Network.ipynb` to train the neural network model and export it as `anti_ML_model.h5`.

3. **Model Deployment and Interaction**:
   - Use the `A-ML_Demo_Quadcode_hackathon.py` script to load the model, preprocess transaction data, make predictions, and visualize results using Streamlit.

## Example Usage

To start the Streamlit app for interactive use, run:
```bash
streamlit run A-ML_Demo_Quadcode_hackathon.py


![image](https://github.com/andreou00/Anti-ML-Quadcode-hackathon-2024/assets/157217334/8e3a5178-7ba1-4361-bf70-27b1ae254593)
