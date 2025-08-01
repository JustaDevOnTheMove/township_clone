from . import files_blueprint
from flask import render_template, send_from_directory, current_app, redirect, url_for



#######################################################
# FILES
#######################################################
@files_blueprint.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

@files_blueprint.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

@files_blueprint.route('/site.webmanifest', )
def webmanifest():
    return send_from_directory('static', 'site.webmanifest', mimetype='application/manifest+json')
