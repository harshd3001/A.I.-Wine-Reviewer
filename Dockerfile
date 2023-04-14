# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python -c "import nltk; nltk.download('vader_lexicon', download_dir='/usr/local/share/nltk_data')"

# Make port 5000 available to the world outside this container
EXPOSE 5000

# docker build -t harsh3001/wine-reviewer:0.0.1.RELEASE .
# docker run -p 5000:5000 harsh3001/wine-reviewer:0.0.1.RELEASE
# Run app.py when the container launches
CMD ["python", "api.py"]