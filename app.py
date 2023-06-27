from flask import Flask, render_template, request, redirect, flash, jsonify
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

posts = []


@app.route('/blog-posts', methods=['GET', 'POST'])
def get_blog_posts():
    with open('blog_posts.json', 'r') as json_file:
        blog_posts = json.load(json_file)
    return jsonify(blog_posts)


# Save the data structure as a JSON file
def save_blog_posts(posts):
    with open('blog_posts.json', 'w') as json_file:
        json.dump(posts, json_file)


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

# Save the initial blog posts
save_blog_posts(blog_posts)


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    global blog_posts  # Include the global keyword to access the variable from outer scope

    if request.method == 'POST':
        # Get the form data
        title = request.form.get('title')
        content = request.form.get('content')

        # Create a new blog post
        new_post = {
            'id': len(blog_posts) + 1,  # Generate a new ID for the post
            'title': title,
            'content': content
        }

        blog_posts.append(new_post)  # Add the new post to the list
        save_blog_posts(blog_posts)  # Save the updated posts

        flash('Blog post added successfully.')  # Display flash message
        return redirect('/')

    return render_template('add.html')



@app.route('/delete/<int:post_id>')
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    for post in blog_posts:
        if post['id'] == post_id:
            blog_posts.remove(post)
            save_blog_posts(blog_posts)  # Save the updated posts
            flash('Blog post deleted successfully.')  # Display flash message
            break  # Exit the loop once the post is found and removed

    return redirect('/')



if __name__ == '__main__':
    app.run()
