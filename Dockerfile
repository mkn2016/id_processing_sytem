RUN echo "Starting to build this...yay for PyQt5"
LABEL version="1.0"
LABEL short_description="PyQt5 Student Id Processing System"
MAINTAINER Martin Kibui Ndirangu
LABEL maintainer="m.k.ndirangu@gmail.com"

RUN echo "Making directory for application"
RUN mkdir app
RUN echo "Copying application directory to /usr/share/"
COPY ./app /usr/share/

