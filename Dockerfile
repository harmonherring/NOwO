FROM python:3.6.8-alpine3.9
ADD __init__.py /
ADD config.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD ["python", "./__init__.py"]