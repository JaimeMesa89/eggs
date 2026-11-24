import os
from pathlib import Path

config_file = """\
title = ""
description = ""
url = ""
language = ""
"""

index_template = """\
<!Doctype html>
<html lang="en"> 
<head>
  <meta charset="UTF-8">
  <title> My blog </title>
  <link rel="stylesheet" href="/styles/style.css">
</head>
<body>
  <h1> Blog posts </h1>
  <ul>
  {% for post in posts %}
  <li> <a href=" {{ post["url"] }}"> {{ post["title"] }} </a>| <small> {{ post["date"] }} </small></li>
  <img src="{{ post["thumbnail"] }}" alt="monito" width="150" height="100">
  {% endfor %}
  </ul>
</body>
</html>
"""

post_template = """\
<!Doctype html>
<html lang="en"> 
<head>
  <meta charset="UTF-8">
  <title> {{ post[title] }} </title>
  <link rel="stylesheet" href="/styles/style.css">
</head>
<body>
  <h1> {{ post["title"] }} </h1>
  {{ post["content"] }}
</body>
</html>
"""

sample_post = """\
title: Sample Title
date: 6-7-2026

Sample content
"""

# Generate project structure if the directory is empty
def init(path):
    if path != None:
        os.chdir(path)

    if len(os.listdir()) == 0:
        os.mkdir('templates')
        os.mkdir('content')
        os.mkdir('styles')
        os.mkdir('static')

        with open('config.toml', 'w') as f:
            f.write(config_file)

        with open('templates/index.html', 'w') as f:
            f.write(index_template)

        with open('templates/post.html', 'w') as f:
            f.write(post_template)

        with open('content/sample_post.md', 'w') as f:
            f.write(sample_post)
            
        with open('styles/style.css', 'w') as f:
            f.write('')


        print("Project initialized succesfully")
    else:
        print("Error: Failed to initialize project")
        print("Error: The selected directory (" + os.getcwd() + ") is not empty")
