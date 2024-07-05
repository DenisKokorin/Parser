FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD alembic upgrade 560928765d92;uvicorn src.main:app --host 0.0.0.0 --port 80