import requests
import json
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def fetch_item(item_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url)
    return response.json()


def fetch_comment_recursive(comment_id):
    comment = fetch_item(comment_id)
    if comment and comment["type"] == "comment":
        return {
            "id": comment["id"],
            "author": comment.get("by", ""),
            "time": comment.get("time", 0),
            "text": comment.get("text", ""),
            "kids": fetch_comments(comment["id"]),
        }
    return None


def fetch_comments(item_id):
    item = fetch_item(item_id)
    if item is None or "kids" not in item:
        return []

    comments = []
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(fetch_comment_recursive, comment_id)
            for comment_id in item["kids"]
        ]
        for future in futures:
            comment = future.result()
            if comment:
                comments.append(comment)

    return comments


def save_comments_to_json(item_id, filename):
    comments = fetch_comments(item_id)
    with open(filename, "w") as file:
        json.dump(comments, file, indent=2)


if __name__ == "__main__":
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description="Fetch and save comments from Hacker News API."
    )
    parser.add_argument(
        "post_id", type=int, help="ID of the post to fetch comments for"
    )
    args = parser.parse_args()

    post_id = args.post_id
    output_filename = f"comments_for_post_{post_id}.json"

    logging.info(f"Starting script for post_id: {post_id}")

    try:
        save_comments_to_json(post_id, output_filename)
        logging.info(f"Comments for post_id {post_id} saved to {output_filename}")
    except Exception as e:
        logging.error(f"Error occurred: {e}")
