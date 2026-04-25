import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")
API_KEY=os.getenv("API_KEY")
CHANNEL_HANDLE="MrBeast"
maxResults=50
url=f"https://youtube.googleapis.com/youtube/v3/channels?part=ContentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}"



def get_playlist_id():
    try:
        res=requests.get(url)
        data=res.json()
        res.raise_for_status()
        channel_items=data["items"][0]
        # print(json.dumps(channel_items,indent=4))
        channel_playlist_id=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        # print(channel_playlist_id)
        
        return channel_playlist_id
    except requests.exceptions.RequestException as  e:
        raise e
    


def get_video_ids(playlist_id):
    base_url= f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlist_id}&key={API_KEY}"
    pageToken=None
    video_ids=[]
    
    try:
        while True:
            url=base_url
            if pageToken:
                url+=f"&pageToken={pageToken}"
            # print(pageToken)
            res=requests.get(url)
            data=res.json()
            # print(json.dumps(data,indent=4))
            allVideos=data.get("items",[]) #iske andar contentDetails karke property inside which we are hacing our videoId which is required right now
            # print(allVideos)
            for items in allVideos:
                video_ids.append(items["contentDetails"]["videoId"])
            
            pageToken=data.get("nextPageToken")
            #when we are using the data["nextpageToken"] directly it will produce error because when it does not have such property what is python going to return to us hence when we dont know whther such property is even present or not then we are going to use .get() method directly. 
            
            if  pageToken is None:
                break


        print(len(video_ids))
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e


def extracted_video_data(all_videos):
    extracted_data=[]
    
    def batch_list(video_id_list,batch_size):
        for video_id in range(0,len(video_id_list),batch_size):
            yield video_id_list[video_id:video_id+batch_size]

    try:
        for batch in batch_list(all_videos,maxResults):
            video_ids_string=",".join(batch)
            url=f"https://youtube.googleapis.com/youtube/v3/videos?part=ContentDetails&part=snippet&part=statistics&id={video_ids_string}&key={API_KEY}"
            res=requests.get(url)
            res.raise_for_status()
            data=res.json()
            for items in data.get("items",[]):
                video_id=items["id"]
                snippet=items["snippet"]
                contentDetails=items["contentDetails"]
                statistics=items["statistics"]

                video_data={
                    "video_id":video_id,
                    "title":snippet["title"],
                    "publishedAt":snippet["publishedAt"],
                    "duration":contentDetails["duration"],
                    "viewCount":statistics.get("viewCount",None),
                    "likeCount":statistics.get("likeCount",None),
                    "commentCount":statistics.get("commentCount",None)
                }
                extracted_data.append(video_data)
                
        
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e


if __name__=="__main__":
    playlist_id=get_playlist_id()
    videos_ids=get_video_ids(playlist_id)
    extracted_video_data(videos_ids)

    