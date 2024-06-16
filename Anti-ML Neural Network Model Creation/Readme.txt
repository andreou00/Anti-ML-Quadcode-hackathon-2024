This folder documents the creation process of our "Anti_ML_model.h5" Neural Network Model.

Data Generation: Unable to find suitable real-world datasets online, we opted to generate our own data. After numerous iterations, we developed the final version of "generatingTransactions.py." This Python script generates transaction data, including both money laundering and normal transactions, with added noise to closely resemble real-world data.

Model Training: We used the generated data to train our Neural Network model. The training and creation of the model were conducted using our script "A_ML_QuadCodehackathon_Neural_Network.ipynb." Our model achieved an impressive accuracy of 97% in detecting money laundering transactions.

Model Export: Post-training, we exported the model as "anti_ML_model.h5" to use on our demo for real-time data.

This comprehensive approach ensured the development of a robust and highly accurate model tailored for identifying money laundering activities.
