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
            raise NotFound()


@api.register(prefix='/incrementMedalTally/<string:team>/<string:medal>',pk='<int:auth>')
class incrementMedalTally(Resource):
    name = 'incrementMedalTally'

    def read(self, request, team, medal, auth):
        if auth is 123:
            try:
				medals[team]['medals'][medal] = medals[team]['medals'][medal]+1
				return 'Success'
            except KeyError:
                raise NotFound()
        else:
        	raise Unauthorized()

