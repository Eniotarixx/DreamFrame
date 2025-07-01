# Base image  
FROM python:3.13.5-bookworm

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*



# Work directory 
WORKDIR /app

# Copy the current directory contents into the container at /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tthe '.' is a reference to the WORKDIR
COPY dream_frame.py .
COPY main.py .



# Command to execute when the container is lauch 
#CMD ["python", "dream_frame.py"]

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]