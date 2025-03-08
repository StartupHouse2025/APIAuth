from flask import request

def checkArgs(required_args, request_args):
    for arg in required_args:
        if arg in request_args:
            pass
        else:
            raise Exception(f"Falta el parámetro requerido: {arg}")

def parsedRespond(data):
    temp = {
        'data' : data,
        'status': True,
        'message': 'ok'
    }
    return temp