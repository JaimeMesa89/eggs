from http import server
import os
import sys
import shutil
from datetime import datetime
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
from http.server import HTTPServer, SimpleHTTPRequestHandler


# Generate project structure if the directory is empty
def init():
    if len(os.listdir()) == 0:
        script_dir = os.path.dirname(os.path.abspath(__file__))

        shutil.copytree(os.path.join(script_dir, 'templates'), os.path.join(os.getcwd(), 'templates'))
        shutil.copytree(os.path.join(script_dir, 'content'), os.path.join(os.getcwd(), 'content'), dirs_exist_ok=True)
        os.mkdir('output')
        print("Project initialized succesfully")

        print(f"An error ocurred: {e}")
    else:
        print("Error: Failed to initialize project")
        print("Error: The current directory is not empty")


# Generate the index and posts on output
def build():
    # Regenerate the output directory
    shutil.rmtree('output')
    os.mkdir('output')

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
            'slug': post.metadata['title'].replace(" ", "") + ".html",
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

        file_path = "output/" + post.metadata['title'].replace(" ", "") + ".html"
        rendered_post = post_template.render(post=data)

        with open(file_path, 'w') as f:
            f.write(rendered_post)

    print('Site generated succesfully')


def serve():
    server = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    print('Servidor en http://localhost:8000')

    server.serve_forever()


# Main
arg = None
try:
    arg = sys.argv[1]
except:
    pass

try:
    match arg:
        case 'init':
            init()

        case 'build':
            build()

        case 'serve':
            serve()

        case None:
            print('Excelsius and Glorious Generator of Sites')
            print('')
            print('Commands:')
            print('  init:  Initalize a new eggs project')
            print('  build: Deletes the content on the output directory and regenerates the site')
            print('  serve: Create a live server of the site, rebuilding the site on change automatically')

        case _:
            print(f'Error: unrecognized argument "{arg}"')
except Exception as e:
    print(f"An error ocurred: {e}")
