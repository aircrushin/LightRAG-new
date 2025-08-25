# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# 先彻底清理原有源
RUN rm -f /etc/apt/sources.list && \
    rm -rf /etc/apt/sources.list.d/ && \
    echo "deb https://mirrors.aliyun.com/debian bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian-security bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb https://mirrors.aliyun.com/debian bullseye-updates main non-free contrib" >> /etc/apt/sources.list

# Install Rust and required build dependenciesc
RUN apt-get update

RUN apt-get install -y \
    curl \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN  curl --proto '=https' --tlsv1.2 -sSf https://rsproxy.cn/rustup-init.sh | sh -s -- -y \
    && . $HOME/.cargo/env

# Copy pyproject.toml and source code for dependency installation
COPY pyproject.toml .
COPY setup.py .
COPY lightrag/ ./lightrag/

# Install dependencies
ENV PATH="/root/.cargo/bin:${PATH}"
RUN pip install --user --no-cache-dir .
RUN pip install --user --no-cache-dir .[api]

# Install depndencies for default storage
RUN pip install --user --no-cache-dir nano-vectordb networkx
# Install depndencies for default LLM
RUN pip install --user --no-cache-dir openai ollama tiktoken
# Install depndencies for default document loader
RUN pip install --user --no-cache-dir pypdf2 python-docx python-pptx openpyxl

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local
COPY ./lightrag ./lightrag
COPY setup.py .

RUN pip install ".[api]"
# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create necessary directories
RUN mkdir -p /app/data/rag_storage /app/data/inputs

# Docker data directories
ENV WORKING_DIR=/app/data/rag_storage
ENV INPUT_DIR=/app/data/inputs

# Expose the default port
EXPOSE 9621

# Set entrypoint
ENTRYPOINT ["python", "-m", "lightrag.api.lightrag_server"]
