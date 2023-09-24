from django.shortcuts import render
from django.http import JsonResponse
import os
import csv
from django.core.serializers import serialize
import datetime
import json
from django.http import HttpResponse
from django.template import loader
from django.db import connection

def create_dashboard(request):
    template = loader.get_template('pages/create_dashboard.html')
    return HttpResponse(template.render())