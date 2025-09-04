# Use an official Python runtime as a parent image
FROM python:3.13-slim
LABEL org.opencontainers.image.description "A simple API"
ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE ${PORT}

ENV WORKDIR=/work
RUN mkdir ${WORKDIR}

# Set the working directory in the container
WORKDIR ${WORKDIR}

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy necessary files
COPY main.py /usr/local/bin

# Run the script when the container launches
ENTRYPOINT ["python", "/usr/local/bin/main.py"]
