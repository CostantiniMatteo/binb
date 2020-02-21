import requests, sys, time
import redis

endpoint = 'https://itunes.apple.com/search?term={}&limit=1'
playlist_path = 'italia_80_90_00.csv'
db = redis.Redis('localhost')

with open(playlist_path) as f:
    last = -1
    song_id = last + 1
    for i, line in enumerate(f):
        song, artist = line.strip().split('ツ')
        query = f"{song.replace(' ', '+')}+{artist.replace(' ', '+')}"
        data = requests.get(endpoint.format(query))
        if data.status_code == 200:
            try:
                song = data.json()['results'][0]
                release_year = int(song['releaseDate'].split('-')[0])
                if release_year < 1962:
                    continue
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
                db.hmset(f"song:{song_id}", record)
                db.zadd('pop', {song_id: song_id})
                song_id += 1
                time.sleep(1)
            except Exception as e:
                print(e, file=sys.stderr)
        else:
            print(data.status_code, file=sys.stderr)
            print(query, file=sys.stderr)
