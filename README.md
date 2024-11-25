# fraud-detection-system

## Setup a Python Virtual Environment

```
# creating and activating virtual environment (Linux/MacOS)
python3 -m venv .venv
source .venv/bin/activate

# creating and activating virtual environment (Windows)
python3 -m venv .venv
.venv\Scripts\Activate.ps1

# installing project requirements
pip install -r requirements.txt
```

## Run MongoDB

If you do not have a Docker container with MongoDB:

```
docker container run --name mongodb -d -p 27017:27017 mongo
```

Otherwise, start the Docker container with MongoDB:

```
docker container start mongodb
```

## Run the Application Server

```
python -m uvicorn mongodb.src.server:app --reload
```
