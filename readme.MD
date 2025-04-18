# Realtime Chat Application
## Tech stack
1. Python, django
2. Django channels daphne, 
3. Redis


## Installation steps
1. Create virtual environment  
```bash
    python -m venv <env> 
```
2. Activate virtual environment   

for windows
```bash
    env\Scripts\activate
```
for mac/linux  
```bash
    source env/bin/activate
```
3. Install requirements.txt
```bash
    pip install -r requirements.txt
```
4. Install redis  

for linux
```zsh
    sudo apt update
    sudo apt install redis
    redis-server
    sudo systemctl enable redis
    sudo systemctl start redis
```
for macos
```zsh
    brew install redis
    brew services start redis
    redis-cli ping
    #return pong
    
```


5. Run the django application
```bash
    python manage.py makemigrations
```
```bash
    python manage.py migrate
```
```bash
    python manage.py runserver
```

5. Open the server with port in your local machine
```zsh
    http://localhost:8000
```

```zsh
    http://127.0.0.1:8000
```
access other device with same network
```zsh
    http://0.0.0.0:8000
```
open this app other device 
```zsh
    http://192.1.1.6:8000
```
or
```zsh
    http://<ip_adress>:8000
```