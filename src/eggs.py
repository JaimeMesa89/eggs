import os
import sys
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, PackageLoader


# Generate project structure if the directory is empty
def init():
    if len(os.listdir()) == 0:
        print("Genreate proyect")
        try:
            os.mkdir('templates')
            os.mkdir('content')
            os.mkdir('output')
        except Exception as e:
            print(f"An error ocurred: {e}")
    else:
        print("Error: Failed to create project")
        print("Error: The current directory is not empty")


# Generate the index and posts on output
def build():
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
    posts.sort(key=lambda post:datetime.strptime(post.metadata["date"], '%d-%m-%Y'), reverse=True)


    # Render index injecting the posts data into the html index template
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


    # Render posts injecting the content in the html post template
    for post in posts:
        data = {
            'content': post,
            'title': post.metadata['title']
        }

        file_path = "output/" + post.metadata['title'].replace(" ", "") + ".html"
        rendered_post = post_template.render(post=data)

        with open(file_path, 'w') as f:
            f.write(rendered_post)


# Main
arg = sys.argv[1]

match arg:
    case 'init':
        init()
    case 'build':
        build()
    case _:
        print(f'Error: unrecognized argument "{arg}"')
