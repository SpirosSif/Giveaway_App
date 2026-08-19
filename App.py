import streamlit as st
import src.insta_api as insta_api
import src.brightdata_api as brightdata_api
import json
import secrets
import time

import src.winner_is as winner_py

URL = st.text_input("Insta URL")
if st.button("Submit", type="primary"):
    if(URL==""):
        st.write("Please enter a valid URL")
    else:
        clear_URL=URL.split("?")[0]
        shortcode=clear_URL.split("/")[-2]
        st.write("The Insta URL is", clear_URL)
        st.write("The shortcode Insta URL is", shortcode)

        insta_data=insta_api.get_insta_data()
        print(insta_data)

        post=insta_api.get_insta_data_by_shortcode(insta_data["user_id"],shortcode)

        #insta_api.get_insta_comments(post_id)
        # 3. Fetch comments through Bright Data
        with st.spinner("Fetching comments..."):
            comments = brightdata_api.get_instagram_comments(clear_URL)

        st.write("Comments fetched:", len(comments))

        st.json(comments[:5])

st.divider()

st.subheader("Giveaway Draw")

if st.button("Draw Winner"):
    with open("data/solo_usernames.json","r",encoding="utf-8") as file:
        usernames=json.load(file)
    with open("data/duplication_filter.json","r",encoding="utf-8") as file:
            creds=json.load(file)
    st.write("Total entries:", len(usernames))
    placeholder=st.empty()

    for i in range(60):
        random_username=secrets.choice(usernames)
        placeholder.write(f"@{random_username}")
        time.sleep(0.2)

    winner=winner_py.draw_winner()
    for i in creds:
        if i["comment_user"]==winner:
            winner_text=i["comment"]
            break
    placeholder.success(f"## WINNER @{winner} \n {winner_text}")
#python -m streamlit run app.py