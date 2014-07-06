from flask import Flask, render_template
from assets import assets

app = Flask(__name__)
assets.init_app(app)

@app.route('/')
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
