# Base image
FROM nanthakps/kpsmlx:heroku_v2

# Set working directory
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# Install dependencies
RUN apt update && apt install -y ffmpeg aria2

# Copy requirements and install
COPY requirements.txt .
RUN pip3 install --upgrade setuptools
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip install yt-dlp

# Ensure README.md exists to prevent startup errors
RUN [ -f README.md ] || touch README.md

# Copy all other files
COPY . .

# Start the bot
CMD ["bash", "start.sh"]
