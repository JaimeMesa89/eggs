import os
import shutil
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader

# Generate the index and posts on output
def build():
    if os.path.isfile('config.toml'):
        # Regenerate the output directory
        shutil.rmtree('output', ignore_errors=True)

        os.mkdir('output')
        os.mkdir('output/posts')
        shutil.copytree('static', 'output/static')
        shutil.copytree('styles', 'output/styles')


        posts = []

        # Load jinja templates
        env = Environment(loader=FileSystemLoader(os.path.join(os.getcwd(),'templates')))
        post_template = env.get_template("post.html")
        index_template = env.get_template("index.html")

        # Get md posts and parse the content
        for markdown_post in os.listdir("content"):
            file_path = os.path.join("content", markdown_post)

            with open(file_path) as f:
                posts.append(markdown(f.read(), extras=['metadata']))


        # Sort all posts by creation date
        posts.sort(key=lambda post:datetime.strptime(post.metadata["date"], '%d-%m-%Y'), reverse=True)


        # Render index injecting the posts data into the index template and write the generated content into a file
        posts_data = []

        for post in posts:
            data = {
                'slug': 'posts/' + post.metadata['title'].replace(" ", "") + '.html',
                'title': post.metadata['title'],
                'date': post.metadata['date']
            }

            posts_data.append(data)

        rendered_index = index_template.render(posts_data = posts_data)

        with open("output/index.html", 'w') as f:
            f.write(rendered_index)


        # Render posts injecting the content in the post template and write the generated contend into files
        for post in posts:
            data = {
                'content': post,
                'title': post.metadata['title']
            }

            file_path = "output/posts/" + post.metadata['title'].replace(" ", "") + ".html"
            rendered_post = post_template.render(post=data)

            with open(file_path, 'w') as f:
                f.write(rendered_post)

        print('Site generated succesfully')
    else:
        print('Error: eggs.toml not found in the current directory or ancestor')

