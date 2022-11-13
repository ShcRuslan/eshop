# EShop

This project was made by me to create a store application

# Technologies Used

+ Python
+ Django
+ Django Rest Framework

# Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

Download this repository

## Installing

Go to the folder where the main course folder is located. Next, in this folder, create a virtual environment.

```
python3 -m venv env
source env/bin/activate
```

Now that we're inside a virtual environment, we can install our package requirements.

```
pip install -r requirements.txt
```

# Usage

Go to the shop folder and enter

```
python manage.py makemigrations

python manage.py migrate

python manage.py runserver
```

In your web browser enter the address: http://127.0.0.1:8000/courses/

# Versioning

+ Django 4.1.2
+ djangorestframework 3.14.0


# Authors

+ **Shchelokov Ruslan** - *initial work*