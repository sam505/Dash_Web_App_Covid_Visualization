FROM python:3.8

# Copy local code to the container image
ENV APP_HOME /app
WORKDIR ${APP_HOME}
COPY . ./

# Install dependecies in the requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

CMD python app.py