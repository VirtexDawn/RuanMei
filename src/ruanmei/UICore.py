from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()
AppName = os.getenv("APPNAME")

Components = {}


def CreateApp():
    global Components

    HideDeploy = """
        <style>
        .stAppDeployButton {
            visibility: hidden;
        }
        </style>
    """
    st.markdown(HideDeploy, unsafe_allow_html=True)

    st.title(str(AppName))
    Components["UserSearchBar"] = st.text_input(
        "User Name / Display Name Roblox"
    )
    Components["SearchButton"] = st.button("Search")

    scroll_frame = st.container(height=300)

    if Components["SearchButton"]:
        with scroll_frame:
            st.write(f"Hasil pencarian untuk: **{Components['UserSearchBar']}**")
            for i in range(1, 20):
                st.write(f"Item #{i}: Data dummy Roblox user detail")