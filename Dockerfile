FROM python:3.9

WORKDIR /wallet

COPY ./app/requirements.txt /wallet/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /wallet/requirements.txt

COPY ./ /wallet/
ENV PYTHONPATH=/wallet

CMD "/wallet/start.sh"