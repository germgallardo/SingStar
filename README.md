# SingStar

Ongoing project to collect and process all your YT data to keep track of your music.

Start by getting your key from Youtube Data API v3. Then you need to create in the same folder a `keys.txt` file and add your key there so you can get access.

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
