# Base image  
FROM python:3.13.5-bookworm

# Work directory 
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tthe '.' is a reference to the WORKDIR
COPY app.py .



# Command to execute when the container is lauch 
CMD ["python", "app.py"]