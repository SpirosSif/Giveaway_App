import dotenv
import requests
import json

def get_insta_data():
    insta_access_token = dotenv.get_key(".env", "INSTA_ACCESS_TOKEN")
    response = requests.get("https://graph.instagram.com/me", params={"fields": "user_id,username","access_token": insta_access_token})
    print(response.status_code)
    return response.json()

def get_insta_data_by_shortcode(user_id,shortcode):
    insta_access_token = dotenv.get_key(".env", "INSTA_ACCESS_TOKEN")
    media_response=requests.get(f"https://graph.instagram.com/{user_id}/media", params={"fields": "id,permalink,media_type,comments_count","access_token": insta_access_token})
    media_collection=media_response.json()
    for i in media_collection["data"]:
        print(i["permalink"])
        if(f"https://www.instagram.com/p/{shortcode}/"==i["permalink"]): 
            post_id=i["id"]
            post_permalink=i["permalink"]
            post_media_type=i["media_type"]
            post_comment_count=i["comments_count"]
    print(post_id,post_permalink,post_media_type,post_comment_count)
    return {
        "id": post_id,
        "permalink": post_permalink,
        "media_type": post_media_type,
        "comments_count": post_comment_count
    }

#def get_insta_comments(post_id):
    all_comments=[]
    url=f"https://graph.instagram.com/{post_id}/comments"
    while url:
        insta_access_token = dotenv.get_key(".env", "INSTA_ACCESS_TOKEN")
        comments_response=requests.get(url, params={"fields": "id,username,text,timestamp", "access_token": insta_access_token} 
                                       if url == f"https://graph.instagram.com/{post_id}/comments" else None)
        res_data=comments_response.json()
        if "data" in res_data:
            all_comments.extend(res_data["data"])
        url = res_data.get("paging", {}).get("next")

    with open("data/comments.json", "w", encoding="utf-8") as file:
        json.dump(all_comments, file, indent=4, ensure_ascii=False)

#def get_insta_comments(post_id):
    all_comments = []
    url = f"https://graph.instagram.com/{post_id}/comments"
    page = 1

    while url:
        insta_access_token = dotenv.get_key(".env", "INSTA_ACCESS_TOKEN")

        comments_response = requests.get(
            url,
            params={
                "fields": "id,text",
                "access_token": insta_access_token
            } if page == 1 else None
        )

        print("PAGE:", page)
        print("STATUS:", comments_response.status_code)

        res_data = comments_response.json()

        print("COMMENTS THIS PAGE:", len(res_data.get("data", [])))
        print("HAS NEXT:", bool(res_data.get("paging", {}).get("next")))
        print("ERROR:", res_data.get("error"))

        all_comments.extend(res_data.get("data", []))

        url = res_data.get("paging", {}).get("next")
        page += 1

    print("TOTAL COMMENTS:", len(all_comments))