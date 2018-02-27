from restart import status
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound
from restart.utils import make_location_header

import threading

api = RESTArt()

medals_lock = threading.Lock()
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

events_lock = threading.Lock()
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
    	ret = []
    	t = threading.Thread(target=getMedalTally.getTally, args=(self, request, team, ret))
    	t.start()
    	t.join()
    	return ret[0]

    def getTally(self, request, team, ret):
		medals_lock.acquire()
		try:
			ret.append(medals[team])
		except KeyError:
			ret.append({"error": "key not found"})
		medals_lock.release()

@api.register(prefix='/incrementMedalTally/<string:team>/<string:medal>',pk='<int:auth>')
class incrementMedalTally(Resource):
	name = 'incrementMedalTally'

	def read(self, request, team, medal, auth):
		if auth is 123:
			ret = []
			t = threading.Thread(target=incrementMedalTally.incrementTally, args=(self, request, team, medal, auth, ret))
			t.start()
			t.join()
			return ret[0]
		else:
			return {"error": "unauthorized access"}

	def incrementTally(self, request, team, medal, auth, ret):
		medals_lock.acquire()
		try:
			medals[team]['medals'][medal] = medals[team]['medals'][medal]+1
			ret.append('Success')
		except KeyError:
			ret.append({"error": "key not found"})
		medals_lock.release()

@api.register(pk='<string:event>')
class getScore(Resource):
	name = 'getScore'
	def read(self, request, event):
		ret = []
		t = threading.Thread(target=getScore.getScore, args=(self, request, event, ret))
		t.start()
		t.join()
		return ret[0]

	def getScore(self, request, event, ret):
		events_lock.acquire()
		try:
			ret.append(events[event])
		except KeyError:
			ret.append({"error": "key not found"})
		events_lock.release()

@api.register(prefix='/setScore/<string:event>/<int:rome_score>/<int:gaul_score>',pk='<int:auth>')
class setScore(Resource):
	name = 'setScore'

	def read(self, request, event, rome_score, gaul_score, auth):
		if auth is 123:
			ret = []
			t = threading.Thread(target=setScore.setScore, args=(self, request, event, rome_score, gaul_score, auth, ret))
			t.start()
			t.join()
			return ret[0]
		else:
			return {"error": "unauthorized access"}

	def setScore(self, request, event, rome_score, gaul_score, auth, ret):
		events_lock.acquire()
		try:
			events[event]['Rome'] = rome_score
			events[event]['Gaul'] = gaul_score
			ret.append('Success')
		except KeyError:
			ret.append({"error": "key not found"})
		events_lock.release()








