FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the project content to /app dir
COPY . .

# Install required libraries
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

# Expose 8000 
EXPOSE 8000

# CMD
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
