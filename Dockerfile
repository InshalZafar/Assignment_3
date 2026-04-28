FROM python:3.10

# Install Chrome + driver
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install selenium pytest

# Set environment
ENV PYTHONUNBUFFERED=1

# Run tests
CMD ["pytest", "-v"]