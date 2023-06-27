from flask import Flask, render_template, request, redirect, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

# Example blog posts
blog_posts = [
    {
        "id": 1,
        "author": "John Doe",
        "title": "First Post",
        "content": "This is my first post."
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Second Post",
        "content": "This is another post."
    }
]


def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as json_file:
        json.dump(posts, json_file)


def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None


def update_post(post_id, title, author, content):
    for post in blog_posts:
        if post['id'] == post_id:
            post['title'] = title
            post['author'] = author
            post['content'] = content
            save_blog_posts(blog_posts)
            break


def delete_post(post_id):
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            save_blog_posts(blog_posts)
            break


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        writer = request.form.get('writer')
        data = request.form.get('data')

        new_post = {
            'id': len(blog_posts) + 1,
            'title': title,
            'author': writer,
            'content': data
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        flash('Blog post added successfully.')
        return redirect('/')

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    if request.method == 'POST':
        delete_post(post_id)
        flash('Blog post deleted successfully.')

    return redirect('/')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = fetch_post_by_id(post_id)

    if post is None:
        return redirect('/add')

    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')
        update_post(post_id, title, author, content)
        return redirect('/')

    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run()
