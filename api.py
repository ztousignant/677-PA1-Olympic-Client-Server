from restart import status
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound
from restart.utils import make_location_header

api = RESTArt()
medals = {
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
events = {
	'Curling':{
		'Rome': 0,
		'Gaul': 0
	},
	'Skiing':{
		'Rome': 0,
		'Gaul': 0
	},
	'Skating':{
		'Rome': 0,
		'Gaul': 0
	}
}

@api.register(pk='<string:team>')
class getMedalTally(Resource):
    name = 'getMedalTally'

    def read(self, request, team):
    	try:
            return medals[team]
        except KeyError:
            return {"error": "key not found"}

@api.register(prefix='/incrementMedalTally/<string:team>/<string:medal>',pk='<int:auth>')
class incrementMedalTally(Resource):
    name = 'incrementMedalTally'

    def read(self, request, team, medal, auth):
        if auth is 123:
            try:
				medals[team]['medals'][medal] = medals[team]['medals'][medal]+1
				return 'Success'
            except KeyError:
                return {"error": "key not found"}
        else:
			return {"error": "unauthorized access"}
@api.register(pk='<string:event>')
class getScore(Resource):
    name = 'getScore'

    def read(self, request, event):
    	try:
            return events[event]
        except KeyError:
            return {"error": "key not found"}

@api.register(prefix='/setScore/<string:event>/<int:rome_score>/<int:gaul_score>',pk='<int:auth>')
class setScore(Resource):
    name = 'setScore'

    def read(self, request, event, rome_score, gaul_score, auth):
        if auth is 123:
            try:
				events[event]['Rome'] = rome_score
				events[event]['Gaul'] = gaul_score
				return 'Success'
            except KeyError:
                return {"error": "key not found"}
        else:
			return {"error": "unauthorized access"}









