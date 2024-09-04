import glob, os
import logging
from flask import Flask, request, render_template
from tinydb import TinyDB, Query
import time
import server_config
import json



app = Flask(__name__)
NUM_OF_NODES = server_config.NUMBER_OF_NODES
SERVER_PORT = server_config.SERVER_RUN_PORT
# node_id : int
# cpu_temp : float
# cpu_use : float
# net_in : int
# net_out : int
# mem_use : float




current = 'db.json'
if os.path.isfile(current):
	os.remove(current)
else:
	db = TinyDB('db.json')



@app.route('/report/')
def report():
	
	query = request.args.to_dict(flat=False)
	node_id = query["node_id"][0]
	cpu_temp = query["cpu_temp"][0]
	cpu_use = query["cpu_use"][0]
	net_in = query["net_in"][0]
	net_out = query["net_out"][0]
	mem_use = query["mem_use"][0]
	db.insert({'node_id' : node_id, 'cpu_temp':cpu_temp, 'cpu_use':cpu_use, 'net_in' : net_in,'net_out' : net_out, 'mem_use':mem_use })
	time.sleep(1)
	return 'Received data from {}'.format(node_id)

@app.route('/')
def home():
	results = []
	i=0
	while NUM_OF_NODES > i:
		Node = Query()
		count = i+1
		try:
			res = db.search(Node["node_id"] == str(count))
			if len(res) > 5:
			#print('FUCKING LIST {} {}'.format(i, res[0]))
				results.append(res[0])
			i+=1
			return render_template('index.html', results = results)
		except:
			print('oops')
			return render_template('500.html')

@app.route('/everything')			
def show():
	
		
	return render_template('everything.html')



@app.before_request
def hook():
	
	print(request.args)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=SERVER_PORT, debug=True)
