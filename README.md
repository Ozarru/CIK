# CIK

python3 -m venv venv
venv/scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
