from googleapiclient.discovery import build
import json

try:
	with open('./keys.txt', mode='r') as my_file:
		YT_API_KEY=my_file.read().split('=')[1]
except FileNotFoundError as e:
	print('File does not exist')

youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

def get_video_details(video_ID):
	request = youtube.videos().list(
		part='snippet, statistics',
		fields='items(kind, id, snippet(title, description, thumbnails, channelTitle), statistics)',
		id=video_ID)
	response = request.execute()
	return response


video_URL = input("Enter your video URL: ")
video_ID = video_URL.split("=")[-1]
details = get_video_details(video_ID)

try:
	items = details['items']	# this throws a key error if it cannot find items

	if items:
		for item in items:
			kind = item['kind']
			video_id = item['id']
			channel_title = item['snippet']['channelTitle']
			title = item['snippet']['title']
			description = item['snippet']['description']
			viewers = item['statistics']['viewCount']
			likes = item['statistics']['likeCount']
			comments = item['statistics']['commentCount']
			print(f"\n[+] {title}\n")
			print(f"Type: {kind}\t" + "|\t" + f"ID: {video_id} \t" + "|\t" + f"Channel Title: {channel_title}")
			print("-"*90)
			print(f"Viewers: {viewers}\t" + "|\t" + f"Likes: {likes}	\t" + "|\t" + f"Comments: {comments}")
			print(f"\n[-] Description:\n\t|{description.replace("\n", "\n\t|")}\n")

	else:
		print("No video details found.")

except KeyError as e:
	print(f"Missing items key: {e}")
except Exception as e:
	print(f"Something failed: {e}")
