FROM python:3.10-slim 

WORKDIR /app
COPY . . 
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt --no-cache-dir 

CMD ["python", "dvmn_checker.py.py"]