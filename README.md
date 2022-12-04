# GroupChat

```
This is an API application related to groupchat where admin can create users, users can create groups, add users to group etc..
```

# Application Setup

```

# To creating virtual environment
virtualenv -p python3 env

# Activate env
source env/bin/activate

# To Install required packages
pip install -r requirement.txt

# To create table schema
python manage.py migrate


```

## To Run Django server / Application

```
python manage.py runserver

```


## Create Superuser
```
# Create superuser using below command
python manage.py createsuperuser

```

## To Run test cases

```
# To run coverage 
coverage run manage.py test

# To check coverage report
coverage report -m --omit="*/env/*"

```