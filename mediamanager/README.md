# Media manager service

Consumes download video request from other service, pull new ones from YouTube and store audio to drive, 
put video information to database. 

## Build

```commandline
docker build -t volunteer-prb/podcasts-api-mediamanager .
```

## Running

#### Local
```commandline
export DOWNLOAD_PATH=<parent_path_to_save_files>
export DATABASE_URI=<database connection string, e.g. postgresql://postgres:qwerty@localhost/youtube_podcasts>
celery --app=app.downloader --broker=redis://localhost worker --loglevel=INFO -Q media_manager_tasks
```

#### In docker 
```commandline
docker run -e DOWNLOAD_PATH=<parent_path_to_save_files> \
  -e DATABASE_URI=<database connection string, e.g. postgresql://postgres:qwerty@localhost/youtube_podcasts>
  -e BROKER_URL=<redis_host> \
  --name publisher --rm \
  volunteer-prb/podcasts-api-mediamanager
```

## Examples

#### With objects class
```python
from app.downloader import download
from app.objects.download_task import DownloadTask

# Note that must exists channel with id UC7Elc-kLydl-NAV4g204pDQ in table 
# source_channels before execute
task = DownloadTask(
    url='https://www.youtube.com/shorts/KBOny-tYdNQ',
    channel_id='UC7Elc-kLydl-NAV4g204pDQ',
)

download.delay(task)
```
