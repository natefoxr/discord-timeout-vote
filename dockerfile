# Use an official Python runtime as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system dependencies for FFmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir discord.py>=2.0.0 pynacl python-dotenv

# Define environment variables
# Place your Discord bot token here or set it through Docker run
# ENV DISCORD_TOKEN=your_token_here

# Set the entry point to start the bot
CMD ["python", "bot.py"]
