import json


genre_popularity = dict()
genreNames = list()
genre_by_pop = list()

posts_filename = 'data/indieheads_top(500)_Mon-Apr-17-191636-2017.json'

with open(posts_filename) as json_data:
    posts = json.load(json_data)

    for post in posts:
        for genre in post['artist_genres']:
            if genre_popularity.get(genre):
                if post.get('comment_count'):
                    genre_popularity[genre] += post['comment_count']
                genre_popularity[genre] += post['score']
            else:
                genreNames.append(genre)
                if post.get('comment_count'):
                    genre_popularity[genre] = post['comment_count'] + post['score']
                else:
                    genre_popularity[genre] = post['score']

    for genreName in genreNames:
        item = dict()
        item['genre_name'] = genreName
        item['popularity'] = genre_popularity[genreName]
        genre_by_pop.append(item)

out_filename = 'indieheads_genres_by_popularity'
with open('data/' + out_filename, 'w') as outfile:
    json.dump(genre_by_pop, outfile)
