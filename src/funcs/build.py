import os
import re
import shutil
from datetime import datetime, timezone
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader
import xml.etree.ElementTree as ET
from email.utils import format_datetime

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

        templates = [
            template
            for template in env.list_templates(extensions=["html"])
            if template not in ["base.html", "post.html"]
        ]


        # Get md posts and parse the content
        for markdown_post in os.listdir("content"):
            file_path = os.path.join("content", markdown_post)

            with open(file_path) as f:
                markdown_file = f.read()

                post = markdown(markdown_file, extras=['metadata'])

                posts.append({
                    "content" : post,
                    "url" : "posts/" + markdown_post[:-3] + ".html",
                    "title" : post.metadata["title"],
                    "description" : post.split("\n\n", 2)[0].strip()[3:-4], 
                    "date" : post.metadata["date"],
                    "date-season" : get_season(post.metadata["date"])
                })


        # Sort all posts by creation date
        posts.sort(key=lambda post:datetime.strptime(post["date"], '%d-%m-%Y'), reverse=True)


        # Render regular templates 
        for template_name in templates:
            template = env.get_template(template_name)
            rendered_page = template.render(posts=posts)

            output_path = os.path.join("output", template_name)

            with open(output_path, "w") as f:
                f.write(rendered_page)


        # Render posts injecting the content in the post template and write the generated contend into files
        for post in posts:
            file_path = "output/" + post["url"]
            rendered_post = post_template.render(post=post)

            with open(file_path, 'w') as f:
                f.write(rendered_post)

        
        # Generate RSS
        generate_rss(posts)

        # Render posts page
        print('Site generated succesfully')
    else:
        print('Error: eggs.toml not found in the current directory or ancestor')


def get_season(date):
    season = ""

    date = date.split("-")

    if int(date[1]) in (12, 1, 2):
        season = "Winter"
    if int(date[1]) in (3, 4, 5):
        season = "Spring"
    if int(date[1]) in (6, 7, 8):
        season =  "Summer"
    else:
        season = "Autumm"

    season += " of " + date[2]

    return season


def generate_rss(posts):
    site_url = "https://jaimemesa.neocities.org/"
    rss = ET.Element("rss", version="2.0")    
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Jaime's Jazz Joint"
    ET.SubElement(channel, "description").text = "Jaime's favorite corner of the internet"
    ET.SubElement(channel, "link").text = site_url
    ET.SubElement(channel, "language").text = "en"

    for post in posts:
        item = ET.SubElement(channel, "item")

        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(item, "description").text = post["description"]
        ET.SubElement(item, "link").text = site_url + post["url"]

        date = datetime.strptime(post["date"], "%d-%m-%Y")
        date = date.replace(tzinfo=timezone.utc)

        ET.SubElement(item, "pubDate").text = format_datetime(date)
    
    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ")
    tree.write("output/rss.xml", encoding="utf-8", xml_declaration=True)


