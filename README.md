## Installation

Clone this repository.

```bash
1.	git clone https://github.com/dev-rathankumar/fashion-dev.git .
```
```bash
2.	pipenv shell
```
```bash
3.	pipenv install
```
```bash
4.	create new postgres database
```
```bash
5.	rename .env-sample to .env and fill up the required credentials
```
```bash
6.	deactivate and reactivate pipenv ("exit" and "pipenv shell")
```
```bash
7.	python manage.py migrate
```
```bash
8.	python manage.py loaddata db-dump.json
```



## Logins

```python

# Superuser
http://127.0.0.1:8000/admin/
appzone.biz@gmail.com
qWerty@123

# Business
http://127.0.0.1:8000/en/userLogin/
business@appzoneit.com
qWerty@123

```