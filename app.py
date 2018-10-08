import sys

from flask import Flask, render_template

from utils.common_utils import getConfig

config = getConfig()

app = Flask(__name__)

# sys.path.append('./routes')
from routes.static_pages import index_page, about_page
from routes.articles_routes import articles
from routes.materials_routes import materials
from routes.auth_routes import auth
from routes.visualizations_routes import visualization
from routes.dashboard import dashboard_route
from routes.search_routes import searches

app.register_blueprint(index_page)
app.register_blueprint(about_page)
app.register_blueprint(articles)
app.register_blueprint(materials)
app.register_blueprint(auth)
app.register_blueprint(visualization)
app.register_blueprint(dashboard_route)
app.register_blueprint(searches)

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

# Main Part
if __name__ == '__main__':
	config = getConfig()
	app.secret_key = config.SECRET_KEY
	app.run(debug=True)
