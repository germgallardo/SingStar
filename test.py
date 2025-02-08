from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from termcolor import colored
import os
import argparse
import sys
import json
import re
import httplib2
import socket
import time


# Retrieves YT_API_KEY defined as an environment variable
YT_API_KEY = os.getenv("YT_API_KEY")

if not YT_API_KEY:
    sys.exit(colored("No API Key found. Set the API key as an environment variable.", "red"))

youtube = build('youtube', 'v3', developerKey=YT_API_KEY)


def get_video(video_ID):
    request = youtube.videos().list(
        part='snippet, contentDetails, statistics',
        fields='items(kind, id, snippet(title, description, thumbnails, channelTitle), contentDetails(duration), statistics)',
        id=video_ID)
    response = request.execute()
    return response


def playlist_request(request, timeout_duration=7, retries=5, backoff=2):
    '''
    Requests a playlist and raises different exceptions if it finds any error
    If the request is correct, the function gives back the response

    Parameters:
    - timeout_duration: maximum amount of time (seconds) the request will wait before raising an error
    - retries: number of attempts to be made before exiting the program because of a connectivity/server issue
    - backoff: exponential backoff factor for the retries, i.e. how many seconds the program will wait to make another retry based on the attempt number
    
    In case there is a connectivity/server issue, it will make some retries with an exponential backoff to give time for recovery
    For more information: https://peerdh.com/blogs/programming-insights/timeout-strategies-and-backoff-techniques-in-structured-concurrency
    '''
    for attempt in range(retries):
        try:
            print(f"Request: {request}")

            # Execute the request and check if the response has a parameter called `items` within the Playlist information
            response = request.execute(http=httplib2.Http(timeout=timeout_duration))
            
            if not response.get('items'):
                sys.exit(colored(f"Playlist not found. Check Playlist_ID as it might be incorrect.", "red"))
            
            return response
        
        except HttpError as e:
            # Request returns a json object that needs to be processed to get the type of error and message
            # For an invalid API key it will give a 400 error, if you have reached your quota, it will give a 403 error
            # For a rate limit exceeded or a connectivity error, the code should be 429 and 500 respectively
            print(f"Raising HttpError: {e}")
            error = json.loads(e.content).get('error', {})
            code = error.get('code', 'Unknown Code')
            message = error.get('message', 'No message provided.')

            if code == 429:
                sys.exit(colored(f"HttpError: {code}. Rate limit exceeded, too many requests."))

            if code == 500:
                sys.exit(colored(f"HttpError: {code}. A connectivity error ocurred. Server is currently unreachable."))

            else:
                # With a regular expression we remove any html tags (e.g. <a> for quota limits) from the message
                sys.exit(colored(f"HttpError: {code}. {re.sub(r'<.*?>', '', message)}", "red"))

        except httplib2.error.ServerNotFoundError as e:
            # A test to simulate this error can be made by disconnecting from the internet
            print(colored(f"There was a server error, check your internet connection. {e}", "red"))

        except socket.timeout as e:
            # To test this, reduce the timeout_duration to 0.1 seconds
            print(colored(f"There was a timeout error, the request took too long to complete. {e}", "red"))

        except Exception as e:
            sys.exit(colored(f"An unexpected error ocurred: {e}", "red"))

        # wait_time is the amount of time (seconds) the program will wait before the next retry
        wait_time = backoff**attempt
        print(f"Attempt {attempt+1} failed. Trying again in {wait_time} seconds")
        time.sleep(wait_time)

    sys.exit(colored("Maximum number of retries reached. The request could not be made. Try later.", "red"))


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

        response = playlist_request(request)

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
    
    except Exception as e:
        sys.exit(colored(f"An unexpected error ocurred: {e}", "red"))


def get_playlist_details(playlist_ID):
    '''
    With contentDetails we can get video ID so we can extract later more information (number of likes, views, duration of the video...)
    With status we can check if that video is public, private or 
    '''
    #import pprint
    request = youtube.playlistItems().list(
        part='snippet, contentDetails, status',
        playlistId=playlist_ID,
        maxResults=50)
    
    response = playlist_request(request)
    #print(pprint.pprint(response))

    # Gets first 50 results from the playlist
    get_playlist_videos(response)

    # Grabs the token for the next page (in case there are several pages), if there's no token, response will return None
    nextPageToken = response.get('nextPageToken')

    # Checks if Token exists and if it's inside the response and then creates a new request by using this token for the next page
    while "nextPageToken" in response:
        nextPage_request = youtube.playlistItems().list(
            part='snippet, contentDetails, status',
            playlistId=playlist_ID,
            maxResults=50,
            pageToken=nextPageToken)
        
        response = nextPage_request.execute()

        # Gets next 50 results from the playlist
        get_playlist_videos(response)

        # Tries to grab the next Token for the next page
        nextPageToken = response.get("nextPageToken")

    print(colored(f"Playlist '{response['items'][0]['snippet']['title']}' has been successfully retrieved!\n", "magenta"))



def get_playlist_videos(response):
    '''
    Receives a playlist request to list all items from within
    '''
    items = response['items']
    
    for item in items:
        video_item = item.get('snippet', {}).get('position', 'No information available')
        video_title = item.get('snippet', {}).get('title', 'No title available')
        if video_title == 'Deleted video' or video_title == 'Private video':
            print(colored(f"{video_item+1} - {video_title}\n", "red"))  # video_item+1 because index starts from 0 and should start from 1
        else:
            print(colored(f"{video_item+1} - {video_title}\n", 'green'))
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
        duration = duration[2:]     # removes `PT` from the string
        # With `find()` we can get the position for each letter, if that letter is not found it will return a -1
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
        items = details['items']    # this throws a key error if it cannot find items

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
                print(f"Viewers: {viewers} \t" + "|\t" + f"Likes: {likes}   \t" + "|\t" + f"Comments: {comments}")
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



if __name__ == "__main__":
    '''
    To run this program: python test.py [Playlist_ID]
    Playlist_ID is an optional parameter and it needs to start with "PL", e.g. PLqNVAh4vnnHEUkdctr7n9LTyUe6-JEHpm
    If Playlist_ID is not provided, the program will use the one from default
    '''

    # Defines parser to provide help information
    epilog_text = colored("For more information visit: https://github.com/germgallardo/SingStar/README.md", "cyan")
    parser = argparse.ArgumentParser(
                    prog='test.py',
                    description='Displays information from each video of a YouTube Playlist',
                    epilog=epilog_text)

    # Accepts a playlist_id parameter, with nargs='?' we can define it as an optional parameter
    parser.add_argument("Playlist_ID",
                        nargs="?",
                        default="PLBKqHs5LAsifp7juT68FVA7M7nNQvLIlS",
                        help="Youtube Playlist ID needs to start with PL, e.g. PLqNVAh4vnnHEUkdctr7n9LTyUe6-JEHpm")
    
    # Grabs the Playlist_ID parameter provided or the one from default
    Playlist_ID = parser.parse_args().Playlist_ID

    if Playlist_ID[:2] != "PL":
        sys.exit(colored("Playlist_ID must start with `PL`. Run `python test.py --help` to check for an example.", "red"))

    if Playlist_ID == parser.get_default('Playlist_ID'):
        print(colored(f"\nUsing default Playlist ID: {Playlist_ID}", "yellow"))
    else:
        print(colored(f"\nUsing provided Playlist ID: {Playlist_ID}", "blue"))


    get_playlist(Playlist_ID)
    get_playlist_details(Playlist_ID)
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