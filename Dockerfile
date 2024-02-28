# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, pip, Git, and the default SQLite version
RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    git \
    libsqlite3-dev \
&& rm -rf /var/lib/apt/lists/*

# Set Python 3.8 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1

# Clone your Django project from the Git repository
RUN git clone https://github.com/usubioinfo/hucovaria.git /project

# Install Django 3.2.12 and any other requirements
WORKDIR /project

#RUN pip3 install -r hucovaria/requirements.txt
RUN pip3 install Django==3.2.12 pandas==1.3.3

# Step 1: Comment urlpatterns in urls.py and uncomment the empty list
RUN sed -i '/^[\t]*path/s/^/# /' main/urls.py

# Step 2: Comment out code in views.py after imports
RUN sed -i '/from .models import */{n;:a;n;s/^/# /;ba}' main/views.py

# Step 3: Run Django migrations
RUN python3 manage.py migrate

# Step 4: Revert changes in urls.py and views.py
RUN sed -i 's/^[[:space:]]*#[[:space:]]*\(path\)/\1/' main/urls.py
RUN sed -i '/from .models import */{n;:a;n;s/^# //;ta;b;:a;n;s/^# //;ba}' main/views.py

# Command to run the Django development server on port 9018
CMD ["python3", "manage.py", "runserver", "0.0.0.0:9018"]
