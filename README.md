# sysaster-api

## Paths

### `/topics`
#### POST
- **code**
- name
- date
- lat
- lon

#### GET

### `/topics/subscribe`
#### POST
- **token**
- **topic** (code of the topic)

### `/topics/unsubscribe`
#### POST
- **token**
- **topic** (code of the topic)

### `/detections`
#### POST
- **topic** (code)

#### GET

## Running

```
cd modules
sudo GAC_PATH="<path to google application credentials>" GAC_FILE="<name of the google application credentials file>" docker-compose up --build
```
