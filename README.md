# Hello, User!

## How to run repo?

### 1. Clonning repo

```
git clone https://github.com/tofickbrodaga/KinopoiskApiDev
```

### 2. Create & run docker container 

```
docker run -d --name movies -p 37891:5432 -e
POSTGRES_DBNAME=test -e POSTGRES_USER=test
-e POSTGRES_PASSWORD=test postgres
```

### 3. Create Free API token in Telegram: @kinopoiskdev_bot

### 4. Create .env file to the directory KinopoiskApiDev and insert into youre token

```
API_KEY="YOURAPIKEYHERE"
```

### 5. Run app

```
cd KinopoiskApiDev
```

```
python3 app.py
```

### 6. Path to the site

```
http://127.0.0.1:5000
```

### *** psql connection

```
psql -h 127.0.0.1 -p 37891 -U test test
```