FROM python:3.9

WORKDIR /wallet

COPY ./app/requirements.txt /wallet/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /wallet/requirements.txt

COPY ./app /wallet/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]