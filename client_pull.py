from restart import status
from restart import testing
from restart.api import RESTArt
from restart.resource import Resource
from restart.exceptions import NotFound
from restart.utils import make_location_header

api = RESTArt()
client = testing.Client(api)
response = client.get('http://127.0.0.1:5000/getScore/Curling')
print response