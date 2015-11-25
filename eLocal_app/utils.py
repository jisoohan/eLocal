import json
from django.http import HttpResponse
from math import sin, cos, sqrt, asin, pi
from decimal import *

def json_response(response_dict, status=200):
    response = HttpResponse(json.dumps(response_dict), content_type="application/json", status=status)
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response

def check_distance(origin, destination, radius):
    print(origin)
    print(destination)
    print(radius)
    lat1 = deg2rad(float(origin[0]))
    lon1 = deg2rad(float(origin[1]))
    lat2 = deg2rad(float(destination[0]))
    lon2 = deg2rad(float(destination[1]))
    r = 3958.8

    distance = 2*3958.8*asin(sqrt( haversin(lat2-lat1) + cos(lat1)*cos(lat2)*haversin(lon2-lon1) ))
    print(distance <= radius)
    return distance <= radius

def haversin(theta):
    return sin(theta/2)**2

def deg2rad(deg):
    return deg*pi/180
