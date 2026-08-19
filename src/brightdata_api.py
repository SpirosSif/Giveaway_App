import requests
import dotenv
import json
import time


def get_instagram_comments(post_url):
    api_token = dotenv.get_key(".env", "BRIGHTDATA_API_TOKEN")

    url = "https://api.brightdata.com/datasets/v3/scrape"

    headers= {
         "Authorization": f"Bearer {api_token}",
         "Content-Type": "application/json"
    }

    params = {
        "dataset_id": "gd_ltppn085pokosxh13",
        "include_errors": "true"
    }

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": [
            {
                "url": post_url
            }
        ]
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=payload
    )

    response.raise_for_status()
    if response.status_code==200:
        comments = []
        errors = []
        for line in response.text.splitlines():
            if not line.strip():
                    continue
            item=json.loads(line)
            if "error" in item:
                errors.append(item)
            else:
                comments.append(item)
        if errors and not comments:
                raise RuntimeError(f"Bright Data failed: {errors[0].get('error')}")
        save_comments(comments)
        return comments
    
    if response.status_code == 202:

        response_data = response.json()

        snapshot_id = response_data["snapshot_id"]

        print("Snapshot ID:", snapshot_id)

        comments = wait_for_snapshot(
            snapshot_id,
            api_token
        )

        save_comments(comments)

        return comments

    return []

def wait_for_snapshot(snapshot_id, api_token):

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    progress_url = (
        f"https://api.brightdata.com/"
        f"datasets/v3/progress/{snapshot_id}"
    )

    while True:

        response = requests.get(
            progress_url,
            headers=headers
        )

        response.raise_for_status()

        progress_data = response.json()

        status = progress_data["status"]

        print("Bright Data status:", status)

        if status == "ready":
            break

        if status in ["failed", "canceled"]:
            raise RuntimeError(
                f"Bright Data job ended with status: {status}"
            )

        time.sleep(5)

    return download_snapshot(
        snapshot_id,
        api_token
    )

def download_snapshot(snapshot_id, api_token):

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    url = (
        f"https://api.brightdata.com/"
        f"datasets/v3/snapshot/{snapshot_id}"
    )

    response = requests.get(
        url,
        headers=headers,
        params={
            "format": "json"
        }
    )

    response.raise_for_status()

    return response.json()

def save_comments(comments):

    with open(
        "data/comments.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            comments,
            file,
            indent=4,
            ensure_ascii=False
        )