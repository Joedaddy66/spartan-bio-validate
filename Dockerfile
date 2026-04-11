FROM python:3.11-slim

# 1. Install the missing C++ library (libstdc++6)
RUN apt-get update && apt-get install -y \
    libstdc++6 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Setup the virtual environment and install fuel
COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the Spartan Engine
COPY . .

# 4. Set the ignition
CMD ["python", "spartan_agent.py"]
