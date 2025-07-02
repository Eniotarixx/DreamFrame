# Base image  
FROM python:3.13.5-bookworm

RUN apt-get update && apt-get install -y libgl1

# Work directory 
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tthe '.' is a reference to the WORKDIR
COPY dream_frame.py .
COPY main.py .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]