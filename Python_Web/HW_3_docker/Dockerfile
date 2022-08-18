FROM python:latest

COPY . /HW_3

WORKDIR /HW_3/src

RUN pip install -r /HW_3/requirements.txt

ENTRYPOINT ["python"]
CMD ["main.py"]