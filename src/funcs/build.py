import os
import re
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
        all_posts_template = env.get_template("posts.html")

        # Get md posts and parse the content
        for markdown_post in os.listdir("content"):
            file_path = os.path.join("content", markdown_post)

            with open(file_path) as f:
                post = markdown(f.read(), extras=['metadata'])

                posts.append({
                    "content" : post,
                    "slug" : markdown_post[:-3] + ".html",
                    "title" : post.metadata["title"],
                    "date" : post.metadata["date"]
                })


        # Sort all posts by creation date
        posts.sort(key=lambda post:datetime.strptime(post["date"], '%d-%m-%Y'), reverse=True)

        # Render index injecting the posts data into the index template and write the generated content into a file
        rendered_index = index_template.render(posts = posts)

        with open("output/index.html", 'w') as f:
            f.write(rendered_index)


        # All posts
        rendered_all_posts = all_posts_template.render(posts = posts)
        with open("output/posts.html", 'w') as f:
            f.write(rendered_all_posts)


        # Render posts injecting the content in the post template and write the generated contend into files
        for post in posts:
            file_path = "output/posts/" + post["slug"]
            rendered_post = post_template.render(post=post)

            with open(file_path, 'w') as f:
                f.write(rendered_post)


        # Render posts page
        print('Site generated succesfully')
    else:
        print('Error: eggs.toml not found in the current directory or ancestor')
