FROM python:3.11.1-alpine
COPY main.py .
CMD ["python", "main.py"]