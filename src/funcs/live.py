import livereload
from funcs.build import build

def live():
    build()

    server = livereload.Server()
    server.watch('content/*.md', build)
    server.watch('templates/*', build)
    server.watch('static/**/*', build)
    server.watch('styles/**/*', build)
    server.serve(root="output", debug=False)
