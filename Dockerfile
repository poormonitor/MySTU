FROM python:3.11-slim

COPY requirements.txt .
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r requirements.txt --no-cache-dir

WORKDIR /app
VOLUME /app

EXPOSE 8000

# command for flask
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "server:app"]
