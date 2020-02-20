import requests, sys, time
import redis

endpoint = 'https://itunes.apple.com/search?term={}&limit=1'
playlist_path = 'playlist.csv'
db = redis.Redis('localhost')

with open(playlist_path) as f:
    for i, line in enumerate(f):
        song, artist = line.strip().split(',')
        query = f"{song.replace(' ', '+')}+{artist.replace(' ', '+')}"
        data = requests.get(endpoint.format(query))
        if data.status_code == 200:
            try:
                song = data.json()['results'][0]
                print(f'----{i}----')
                print(f"{song['trackName']} - {song['artistName']}")
                record = {
                    'artistName': song['artistName'],
                    'trackName': song['trackName'],
                    'trackViewUrl': song['trackViewUrl'],
                    'previewUrl': song['previewUrl'],
                    'artworkUrl60': song['artworkUrl60'],
                    'artworkUrl100': song['artworkUrl100']
                }
                db.hmset(f"song:{i}", record)
                db.zadd('rock', {i: i})
                time.sleep(1)
            except Exception as e:
                print(e, file=sys.stderr)
        else:
            print(data.status_code, file=sys.stderr)
            print(query, file=sys.stderr)
