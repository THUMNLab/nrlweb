from flask import Flask, request, render_template, session
import json

app = Flask(__name__)
#app.debug = True
try:
	app.secret_key = open('secret_key').read()
except Exception as e:
	print('Please create a file named `secret_key` with a secret string like `d3b4c763-24b3-451b-9dbf-b3063c500198`.')
	raise e

for cnt_path in ['counter', '/shared/counter']:
	try:
		cnt = sum((1 for line in open(cnt_path)))
		break
	except Exception as e:
		pass
else:
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
	global cnt, cnt_path
	if 'count' not in session:
		cnt += 1
		session['count'] = cnt
		with open(cnt_path, 'a') as f:
			f.write('%s\n' % request.remote_addr)
	
@app.route('/')
def index():
	global papers
	return render_template('index.html', cnt = add_th(session['count']), papers = papers)
	
@app.route('/<name>')
def show_page(name):
	global papers
	args = None
	for paper in papers:
		if paper['url'] == name:
			args = paper
			break
	return render_template('%s.html' % name, cnt = add_th(session['count']), args = args, papers = papers)

if __name__ == '__main__':
	load_papers()
	app.run(host = '0.0.0.0')
