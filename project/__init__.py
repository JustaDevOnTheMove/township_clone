from flask import Flask, render_template



######################################
#### Application Factory Function ####
######################################

# def noop(_in, out, **kw):
#     out.write(_in.read())

def create_app():
    # Create the Flask application
    app = Flask(__name__, template_folder='templates')

    register_blueprints(app)
    register_error_pages(app)
    return app



########################
### Helper Functions ###
########################

def register_blueprints(app):
    # Import the blueprints
    from project.website import pages_blueprint
    app.register_blueprint(pages_blueprint)

    from project.website import files_blueprint
    app.register_blueprint(files_blueprint)


def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
