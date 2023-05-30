
# Automated Financial Analysis

### Description

This project automates the financial analysis, generates an excel analysis report and sends the calculated reports to user mentioned mail id.
 
### Software Design

 - Finance APIs and libraries used - **yfinance** (for basic stock data), **AlphaVantageAPI**(for obtaining financial statements)
 - Utilized *stmplib*, *mime* and *google's stmp server* for sending emails
 - Incorporated Flask and **Flask Restful** libraries for creating an API for Automating Financial Analysis
 - Deployed with GCP 




### Usage

1. Get the required environment variables

2. Clone the repository

```ssl
git clone https://github.com/kowshik27/Financial-Analysis-Automation.git
```

3. Install and activate virtual environment


- Activating Virtual env in Linux/Ubuntu
```ssl
source <venv_name>/bin/activate
```
- For Windows
```ssl
venv\Scripts\activate
```

4. Install the dependencies

```python
pip install -r requirements.txt
```

5. Run the Flask App
```python
python app.py
```


### Environment Variables

To run this project, you will need to add the following environment variables to your .env file

 1. `api_key` for AlphaVantageAPI. Get a free api at [this link](https://www.alphavantage.co/support/#api-key). 

 2. `smtp password` and `sender mail/smtp username` using any smtp server. I have used google smtp server. Refer this video for activat

