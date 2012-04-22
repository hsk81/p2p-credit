from django.http import HttpResponse
import json

class DATA:

    def info (request):

        jsdat = {
            'app' : 'edu',
            'ver' : '0.1'
        }

        return HttpResponse(json.dumps(jsdat)+'\n', mimetype='application/json')

    info = staticmethod (info)

class POST:

    pass

if __name__ == "__main__":

    pass
