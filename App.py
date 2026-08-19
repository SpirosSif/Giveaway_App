import streamlit as st
import src.insta_api as insta_api
import src.brightdata_api as brightdata_api

URL = st.text_input("Insta URL")

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

st.button("Submit", type="primary")

#python -m streamlit run app.py