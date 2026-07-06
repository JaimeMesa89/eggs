import os
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader

posts = []
env = Environment(loader=PackageLoader('eggs', 'templates'))
post_template = env.get_template("post.html")
index_template = env.get_template("index.html")

# Get md posts and parse the content
for markdown_post in os.listdir("content"):
    file_path = os.path.join("content", markdown_post)

    with open(file_path) as f:
        posts.append(markdown(f.read(), extras=['metadata']))


# Sort all posts by creation date
posts.sort(key=lambda x:datetime.strptime(x.metadata["date"], '%d-%m-%Y'), reverse=True)


# Render index
posts_data = []

for post in posts:
    data = {
        'slug': post.metadata['title'].replace(" ", "") + ".html",
        'title': post.metadata['title'],
        'date': post.metadata['date']
    }

    posts_data.append(data)

rendered_index = index_template.render(posts_data = posts_data)

with open("output/index.html", 'w') as f:
    f.write(rendered_index)


# Render posts injecting the content in the html templates
for post in posts:
    data = {
        'content': post,
        'title': post.metadata['title']
    }

    file_path = "output/" + post.metadata['title'].replace(" ", "") + ".html"
    rendered_post = post_template.render(post=data)

    with open(file_path, 'w') as f:
        f.write(rendered_post)
