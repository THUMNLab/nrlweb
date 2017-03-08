from flask import Flask
from flask import render_template

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')
	
@app.route('/<name>')
def show_page(name):
	return render_template('%s.html' % name)

if __name__ == '__main__':
    app.run()
