import json

def filter_users():
    solo_users=[]
    usernames=[]
    seen_users=set()

    with open("data/comments.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    print(type(data))
    for i in data:
        if i["comment_user"] in seen_users:
            continue
       
        if len(i.get("tagged_users_in_comment", []))==2:
            solo_users.append(i)
            seen_users.add(i["comment_user"])
            usernames.append(i["comment_user"])

    save_comments(solo_users,"duplication_filter")
    save_comments(usernames,"solo_usernames")


def save_comments(comments,file_name):

    with open(
        f"data/{file_name}.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            comments,
            file,
            indent=4,
            ensure_ascii=False
        )

filter_users()
