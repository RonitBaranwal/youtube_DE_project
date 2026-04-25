import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
API_KEY=os.getenv("API_KEY")
CHANNEL_HANDLE="MrBeast"
url=f"https://youtube.googleapis.com/youtube/v3/channels?part=ContentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"



def get_playlist_id():
    try:
        res=requests.get(url)
        data=res.json()
        res.raise_for_status()
        channel_items=data["items"][0]
        # print(json.dumps(channel_items,indent=4))
        channel_playlist_id=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlist_id)
        
        return channel_playlist_id
    except requests.exceptions.RequestException as  e:
        raise e
    

if __name__=="__main__":
    get_playlist_id()

    