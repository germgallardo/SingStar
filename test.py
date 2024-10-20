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


video_URL = 'https://www.youtube.com/watch?v=L8HxKTty1WU'
video_ID = video_URL.split("=")[-1]
#print(f"Video ID: {video_ID}\n")
details = get_video_details(video_ID)

try:
	items = details['items']	# this throws a key error if it cannot find items
	print(items)
	if items:
		for item in items:
			print(f"[+] {item['snippet']['title']}\n")
			print(f"Type: {item['kind']}\t" + "|\t" + f"ID: {item['id']} \t" + "|\t" + f"Channel Title: {item['snippet']['channelTitle']}")
			print(f"Viewers: {item['statistics']['viewCount']}\t" + "|\t" + f"Likes: {item['statistics']['likeCount']}\t" + "|\t" + f"Comments: {item['statistics']['commentCount']}")
			print(f"Description:\n\t|{item['snippet']['description'].replace("\n", "\n\t|")}")

	else:
		print("No video details found.")

except KeyError as e:
	print(f"Missing items key: {e}")
except Exception as e:
	print(f"Something failed: {e}")
