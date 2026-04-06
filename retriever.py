import sys
from playwright.sync_api import sync_playwright


def retrieve_cookies(url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        cookies = context.cookies()
        browser.close()

    return "; ".join(f"{c['name']}={c['value']}" for c in cookies)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: retriever.py <url>", file=sys.stderr)
        sys.exit(1)

    try:
        print(retrieve_cookies(sys.argv[1]))
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)
