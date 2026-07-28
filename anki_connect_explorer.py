# /// script
# requires-python = ">=3.13"
# dependencies = ["requests", "ipython"]
# ///
from datetime import datetime
import requests

import IPython


def invoke(action, **params):
    data = {"action": action, "version": 6}
    if params:
        data["params"] = params
    r = requests.post("http://127.0.0.1:8765", json=data)
    return r.json()


def getReviewsOfCards(*card_ids):
    return invoke("getReviewsOfCards", cards=card_ids)["result"]


def show_review_times_for_cards(*card_ids):
    res = getReviewsOfCards(*card_ids)
    for card_id, reviews in res.items():
        print(f"{card_id}:")
        for review in reviews:
            dt = datetime.fromtimestamp(review["id"] / 1000)
            print(f"  {dt.isoformat()}, last interval: {review['lastIvl']}, interval: {review['ivl']}")


if __name__ == "__main__":
    IPython.embed(colors="Neutral")
