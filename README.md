# get-cookie

Retrieves raw cookie values from a URL using a headless Chromium browser. Handles JavaScript-rendered cookies and bot challenges.

## Usage

### Docker

```bash
docker build -t get-cookie .
docker run --rm get-cookie <url>
```

### Local

```bash
pip install playwright && playwright install chromium
python retriever.py <url>
```

### Output

Prints cookies to stdout as a raw header string:

```
session=abc123; csrf=xyz456
```

Errors are written to stderr with exit code 1.

## Requirements

- Docker, **or**
- Python 3.8+ with `playwright` and Chromium
