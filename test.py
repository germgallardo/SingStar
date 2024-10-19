from googleapiclient.discovery import build

try:
	with open('./keys.txt', mode='r') as my_file:
		YT_API_KEY=my_file.read().split('=')[1]
		print(YT_API_KEY)
except FileNotFoundError as e:
	print('File does not exist')

youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

def get_video_details(video_ID):
    request = youtube.videos().list(part='snippet,statistics', id=video_ID)
    response = request.execute()
    return response

video_URL = 'https://www.youtube.com/watch?v=L8HxKTty1WU'
video_ID = video_URL.split("=")[-1]
print(video_ID)
details = get_video_details(video_ID)
print(details)