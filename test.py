from googleapiclient.discovery import build
from termcolor import colored


try:
	with open('./keys.txt', mode='r') as my_file:
		YT_API_KEY=my_file.read().split('=')[1]
except FileNotFoundError as e:
	print('File does not exist')

youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

def get_video(video_ID):
	request = youtube.videos().list(
		part='snippet, statistics',
		fields='items(kind, id, snippet(title, description, thumbnails, channelTitle), statistics)',
		id=video_ID)
	response = request.execute()
	return response


def get_video_information(details):
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
				print(colored(f"\n[+] {title}\n", "green"))
				print(f"Type: {kind}\t" + "|\t" + f"ID: {video_id} \t" + "|\t" + f"Channel Title: {channel_title}")
				print("-"*90)
				print(f"Viewers: {viewers} \t" + "|\t" + f"Likes: {likes}	\t" + "|\t" + f"Comments: {comments}")
				print(colored("\n[-] Description:\n", "light_magenta") + "\t|" + f"{description.replace("\n", "\n\t|")}\n")

		else:
			print("No video details found.")

	except KeyError as e:
		print(f"Missing items key: {e}")
	except Exception as e:
		print(f"Something failed: {e}")

if __name__:
	video_URL = input(colored("\nEnter your video URL: ", "red"))
	video_ID = video_URL.split("=")[-1]
	details = get_video(video_ID)
	get_video_information(details)
