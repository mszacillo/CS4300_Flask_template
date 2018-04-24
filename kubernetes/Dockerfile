#Read from Ubuntu Base Image
FROM python:2.7
RUN mkdir -p /service
# Copy over all the files of interest
ADD app /service/app
ADD app.py /service/app.py
ADD config.py /service/config.py
ADD manage.py /service/manage.py
ADD requirements.txt /service/requirements.txt
ADD LyricsGenius /service/LyricsGenius
ADD SearchTest.py /service/SearchTest.py
ADD data.json /service/data.json
WORKDIR /service/
RUN pip install -r requirements.txt
CMD python -u app.py $APP_SETTINGS $DATABASE_URL
