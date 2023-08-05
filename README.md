# Hacker News Comments Scraper

A Python script to fetch all comments under a post from the Hacker News API and save them to a JSON file.

## Overview

This script uses the [Hacker News API](https://firebase.google.com/docs/reference/rest/database) to retrieve comments recursively for a given post. It utilizes the `requests` library to make HTTP requests and saves the comments in a JSON format.

## Requirements

- Python 3.x
- requests library

## Usage

1. Clone the repository or download the script file.

2. Install the required dependencies using `pip`:

	```bash
	pip install -r requirements.txt
	```

3. Run the script from the command line with the post_id as an argument:

	```bash
	python3 script.py POST_ID
	```

	Replace POST_ID with the ID of the post you want to fetch comments for.

4. The script will fetch all the comments under the specified post and save them to a JSON file named comments_for_post_POST_ID.json, where POST_ID is replaced with the actual post ID.

## Disclaimer

This script is for educational and personal use only. Use it responsibly and adhere to the terms and conditions of the Hacker News API.

