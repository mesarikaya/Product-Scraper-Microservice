#	Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START docker]

# The Google App Engine python runtime is Debian Jessie with Python installed
# and various os-level packages to allow installation of popular Python
# libraries. The source is on github at:
# https://github.com/GoogleCloudPlatform/python-docker


FROM gcr.io/google_appengine/python

# Create a virtualenv for the application dependencies.
# # If you want to use Python 2, use the -p python2.7 flag.

# Update
RUN apt-get update --fix-missing
RUN apt-get -y upgrade --fix-missing

RUN virtualenv -p python3 /env
ENV PATH /env/bin:$PATH

ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install --upgrade pip && /env/bin/pip install -r /app/requirements.txt
ADD . /app

RUN apt-get install -y curl
RUN apt-get install -y unzip

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# Copy everything to Docker
COPY ./ ./

# Install chromium instead
#RUN apt-get install -y chromium-browser

# Install chromedriver for Chromium
#RUN curl https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip -o /usr/local/bin/chromedriver.zip
#RUN unzip /usr/local/bin/chromedriver.zip -d /usr/local/bin/
#RUN chmod +x /usr/local/bin/chromedriver || rm /usr/local/bin/chromedriver.zip


#install python dependencies
#download and install chrome
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

CMD ["./background_task.sh"]
# CMD gunicorn --workers=3 app.wsgi -b 0.0.0.0:8080
# [END docker]
