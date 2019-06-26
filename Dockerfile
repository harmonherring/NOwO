FROM python:3
ADD __init__.py /
ADD config.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
CMD ["python", "./__init__.py"]