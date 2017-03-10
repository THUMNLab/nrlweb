from flask import Flask, request, render_template, session
import json

app = Flask(__name__)
app.debug = True
app.secret_key = 'd3b4c763-24b3-451b-9dbf-b3063c500198'

try:
	cnt = sum((1 for line in open('counter')))
except Exception as e:
	cnt = 0
	
def load_papers():
	global papers
	papers = json.load(open('paper_list.json'))

def add_th(num):
	if num % 10 == 1 and num % 100 != 11:
		suf = 'st'
	elif num % 10 == 2 and num % 100 != 12:
		suf = 'nd'
	elif num % 10 == 3 and num % 100 != 13:
		suf = 'rd'
	else:
		suf = 'th'
	return '%d-%s' % (num, suf)
	
@app.before_request
def add_counter():
	global cnt
	if 'count' not in session:
		cnt += 1
		session['count'] = cnt
		with open('counter', 'a') as f:
			f.write('%s\n' % request.remote_addr)
	
@app.route('/')
def index():
	global papers
	return render_template('index.html', cnt = add_th(session['count']), papers = papers)
	
@app.route('/<name>')
def show_page(name):
	global papers
	return render_template('%s.html' % name, cnt = add_th(session['count']), papers = papers)

if __name__ == '__main__':
	load_papers()
	app.run(host = '0.0.0.0')
