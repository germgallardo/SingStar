from googleapiclient.discovery import build
from termcolor import colored
import os


try:
	with open('./keys.txt', mode='r') as my_file:
		YT_API_KEY=my_file.read().split('=')[1]
except FileNotFoundError as e:
	print('File does not exist. Key cannot be retrieved.')


youtube = build('youtube', 'v3', developerKey=YT_API_KEY)


def get_video(video_ID):
	request = youtube.videos().list(
		part='snippet, contentDetails, statistics',
		fields='items(kind, id, snippet(title, description, thumbnails, channelTitle), contentDetails(duration), statistics)',
		id=video_ID)
	response = request.execute()
	return response


def get_playlist(playlist_ID):
    '''
    Receives a playlist_ID that needs to start with PL_ and then we list all it's content by using list() keyword.
    With part we specify which aspects we want to retrieve and then we save it inside our response variable.
    Response is a dictionary containing key-values metadata so we can pick up the ones we are interested in. 
    '''
    try:
        request = youtube.playlists().list(
            part='snippet, contentDetails, status',
            id=playlist_ID)
        response = request.execute()

        # It's a playlist so response['items'] will only contain a single result with the playlist information
        items = response['items'][0]
        playlist_title = items['snippet']['title']
        playlist_items = items['contentDetails']['itemCount']
        playlist_status = items['status']['privacyStatus']
        playlist_ownership = items['snippet']['channelTitle']
        playlist_image = items['snippet']['thumbnails']['default']['url']    # change to grab the biggest possible

        print("\n[*] Displaying playlist information...")
        print(f"Title playlist: {playlist_title}\t" + "|\t" + f"Number of videos: {playlist_items}")
        print(f"Playlist owner: {playlist_ownership}")
        print(f"Playlist image URL: {playlist_image}")
        print(f"Playlist status: {playlist_status}\n")
        return response
    
    except UnboundLocalError as e:
        print(f"Check if the playlist URL is correct: {e}")


def get_playlist_details(playlist_ID):
    '''
    With contentDetails we can get video ID so we can extract later more information (number of likes, views, duration of the video...)
    With status we can check if that video is public, private or 
    '''
    import pprint
    request = youtube.playlistItems().list(
        part='snippet, contentDetails, status',
        playlistId=playlist_ID,
        maxResults=50)
    response = request.execute()
    print(pprint.pprint(response))

    items = response['items']

    for item in items:
        video_item = item.get('snippet', {}).get('position', 'No information available')
        video_title = item.get('snippet', {}).get('title', 'No title available')
        if video_title == 'Deleted video' or video_title == 'Private video':
            print(colored(f"{video_item} - {video_title}\n", "red"))
        else:
            print(colored(f"{video_item} - {video_title}\n", 'green'))
        video_URL = 'https://www.youtube.com/watch?v=' + item.get('contentDetails', {}).get('videoId', 'No video ID available')
        print(f"Video URL: {video_URL}\n")
        video_status = item.get('status', {}).get('privacyStatus', 'No information available')
        print(f"Video status: {video_status}")
        video_thumbnail = item.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', 'No default URL available')
        print(f"Video thumbnail: {video_thumbnail}")
        video_owner = item.get('snippet', {}).get('videoOwnerChannelTitle', 'No information available')
        print(f"Video Channel: {video_owner}")
        print("-"*100 + "\n")
    return response


def time_format(duration):
	'''
	YT uses ISO 8601 to format time and return it as a string as PT1H4M3S (PT is Time Duration, H is Hour, M is Minute and S is Second)
	This function dissects the string and separates hours, minutes and seconds for a more convenient view
	'''
	try:
		duration = duration[2:]
		#print(duration)
		h, m, s = duration.find("H"), duration.find("M"), duration.find("S")
		seconds = duration[m+1:s]
		if h > 0:
			minutes = duration[h+1:m]
			hours = duration[:h]
			return hours + " hours " + minutes + " minutes " + seconds + " seconds"
		else:
			minutes = duration[:m]
			return minutes + " minutes " + seconds + " seconds"

	except Exception as e:
		print(f"Time/Hour format error: {e}")


def time_format_minutes(duration):
	'''
	YT uses ISO 8601 to format time and return it as a string as PT1H4M3S (PT is Time Duration, H is Hour, M is Minute and S is Second)
	This function returns the total amount of minutes
	'''
	duration = duration[2:]
	h, m, s = duration.find("H"), duration.find("M"), duration.find("S")
	seconds = int(duration[m+1:s])
	if h > 0:
		minutes = int(duration[h+1:m])
		hours = int(duration[:h])
		return str(hours*60 + minutes + round(seconds/60, 2)) + " minutes"
	else:
		minutes = int(duration[:m])
		return str(minutes + round(seconds/60, 2)) + " minutes"


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
				duration = item['contentDetails']['duration']
				print(colored(f"\n[+] {title}\n", "green"))
				print(f"Type: {kind}\t" + "|\t" + f"ID: {video_id} \t" + "|\t" + f"Channel Title: {channel_title}")
				print("-"*90)
				print(f"Viewers: {viewers} \t" + "|\t" + f"Likes: {likes}	\t" + "|\t" + f"Comments: {comments}")
				print(colored("\n[-] Description:\n", "light_magenta") + "\t|" + f"{description.replace("\n", "\n\t|")}\n")
				print(f"Duration without formatting: {duration}")
				print(f"Duration: {time_format(duration)}")
				print(f"Duration in minutes: {time_format_minutes(duration)}")

		else:
			print("No video details found.")

	except KeyError as e:
		print(f"Missing items key: {e}")
	#except Exception as e:
		#print(f"Something failed: {e}")



def read_cache(cache_file="cache.txt"):
	'''Reads cache and gives back what has been stored before'''
	if os.path.exists(cache_file):
		with open(cache_file, "r") as file:
			return file.read().strip()	# strip is for removing empty spaces
	
	print(f"{cache_file} does not exist.")
	return None


def save_to_cache(video_URL, cache_file="cache.txt"):
	'''Saves video to cache'''
	with open(cache_file, "w") as file:
		file.write(video_URL)


if __name__:
    #video_URL = input(colored("\nEnter your video URL: ", "red"))
    #video_ID = video_URL.split("=")[-1]
    #details = get_video(video_ID)
    if not read_cache():
        print("No cache found.")
        playlist_URL = input(colored("\nEnter your playlist URL: ", "red"))
        print("[+] Saving to cache...")
        save_to_cache(playlist_URL)
    else:
        print(f"\n[*] Cache file: {read_cache()}")
        playlist_URL = input(colored("\nEnter your playlist URL (press Enter to use cache): ", "red"))
        if not playlist_URL:
            print("Using cache...")
            playlist_URL = read_cache()
        else:
            print("[+] Saving to cache...")
            save_to_cache(playlist_URL)
    
    print(playlist_URL)
    playlist_ID = playlist_URL.split("=")[-1]
    get_playlist(playlist_ID)
    get_playlist_details(playlist_ID)
    #get_video_information(details)






# Checklist improvements
# [] Create a database and add every item of the playlist
# [] Check periodically (once a day?) if videos have changed their status
# [] Give warnings for videos that you dont have access or that they have change their status
# [] Automate this check so it's done without you doing anything
# [] Status might lie, grab video ID and check if the URL for that video is working
# [] If video URL is working, check that video is actually displayed or unavailable! This might be check with requests maybe?
# [] If video is down, implement a YT search engine to search for similarities and display those that might be useful
# [] Add a counter so you can get metrics and the number of times you watch a video
# [] Use youtube-dl or something similar
# [] Think of a front-end interface or use Streamlit to display everything