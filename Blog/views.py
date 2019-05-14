from flask import Blueprint, session, render_template, flash, redirect, url_for, request
from slugify import slugify
from werkzeug.security import generate_password_hash
import uuid
from PIL import Image
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import boto3
import io

blog_app = Blueprint('blog_app', __name__)

from application import db, application
from Blog.models import Post, Category, Comment
from author.models import Author
from Blog.forms import PostForm, CommentForm
from author.forms import ResetPasswordForm, ChangeUsernameForm
from author.decorators import login_required_check_confirmed, login_required
from config import BUCKET_NAME


limiter = Limiter(
        application,
        key_func=get_remote_address
    )

POSTS_PER_PAGE = 5

s3 = boto3.resource('s3')


# typeahead for categories?
# if session.id stuff for landing page? show different buttons instead of register if signed in.


@blog_app.route('/blog')
def index():
    page = int(request.values.get('page', '1'))
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()) \
        .paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html',
                           posts=posts,
                           title='Latest Posts')


@blog_app.route('/profile', methods=['GET', 'POST'])
@login_required_check_confirmed
def profile():
    author = Author.query.get(session['id'])
    posts = Post.query.filter_by(author_id=author.id).order_by(Post.publish_date.desc())[:10]  # Last 10 posts from user

    # forms that will be used for the modals on profile page.
    password_form = ResetPasswordForm()
    username_form = ChangeUsernameForm()

    if password_form.validate_on_submit():
        hashed_password = generate_password_hash(password_form.password.data)  # generate hash from pass form data.
        author.password = hashed_password  # change authors password
        db.session.commit()
        flash("Password successfully changed.", "success")

    if username_form.validate_on_submit():
        username = username_form.username.data
        author.username = username
        db.session.commit()
        db.session.refresh(author)
        flash("Username successfully changed.", "success")

    return render_template('blog/profile.html', posts=posts, password_form=password_form, username_form=username_form, author=author)


@blog_app.route('/')
def landing():
    return render_template('blog/landing_page.html')


@blog_app.route('/post', methods=('GET', 'POST'))
@login_required_check_confirmed
@limiter.limit("5/hour")
def post():
    form = PostForm()

    if form.validate_on_submit():
        image_id = None

        # create unique ID for image file_name. open image with PIL.
        if form.image.data:
            f = form.image.data
            image_id = str(uuid.uuid4())
            file_name = image_id + '.png'
            img = Image.open(f)

            # Send the Bytes to S3
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            s3_object = s3.Object(BUCKET_NAME, file_name)
            s3_object.put(
                Body=img_bytes.getvalue(),
                ContentType='image/png'
            )

        # Create new category in DB, if submitted in form.
        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data

        author = Author.query.get(session['id'])
        title = form.title.data.strip()
        body = form.body.data.strip()
        post = Post(
            author=author,
            title=title,
            body=body,
            image=image_id,
            category=category
        )

        db.session.add(post)
        db.session.commit()

        slug = slugify(str(post.id) + "-" + post.title)
        post.slug = slug
        db.session.commit()

        flash('Article Posted', 'success')
        return redirect(url_for('.article', slug=slug))

    return render_template('blog/post.html', form=form, action='new')


# no un-auth comments? all users must be signed up to comment.
@blog_app.route('/posts/<slug>', methods=['GET', 'POST'])
@limiter.limit("20/hour")
def article(slug):
    form = CommentForm()
    post = Post.query.filter_by(slug=slug).first_or_404()
    prev_url = request.referrer

    if form.validate_on_submit():
        author = Author.query.get(session['id'])  # query author ID so we can pass username into comment model.
        comment = Comment(
            author.username,  # username of signed in user.
            form.comment.data  # pull comment data from comment form
        )

        post.comments.append(comment)  # append comment to post (comments field of the model)
        db.session.add(comment)
        db.session.commit()
        flash("Thank you for taking the time to comment.", 'success')
        return redirect(url_for('.article', slug=slug))

    return render_template('blog/article.html', post=post, form=form, prev_url=prev_url)


@blog_app.route('/edit/<slug>', methods=('GET', 'POST'))
@login_required_check_confirmed
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    form = PostForm(obj=post)

    if form.validate_on_submit():
        original_image = post.image
        original_title = post.title
        form.populate_obj(post)

        if form.image.data:
            f = form.image.data
            image_id = str(uuid.uuid4())
            file_name = image_id + '.png'
            img = Image.open(f)

            # Send the Bytes to S3
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            s3_object = s3.Object(BUCKET_NAME, file_name)
            s3_object.put(
                Body=img_bytes.getvalue(),
                ContentType='image/png'
            )

            post.image = image_id

        else:
            post.image = original_image

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category

        if form.title.data != original_title:
            post.slug = slugify(str(post.id) + '-' + form.title.data)

        db.session.commit()
        flash('Article Edited', 'success')
        return redirect(url_for('.article', slug=post.slug))

    return render_template('blog/post.html', form=form, post=post, action='edit')


@blog_app.route('/delete/<slug>')
@login_required_check_confirmed
def delete(slug):
        post = Post.query.filter_by(slug=slug).first_or_404()
        post.live = False
        db.session.commit()
        flash('Article deleted', 'success')
        return redirect(url_for('.index'))


@blog_app.route('/categories/<category_id>')
def categories(category_id):
    category = Category.query.filter_by(id=category_id).first_or_404()
    page = int(request.values.get('page', '1'))
    posts = category.posts.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/category_posts.html', posts=posts, title=category.name, category_id=category_id)


# route for unconfirmed users. Will redirect to index if already confirmed.
@blog_app.route('/unconfirmed')
@login_required
def unconfirmed():
    if (Author.query.get(session['id'])).confirmed is True:
        return redirect(url_for('.index'))
    return render_template('author/unconfirmed.html')


@blog_app.errorhandler(429)
def ratelimit_handler(e):
    flash("Please do not spam, come back in 1 hour.", 'error')
    return redirect(url_for('.index'))







