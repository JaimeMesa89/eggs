import sys

from funcs.init import init
from funcs.build import build

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
