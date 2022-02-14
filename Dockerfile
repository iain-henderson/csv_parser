FROM python:alpine

COPY csv_parser.py csv_parser.py

ENTRYPOINT ["python3", "csv_parser.py"]