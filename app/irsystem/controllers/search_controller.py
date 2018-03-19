from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

project_name = "Tunage: Finding songs to send a message"
net_id = "Michas Szacillo: (mas744), Gabrielle Haam (ggh39), Spencer Weiss (scw99), Wyatt Queirlo (wfq2), Filip Relander (far68)"

@irsystem.route('/', methods=['GET'])
def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "Your search: " + query
		data = range(5)
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)



