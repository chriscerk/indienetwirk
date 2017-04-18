import praw
import oauthinfo
import pylast
import re
import json
import uuid
import time
import nltk

print("")
print("-----indienetwirk-----")
print("")

def get_reddit_instance():
    my_info = oauthinfo.OAuthInfo()

    # Set OAuth info here
    id = '2bwdgZMLDesHrg'
    secret = 'trxw1X5z2xLmmkgD5_nn1X37CN4'
    agent = 'CrimsonAndCoder'

    my_info.set_info(id, secret, agent)

    if my_info.is_set is False:
        my_info.set_info_by_input()

    reddit = praw.Reddit(client_id=my_info.client_id,
                         client_secret=my_info.client_secret,
                         user_agent=my_info.user_agent)

    if reddit.read_only:
        print("read_only permissions on reddit verified.")
    else:
        print("An error occurred, ensure your client id, secret, and user agent information was correct")
        print("client id: " + my_info.client_id)
        print("client secret: " + my_info.client_secret)
        print("user agent: " + my_info.user_agent)
        exit()

    return reddit


def get_subreddit_instance(subreddit_name=input('Subreddit to archive: ')):
    subreddit = reddit.subreddit(subreddit_name)

    if subreddit.display_name is None:
        print("Unable to obtain subreddit instance, check name")
        exit()

    print('subreddit')
    print('   Name: ' + subreddit.display_name)
    print('   Title: ' + subreddit.title)
    print('')

    return subreddit


def get_subreddit_posts_by_date():
    print('Function not yet implemented!')
    exit()


def get_tag_names(artist):
    tags = artist.get_top_tags()
    tag_names = list()
    count = 0
    for tag in tags:
        count += 1
        if count > 5:
            break
        tag_names.append(tag[0].name)
    return tag_names


def get_lastFM_artist(query):
    first_search = network.search_for_artist(query)
    results_first = first_search.get_next_page()

    if results_first is None:
        return None

    if len(results_first) > 0:
        artist = results_first[0]
        if artist.listener_count > 3000:
            artist = network.get_artist(artist.name)
            return artist
    return None


def parse_post(submission):

    tag = '\[(?P<tag>FRESH((\s)?\w+)*)\]'
    artist = '(?P<artist>(\s?\w+)*)'
    release = '(?P<release>(\s?.+)*)'

    pattern = '^' + tag + '\s+' + artist + '\s+-\s+' + release + '$'
    m = re.search(pattern, submission.title)

    if m is None:
        return

    query = m.group('artist')
    artist = get_lastFM_artist(query)

    if artist is None:
        return

    post_info = dict()
    unique_id = uuid.uuid4().hex

    post_info['artist_genres'] = get_tag_names(artist)
    post_info['artist_name'] = artist.name
    post_info['artist_release'] = m.group('release')
    post_info['tag'] = m.group('tag')
    post_info['score'] = submission.score
    post_info['comment_count'] = len(submission.comments._comments)

    if submission.media:
        post_info['media_type'] = submission.media['type']
        try:
            post_info['media_thumbnail'] = submission.media['oembed']['thumbnail_url']
            post_info['media_embed'] = submission.media['oembed']['html']
        except:
            pass

    post_info['key'] = unique_id
    posts.append(post_info)
    print(post_info['artist_name'] + ' - ' + post_info['artist_release'])


reddit = get_reddit_instance()
subreddit = get_subreddit_instance()


API_KEY = "295cb5dbd2e307d9dc7dea1908dfec95"
API_SECRET = "c4c2b7f674c39e7e0842e7115b70b06f"
username = "chriscerk"
password_hash = pylast.md5(" 87000520")

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                               username=username, password_hash=password_hash)

posts = list()

print('Artist - Release')
print("----------")
post_count = 500
for submission in subreddit.top(limit=post_count):
    parse_post(submission)

current_date = time.ctime().replace(" ", "-").replace(":", "")
filename = subreddit.display_name + '_top(' + str(post_count) + ')_' + current_date + '.json'

with open('data/' + filename, 'w') as outfile:
    json.dump(posts, outfile)
