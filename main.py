import requests
import json


def fetch_item(item_id):
    url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
    response = requests.get(url)
    return response.json()


def fetch_comments(item_id):
    item = fetch_item(item_id)
    if item is None or "kids" not in item:
        return []

    comments = []
    for comment_id in item["kids"]:
        comment = fetch_item(comment_id)
        if comment and comment["type"] == "comment":
            comments.append(
                {
                    "id": comment["id"],
                    "author": comment.get("by", ""),
                    "time": comment.get("time", 0),
                    "text": comment.get("text", ""),
                    "kids": fetch_comments(comment["id"]),
                }
            )
    return comments


def save_comments_to_json(item_id, filename):
    comments = fetch_comments(item_id)
    with open(filename, "w") as file:
        json.dump(comments, file, indent=2)


if __name__ == "__main__":
    # Replace 'POST_ID' with the ID of the post you want to fetch comments for
    post_id = "POST_ID"
    output_filename = f"comments_for_post_{post_id}.json"
    save_comments_to_json(post_id, output_filename)
