from __future__ import print_function
import sys
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_sqlalchemy import sqlalchemy

from app import app,db

from app.forms import PostForm
from app.models import Post, Tag, postTags


@app.before_first_request
def initDB(*args, **kwargs):
    db.create_all()
    if Tag.query.count() == 0:
        tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    smilecount = Post.query.count()
    return render_template('index.html', smilecount = smilecount, title="Smile Portal", posts=posts.all())


@app.route('/postsmile', methods=['GET', 'POST'])
def postsmile():
    form = PostForm()
    if form.validate_on_submit():
        newPost = Post(title = form.title.data, body = form.body.data, happiness_level = form.happiness_level.data)
        db.session.add(newPost)
        db.session.commit()
        flash('Post: "' + newPost.title + '" has been posted')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)


@app.route('/like/<post_id>', methods=['GET'])
def likepost(post_id):
    post = Post.query.get(post_id)
    post.likes +=1
    db.session.commit()
    flash('Post: "' + post.title + '" has been liked')
    return redirect(url_for('index'))
    
