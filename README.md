# Instagram Giveaway Picker

A Python / Streamlit application for collecting, filtering and selecting valid participants from an Instagram giveaway.

The project was initially created for the **4 hit** Instagram giveaway, but it can be adapted for other Instagram giveaways by changing the relevant configuration values.

## Features

- Accepts an Instagram post URL
- Verifies Instagram media information
- Collects comments through Bright Data
- Saves the raw comments locally
- Filters duplicate participants
- Checks giveaway-specific participation requirements
- Creates a clean list of eligible usernames
- Can be extended with a random giveaway winner selection system

---

## Project Structure

```text
Giveaway_App/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
├── .gitignore
│
├── data/
│   ├── comments.json
│   └── solo_users.json
│
└── src/
    ├── __init__.py
    ├── insta_api.py
    ├── brightdata_api.py
    └── filtering_comments.py
Files

app.py
Main Streamlit application.

src/insta_api.py
Handles communication with the Instagram / Meta API and retrieves information about the Instagram account and media.

src/brightdata_api.py
Collects Instagram comments through the Bright Data API.

src/filtering_comments.py
Processes the downloaded comments and removes invalid or duplicate entries according to the giveaway rules.

data/comments.json
Contains the raw comments retrieved from Instagram.

data/solo_users.json
Contains the filtered giveaway participants.

Requirements

You need:

Python 3
pip
A Meta / Instagram API access token
A Bright Data API token
Installation
1. Clone the repository
git clone YOUR_REPOSITORY_URL

Then enter the project directory:

cd Giveaway_App
2. Optional: Create a virtual environment

Windows:

python -m venv .venv

Activate it:

.venv\Scripts\activate

macOS / Linux:

python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies

Run:

pip install -r requirements.txt

The project currently uses packages such as:

streamlit
requests
python-dotenv
Environment Variables

Create a file named:

.env

inside the root directory of the project.

It should contain:

INSTA_ACCESS_TOKEN=YOUR_INSTAGRAM_ACCESS_TOKEN
BRIGHTDATA_API_TOKEN=YOUR_BRIGHTDATA_API_TOKEN

Do not upload the .env file to GitHub.

The project should include .env in .gitignore.

Example:

.env
.venv/
__pycache__/
data/

You can also create a safe .env.example file:

INSTA_ACCESS_TOKEN=
BRIGHTDATA_API_TOKEN=

This tells other developers which environment variables are required without exposing the actual tokens.

Before Running the Application

Make sure the following directory exists:

data/

The application uses this directory to store downloaded and filtered giveaway data.

For example:

data/comments.json
data/solo_users.json

These files may contain Instagram usernames and comment information and therefore should normally not be committed to a public repository.

Running the Application

From the root directory:

Giveaway_App/

run:

python -m streamlit run app.py

or, depending on your Python installation:

python3 -m streamlit run app.py

Streamlit will provide a local address, usually similar to:

http://localhost:8501

Open it in your browser.

How It Works

The basic flow of the application is:

Instagram Post URL
        ↓
Instagram / Meta API
        ↓
Media verification
        ↓
Bright Data
        ↓
Download comments
        ↓
data/comments.json
        ↓
Filtering
        ↓
data/solo_users.json
        ↓
Eligible participants
        ↓
Winner selection
Instagram Post Shortcode

Every Instagram post or Reel has a unique shortcode.

For example:

https://www.instagram.com/p/Db_KRwuCDyE/

The shortcode is:

Db_KRwuCDyE

For a Reel:

https://www.instagram.com/reel/Dbvttt7Im8J/

the shortcode is:

Dbvttt7Im8J

The application can extract the shortcode from the submitted URL using:

clear_URL = URL.split("?")[0]
shortcode = clear_URL.rstrip("/").split("/")[-1]
Using the Project for Another Giveaway

If you want to reuse this project for another Instagram giveaway, several values may need to be changed.

1. Instagram Post

Use the URL of the new giveaway post in the Streamlit application.

If a shortcode is currently hardcoded anywhere in the project, for example:

post_id = insta_api.get_insta_data_by_shortcode(
    insta_data["user_id"],
    "Db_KRwuCDyE"
)

replace:

Db_KRwuCDyE

with the shortcode of the new Instagram post.

Preferably, use the shortcode extracted automatically from the entered URL:

post_id = insta_api.get_insta_data_by_shortcode(
    insta_data["user_id"],
    shortcode
)

This way the source code does not need to be modified for every giveaway.

2. Giveaway Rules

The filtering logic is located in:

src/filtering_comments.py

The original giveaway rules were based on:

One entry per Instagram account
The participant must tag the required number of users
Only comments submitted before the giveaway deadline are accepted

If another giveaway has different rules, modify the filtering conditions inside this file.

For example, if the giveaway requires exactly two tagged users:

if len(i.get("tagged_users_in_comment", [])) == 2:

If another giveaway requires three users:

if len(i.get("tagged_users_in_comment", [])) == 3:
3. Giveaway Deadline

If the filtering code contains a hardcoded deadline, update it for the new giveaway.

For example:

"2026-08-20T14:00:00.000Z"

represents the UTC equivalent of the original giveaway deadline.

For reusable projects, it is recommended to eventually move values such as:

GIVEAWAY_DEADLINE
REQUIRED_TAGS

into a configuration file or environment variables rather than keeping them hardcoded.

Comment Data

The raw Bright Data output is stored in:

data/comments.json

A comment may contain information such as:

{
    "comment_user": "example_user",
    "comment_date": "2026-08-18T12:19:33.000Z",
    "comment": "@friend1 @friend2",
    "tagged_users_in_comment": [
        "@friend1",
        "@friend2"
    ],
    "comment_id": "123456789"
}

The exact fields available depend on the data returned by the scraper.

Duplicate Participants

The giveaway allows one entry per Instagram account.

To prevent duplicate entries, the filtering script keeps track of usernames that have already been accepted.

Example:

seen_users = set()

Then:

if i["comment_user"] in seen_users:
    continue

Once a participant is accepted:

seen_users.add(i["comment_user"])

This prevents multiple comments from the same account from creating multiple giveaway entries.

Running the Filtering Script Separately

The filtering script can also be executed without running Streamlit.

From the project root:

python src/filtering_comments.py

or:

python3 src/filtering_comments.py

Do not run it from inside the src directory if the script uses paths such as:

data/comments.json

The working directory should be:

Giveaway_App/

and not:

Giveaway_App/src/
Character Encoding

Instagram comments may contain:

Greek characters
accented characters
emojis
special symbols

For this reason JSON files should always be opened using UTF-8.

Example:

with open(
    "data/comments.json",
    "r",
    encoding="utf-8"
) as file:
    data = json.load(file)

When writing JSON:

json.dump(
    data,
    file,
    indent=4,
    ensure_ascii=False
)
Bright Data

Bright Data is used to retrieve Instagram comments.

The API token is loaded from:

BRIGHTDATA_API_TOKEN=

The scraper may return the results immediately or may return a snapshot_id while the scraping job is still processing.

The application handles this by:

Starting the scraping request
Receiving a snapshot ID when necessary
Checking the snapshot status
Downloading the results once they are ready
Saving them to:
data/comments.json

Avoid repeatedly running the scraper while developing the filtering logic.

Once comments.json has been downloaded successfully, filtering and testing can be performed locally without consuming additional scraping/API usage.

Instagram / Meta API

The Instagram access token is stored in:

INSTA_ACCESS_TOKEN=

The Meta / Instagram API is used to identify the connected Instagram account and locate the requested media.

The project currently uses media information such as:

id
permalink
media_type
comments_count
Security

Never commit API tokens.

Make sure .gitignore contains:

.env

Before pushing the repository, also check that no token has accidentally been written directly inside:

app.py
src/insta_api.py
src/brightdata_api.py

Do not publish raw Instagram participant data unless necessary.

For a public GitHub repository, it is recommended to ignore:

data/

and provide example / anonymized JSON data instead.

Example .gitignore
# Environment variables
.env

# Virtual environments
.venv/
venv/

# Python cache
__pycache__/
*.pyc

# Giveaway participant data
data/

# IDE / OS files
.vscode/
.idea/
.DS_Store
Thumbs.db
Development Notes

During development, API calls should be kept separate from filtering logic.

A recommended workflow is:

1. Download comments once
2. Save comments.json
3. Develop and test filtering locally
4. Verify filtered participants
5. Run the winner selection

This avoids unnecessary API requests and makes debugging much easier.

Disclaimer

This project is an independent giveaway utility.

It is not affiliated with, endorsed by, sponsored by, or officially connected to Instagram, Meta or Bright Data.

Anyone reusing this project is responsible for complying with:

Instagram / Meta platform rules
API provider terms
local giveaway regulations
applicable privacy and data protection requirements
Author

Created as part of the 4 hit content creation project.

Built with Python and Streamlit.


Θα έκανα όμως **2 μικρές αλλαγές πριν το ανεβάσεις στο GitHub**:

1. Μην ανεβάσεις το πραγματικό `data/comments.json`, γιατί περιέχει πραγματικά Instagram usernames/comments.
2. Αντί γι' αυτό, μπορείς αργότερα να βάλεις:
   ```text
   example_data/sample_comments.json