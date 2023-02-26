FROM python:slim

WORKDIR /app
COPY fritz_dyndns.py requirements.txt .

RUN python -m pip install -r requirements.txt

CMD ["python3", "fritz_dyndns.py"]