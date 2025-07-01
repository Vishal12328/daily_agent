FROM python:3.11-slim

WORKDIR /home/newsletter-application

COPY . .

RUN pip install -r requirements.txt

CMD ["python","daily_agent.py"]
