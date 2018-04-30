from . import *
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder
from app.irsystem.controllers.settings import access_token, refresh_token

project_name = "Tunage - Finding songs to send a message"
net_id = "Michas Szacillo: (mas744), Gabrielle Haam (ggh39), Spencer Weiss (scw99), Wyatt Queirolo (wfq2), Filip Relander (far68)"

@irsystem.route('/', methods=['GET',"POST"])
def search():
	output_message = 'hi, please enter a query :)'
	'''query = request.args.get('search')
	if not query:
		data = []
		output_message = 'hi, please enter a query :)'
	else:
		data = range(10)
		output_message = "Your search: " + query
	'''
	if request.method == "GET":
		global access_token
		mytok = access_token
		print(mytok)
		return render_template('search.html', name=project_name, netid=net_id, output_message=output_message,tok=mytok)
	if request.method=="POST":
		response = bencode({
        "Access-Control-Allow-Origin": "*",
    	})
    	return Response(response, mimetype='text/plain')
