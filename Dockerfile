FROM python:3.10-slim
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Set environment variables (can be overridden at runtime)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]