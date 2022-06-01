# Youtube podcasts backend

## Build

*todo*

## Running

### Local

#### Web API
```commandline
export FLASK_APP=app
export DATABASE_URI=postgresql://postgres:qwerty@localhost/youtube_podcasts
flask run
```

#### Celery workers
```commandline
export BASE_URL=https://0000-000-00-00-00.eu.ngrok.io
celery -A app worker
```

## Environment

* `DATABASE_URI` database connection string (default is `sqlite:///db.sqlite`)
* `BASE_URL` base url for PubSubHubbub subscription (must be allowed to access from Internet)

## Web API

### Common

REST endpoints return wrapped results. When an API call is successful, the result
object is used as a simple envelope for the results, using the data key, as in the
following:

```json
{
  "status": "success",
  "data": {}
}
```

When an API call is rejected due to invalid data or call conditions, or call fails
due to an error on the server, the result object message key describe what's happend.
For example:

```json
{
  "status": "error",
  "message": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
}
```

### Pagination

REST endpoints supported pagination accept URL Query attributes `page` (default is 1) and `per_page` (default is 20),
e.g. URL query: `http://<host>/<endpoint>?page=2&per_page=10`.

Return response (data section):

```json
{
  "pagination": {
    "has_next": true,
    "next_num": 15,
    "has_prev": true,
    "prev_num": 13,
    "page": 14,
    "page_range": [
      9,
      10,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      19
    ]
  },
  "items": []
}
```

* `has_next`: has next page (`true` or `false`)
* `next_num`: next page number (`int` or `null`)
* `has_prev`: has previous page (`true` or `false`)
* `prev_num`: previous page number (`int` or `null`)
* `page`: current page number (`int`)
* `page_range`: list of available pages (by default 5 pages left and 5 pages right of current page)
* `items`: list of objects in current page

### Filtering

REST endpoints supported filtering accept URL Query attributes starts with `filter_by_`.
Pass field name and filtering modifier split by two underlines after prefix.

Nested filters allowed, split child field from parent with two underline.

| Filtering modifier | Meaning                         |
|--------------------|---------------------------------|
| `__gte`            | greater or equal                |
| `__gt`             | strict greater                  |
| `__lt`             | strict lower                    |
| `__lte`            | lower or equal                  |
| `__neq` or `__ne`  | not equal                       |
| `__like`           | pattern search                  |
| `__like`           | case insensitive pattern search |
| `__ieq`            | case insensitive equal          |
| `__eq` or empty    | strict equal                    |

Examples:
* Select 20 items at page 1 contains word "popular" (case insensitive) in title:
  `http://localhost:5000/channels/find?page=1&per_page=20&filter_by_title__ilike=%popular%`

