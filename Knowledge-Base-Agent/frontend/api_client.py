import os
import requests

BASE_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

TIMEOUT = 10


def _request(method, endpoint, **kwargs):
    url = f"{BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    try:
        response = requests.request(
            method,
            url,
            timeout=TIMEOUT,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.Timeout:
        raise RuntimeError("Backend request timed out.")

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Backend is not running at {BASE_URL}"
        )

    except requests.exceptions.HTTPError as exc:
        raise RuntimeError(
            f"HTTP {exc.response.status_code}: "
            f"{exc.response.text[:300]}"
        )

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(f"Request failed: {exc}")

    except ValueError:
        raise RuntimeError("Backend returned invalid JSON.")


def health_check():
    return _request("GET", "/")


def search_articles(question):
    return _request(
        "POST",
        "/search",
        json={"question": question}
    )


def get_similar_queries():
    return _request("GET", "/similar-queries")


def get_article_audit():
    return _request("GET", "/article-audit")


def get_recommendations(question):
    return _request(
        "POST",
        "/recommendations",
        json={"question": question}
    )
