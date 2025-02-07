# SingStar

Ongoing project to collect and process all your YT data to keep track of your music.

Start by getting your key from Youtube Data API v3.

For running the program, Youtube Data API key needs to be set up first as an environment variable. For Windows (Powershell):
```
$env:YT_API_KEY="ADD_YOUR_YT_DATA_API"
```
For Mac/Linux the next command can be used instead:
```
export YT_API_KEY="ADD_YOUR_YT_DATA_API"
```
**Note: This is temporary and needs to be set up every time you run a terminal session or the key will not be available.**

To do it permanently, for Windows you need to manually open the environment variable settings and add a new one called `YT_API_KEY` with your current key. For Mac/Linux the export command needs to be added to the `.bashrc` file.

---

This application requires a `Playlist_ID` parameter. This parameter needs to be provided through the command line input.

Given a Playlist URL like:
```
https://www.youtube.com/watch?v=-MfiaO7xl2c&list=PLqNVAh4vnnHEUkdctr7n9LTyUe6-JEHpm
```

The `Playlist ID` parameter is everything after `list=`, in this case it would be:
```
PLqNVAh4vnnHEUkdctr7n9LTyUe6-JEHpm
```

**Note: `Playlist_ID` needs to start with `PL`.**

---

To run the application, first install the required dependencies and then use the following command to execute the program:
```
pip install -r requirements.txt
```
```
python test.py [Playlist_ID]
```

If no Playlist ID is provided, the program will use a default `Playlist_ID`.
