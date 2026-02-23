FROM python:3.10
WORKDIR /app
RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]  