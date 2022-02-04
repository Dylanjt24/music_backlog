import requests
import random
from flask_app import app
from flask import render_template, request, redirect, session, jsonify
from flask_app.models.user_model import User
from flask_app.models.album_model import Album
import os


@app.route('/')
def results():
    return render_template('search.html')

@app.route('/search', methods=['POST'])
def search():
    exists = True
    count = 0
    while exists:

        r = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={request.form['query']}&limit=300&autocorrect=1&api_key={os.environ.get('MUSIC_BACKLOG_API_KEY')}&format=json")
        if (len(r.json()['similarartists']['artist']) == 0):
            return "none"

        index = random.randrange(0, len(r.json()['similarartists']['artist']))
        artist_name = r.json()['similarartists']['artist'][index]['name']

        r = requests.get(f"http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist={artist_name}&limit=1&api_key={os.environ.get('MUSIC_BACKLOG_API_KEY')}&format=json")
        artist_name = r.json()['topalbums']['album'][0]['artist']['name']
        album_name = r.json()['topalbums']['album'][0]['name']
        album = Album.get_one_by_artist_album({'artist': artist_name, 'album': album_name})

        if 'uuid' not in session:
            exists = False
        elif not album:
            exists = False
        else:
            in_ignored = User.get_one_ignored({'user_id': session['uuid'], 'album_id': album.id})
            in_backlog = User.get_one_backlog({'user_id': session['uuid'], 'album_id': album.id})
            if not in_ignored and not in_backlog:
                exists = False

        count += 1
        if count == 25:
            return 'none'
    return jsonify( r.json() )

@app.route('/backlog')
def backlog():
    if 'uuid' not in session:
        return redirect('/')
    backlog = User.get_backlog({'id': session['uuid']})
    return render_template('backlog.html', backlog=backlog)

@app.route('/backlog/add', methods=['POST'])
def add_to_backlog():
    album = Album.get_one_by_artist_album(request.form)
    if not album:
        album = Album.create(request.form)
        Album.add_to_backlog({'album_id': album, 'user_id': session['uuid']})
        return redirect('/')
    Album.add_to_backlog({'album_id': album.id, 'user_id': session['uuid']})
    return redirect('/')

@app.route('/backlog/<int:id>/delete')
def remove_album(id):
    Album.remove_from_backlog({'id': id})
    return redirect('/backlog')

@app.route('/backlog/ignore')
def get_ignored():
    if 'uuid' not in session:
        return redirect('/')
    ignored = User.get_ignored({'id': session['uuid']})
    return render_template('ignored.html', ignored=ignored)

@app.route('/backlog/ignore/add', methods=['POST'])
def ignore_album():
    album = Album.get_one_by_artist_album(request.form)
    if not album:
        album = Album.create(request.form)
        Album.ignore_album({'album_id': album, 'user_id': session['uuid']})
        return redirect('/')
    Album.ignore_album({'album_id': album, 'user_id': session['uuid']})
    return redirect('/')

@app.route('/backlog/ignore/<int:id>/delete')
def remove_ignored(id):
    Album.remove_from_ignored({'id': id})
    return redirect('/backlog/ignore')