## How to run automation tests

### 1. Clone the repository
```python
git clone https://github.com/gmngit/Automation_UI.git
```

### 2. Build image "server"
```python
docker build -t server ./src/server
```

### 3. Download standalone-chrome image
```python
docker pull selenium/standalone-chrome
```

### 4. Build image "tests"
```python
docker build -t tests .
```

### 5. Build image "allure"
```python
docker build -t allure ./allure
```

### 6. Run web server container
```python
docker compose up -d webserver
```

### 7. Run selenium-chrome container
```python
docker compose up -d selenium-chrome
```

### 8. Run tests container
```python
docker compose up automation-tests
```

### 9. Run allure container
```python
docker compose up -d allure-report
```

### 10. Open allure report in browser
```python
http://localhost:8080
```

### 11. Clean containers
```python
docker compose down
```