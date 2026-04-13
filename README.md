# get-cookie

Retrieves raw cookie values from a URL using a headless Chromium browser. Handles JavaScript-rendered cookies and bot challenges. Exposed as a REST API secured with a Bearer token.

## Usage

### Docker

```bash
docker build -t get-cookie .
docker run --rm -e APP_SECRET=your-secret -p 8000:8000 get-cookie
```

### Local

```bash
pip install -r requirements.txt && playwright install chromium
APP_SECRET=your-secret uvicorn app:app --host 0.0.0.0 --port 8000
```

### API

**POST /cookies**

```bash
curl -X POST http://localhost:8000/cookies \
  -H "Authorization: Bearer your-secret" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

Optionally pass `actions` to wait before collecting cookies (e.g. for JS-rendered cookies or bot challenges):

```bash
curl -X POST http://localhost:8000/cookies \
  -H "Authorization: Bearer your-secret" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "actions": [
      {"action": "wait", "value": 5000}
    ]
  }'
```

`value` is the wait duration in milliseconds (defaults to 1000).

Response:

```json
{"cookies": "session=abc123; csrf=xyz456"}
```

Interactive API docs available at `http://localhost:8000/docs`.

### CLI (standalone)

```bash
python retriever.py <url>
```

Prints cookies to stdout as a raw header string. Errors are written to stderr with exit code 1.

## Requirements

- Docker, **or**
- Python 3.8+ with `playwright`, `fastapi`, `uvicorn`, and Chromium
