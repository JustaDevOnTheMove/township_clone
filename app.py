import os, sys
from dotenv import load_dotenv
from flask_frozen import Freezer
from flask_htmlmin import HTMLMIN
from flask_assets import Environment, Bundle
from project import create_app

load_dotenv()

app = create_app()
app.config.from_object(__name__)

# Flask app settings
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'set-your-secret-key-here-or-in-dot-env')
app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['PORT'] = os.getenv('PORT', 5002)

# Build script settings
app.config['RUN_TYPE'] = f'{sys.argv[1] if len(sys.argv) > 1 else "run"}'
app.config['BUILD_ENV'] = os.getenv('BUILD_ENV', '')
app.config['ASSET_HOST'] = os.getenv('ASSET_HOST', '')
app.config['ASSET_HOST_DEV'] = os.getenv('ASSET_HOST') == 'True'

# flask_frozen settings
# Where to store the static files. The root of your static website will be in here.
app.config['FREEZER_DESTINATION'] = 'build'
# Remove extra files that are not part of the build
app.config['FREEZER_REMOVE_EXTRA_FILES'] = True
# Files to not copy into /project/build/static/* (in alphabetical order)
app.config['FREEZER_STATIC_IGNORE'] = [
    '.webassets-cache',
    'media',
    'tailwind',
    'robots.txt',
    'site.webmanifest',
    'sitemap.xml',
]

assets = Environment(app)

# If ASSET_HOST is specified (e.g.: https://cdn.example.com), then fully qualified URL are applied to assets.
# If ASSET_HOST_DEV == "True" then this will apply to local development also if ASSET_HOST is specified.
if app.config.get('ASSET_HOST') and (
    app.config.get('RUN_TYPE', 'run') == "build" or
    app.config.get('ASSET_HOST_DEV')):
    def flask_assets_url_for(endpoint='', **values):
        host = app.config.get('ASSET_HOST')
        return f"{host}/{endpoint}"
    assets.url = flask_assets_url_for('static')

# Only minify the HTML when building the frozen files for production
if app.config["BUILD_ENV"] == "production":
    app.config['MINIFY_HTML'] = True
    htmlmin = HTMLMIN(app)

# Only minify the CSS when building the frozen files for production
# (in sequencial order that they need to be withing the final output file)
if app.config["BUILD_ENV"] == "production":
    css = Bundle(
        'tailwind/generated.css',
        'tailwind/fonts.css',
        'tailwind/custom.css',
        filters='cssmin',
        output='css/styles.css',
    )
else:
    css = Bundle(
        'tailwind/generated.css',
        'tailwind/fonts.css',
        'tailwind/custom.css',
        output='css/styles.css',
    )

assets.register('css_all', css)

# Force rebuild of the bundled CSS file(s).
# This is needed to (re)generate: `css/styles.css`
css.build(force=True)

# Initialize the freezer
freezer = Freezer(app)


if __name__ == '__main__':
    # To generate the static site files into the build directory:
    # `python3 app.py build` or `scripts/build-dev.sh` or `scripts/build.sh`
    if app.config["RUN_TYPE"] == "build":
        freezer.freeze()

    # To run the site in development mode:
    # `python3 app.py` or `scripts/run-dev.sh`
    else:
        app.run(
            port=app.config['PORT'],
            debug=app.config['FLASK_ENV'] == 'development',
        )
