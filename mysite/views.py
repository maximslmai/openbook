from django.http import HttpResponse
from django.shortcuts import render_to_response
from datetime import *

def index(request):
	time = datetime.now()
	return render_to_response('index.html', locals());