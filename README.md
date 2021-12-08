# YTU Embedded Systems Weather Monitor Web Center
This project aiming to stream raspberry pi weather sensors to serve external monitor service.  

This project uses venv for manage python virtual environment so follow this guideline.  

# 1-Install venv and Create venv
- https://docs.python.org/3/library/venv.html  
- pip install virtualenv
- python -m venv venv
- (Windows) .\venv\Scripts\activate
- (Linux) ./venv/scripts/activate
- You are ready to go!!!

# 2-Usage
- Go to project directory via activated venv cli
- pip install -r requirements.txt
- set FLASK_APP=app.py
- flask run 