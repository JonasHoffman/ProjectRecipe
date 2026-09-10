import httpx



def fetch_page(url):
    response = httpx.get(
        url,
        follow_redirects=True
    )

    if response.status_code != 200:
        raise Exception(
            f"Request failed: {response.status_code}"
        )

    return response.text
    