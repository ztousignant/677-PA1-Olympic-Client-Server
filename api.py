from restart import status
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound
from restart.utils import make_location_header

api = RESTArt()
teams = {
	'Rome': {
		'medals': {
			'bronze': 0, 
			'silver': 0, 
			'gold': 0
		}
	},
	'Gaul': {
		'medals': {
			'bronze': 0, 
			'silver': 0, 
			'gold': 0
		}
	}
}

@api.register(pk='<string:team>')
class getMedalTally(Resource):
    name = 'getMedalTally'

    def read(self, request, team):
    	try:
            return teams[team]
        except KeyError:
            raise NotFound()
