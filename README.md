# Credit Scoring project
## Purpose: 
 * Project is aimed to autonomically score the ability of returning money of each customer by assigning probability of default for each one
## Prerequisites
  * Python 3.10 - 3.11
  * Docker
## Project Structure
```bash
/credit_scoring_project
├── api.py
├── consumer.py
├── data
│   └── deploit_testing.csv
├── models
│   ├── mapping_dict.joblib
│   └── pipeline.joblib
├── notebooks
│   ├── 1_engineering_data.ipynb
│   ├── 2_EDA.ipynb
│   ├── 3_split_data.ipynb
│   └── 4_model.ipynb
├── preprocessor
│   ├── encode.py
│   ├── __pycache__
│   └── transformer.py
├── __pycache__
│   └── api.cpython-312.pyc
├── README.md
├── requirements.txt
└── ui.py
```

## Architecture
 <img width="862" height="435" alt="Image" src="https://github.com/user-attachments/assets/449910b4-5a60-4093-943f-cde03a0719fc" />d
 
## Instructions
* 1) Download the project
  ```bash
  git clone https://github.com/anhduong77/Credit-Scoring-ML-project.git
  ```
  
* 2) Create environment and install dependencies (python version 3.10 - 3.11)
  ```bash
  python3.11 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ```
  
* 3) Install RabbitMQ
  ```bash
  docker run -d --hostname my-rabbit --name rabbitmq \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management
  ```
* 4) Run program
  ```bash
  python consumer.py
  uvicorn api:app --reload --port 8000
  streamlit run ui.py
  ```
* 5) Upload data and test
     Go to http://localhost:8501/
     Upload available data in data/deploit_testing.csv
     Chose the row index and click the 'Predict selected row' button
