# Python Asynchronous REST API Sample
Implementation of a generic Python asynchronous REST API without external dependencies

## Sample
Start a job in the background and return the job id:
```
curl -X POST \
  'http://127.0.0.1:8000/asyncservice' \
  --data-raw 'An input in whatever format'

Output:
{"id": "19641567-6b67-4344-8aa9-7bb76ba3a21e"}
```

Retrieve the job results:
```
curl -X GET \
  '127.0.0.1:8000/asyncservice?id=19641567-6b67-4344-8aa9-7bb76ba3a21e'

Output:
Sample
```