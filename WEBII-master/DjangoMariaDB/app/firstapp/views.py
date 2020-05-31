# Create your views here.
#IMPORT models
from .models import Movie,ApiUsers

#IMPORT LIBRARIRES/FUNCTIONS
#from django.shortcuts import render , HttpResponse
from django.http import JsonResponse
import json
from firstapp.customClasses import *
#IMPORT DJANGO PASSWORD HASH GENERATOR AND COMPARE
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, HttpResponse

def vista (request):
    return render(request,'index.html')
#check_password(noHashPassword,HashedPassword) this funcion validate if the password match to the hash
def login(request):

    #VALIDATE METHOD
    if request.method == 'POST':

        #DECLARE RESPONSE
        responseData = {}
        msgError = ""
        detectedError = False

        #CHECK JSON STRUCTURE
        validateJson = checkJson(request.body)
        if (validateJson):
            jsonBody = json.loads(request.body)

        #CHECK JSON CONTENT
            if "user" not in jsonBody:
                msgError = "Requires User"
                detectedError = True
            elif "password" not in jsonBody:
                msgError = "Requires Password"
                detectedError = True
        #CHECK IF USER EXITST
            else:
                try:
                    currentUser = ApiUsers.objects.get(user = jsonBody['user'])
                except Exception as e:
                    msgError = "The user does not exist or the password is incorrect"
                    detectedError = True
                    responseData['result'] = 'error'
                    responseData['message'] = msgError
                    return JsonResponse(responseData,status=401)


        #TAKE PASSWORD OF THE USER
                passJsonBody = jsonBody['password']
                currentUserPass = currentUser.password


        #CHECK IF PASSWORD IS CORRECT
                if not check_password(passJsonBody,currentUserPass):
                    msgError = "The user does not exist or the password is incorrect"
                    detectedError = True



        #CHECK IF USER HAS API-KEY
                elif currentUser.api_key == None:
                            newApiKey = ApiKey().generate_key_complex()
                            currentUser.api_key = newApiKey
                            currentUser.save()
                            responseData['result'] = 'SUCCESS'
                            responseData['message'] = 'Correct Credentials'
                            responseData['userApiKey'] = currentUser.api_key
                            return JsonResponse(responseData,status=200)



                else:
                    responseData['result'] = 'SUCCESS'
                    responseData['message'] = 'Correct Credentials'
                    responseData['userApiKey'] = currentUser.api_key
                    return JsonResponse(responseData,status=200)


            if detectedError == True:
                    responseData['result'] = 'ERROR'
                    responseData['message'] = msgError
                    detectedError = False
                    return JsonResponse(responseData,status=401)

        else:
            responseData['result'] = 'ERROR'
            msgError = "Invalid JSON Format"
            responseData['message'] = msgError
            return JsonResponse(responseData)

        #RETURN RESPONSE
    else:
        responseData = {}
        responseData['result'] = 'ERROR'
        responseData['message'] = 'Invalid Request'
        return JsonResponse(responseData, status=400)

def makepassword(request,password):
    hashPassword = make_password(password)
    response_data = {}
    response_data['password'] = hashPassword
    return JsonResponse(response_data, status=200)


def checkJson(myJson):
    try:
        json_object = json.loads(myJson)
    except ValueError as e:
        return False
    return True


def list(request):

            #VALIDATE METHOD
            if request.method == 'POST':

                #DECLARE RESPONSE
                responseData = {}
                msgError = ""
                detectedError = False


                #Checamos que este este el header
                if  request.headers.get("user-api-key") == None:
                    responseData['result'] = 'ERROR'
                    responseData['message'] = 'Requires ApiKey'
                    return JsonResponse(responseData,status=400)

                #CHECK JSON STRUCTURE
                validateJson = checkJson(request.body)
                if (validateJson):
                    jsonBody = json.loads(request.body)

                #CHECK JSON CONTENT
                    if "user" not in jsonBody:
                        msgError = "Requires User"
                        detectedError = True
                    elif "password" not in jsonBody:
                        msgError = "Requires Password"
                        detectedError = True
                #CHECK IF USER EXITST
                    else:
                        try:
                            currentUser = ApiUsers.objects.get(user = jsonBody['user'])
                        except Exception as e:
                            msgError = "The user does not exist or the password is incorrect"
                            detectedError = True
                            responseData['result'] = 'ERROR'
                            responseData['message'] = msgError
                            return JsonResponse(responseData,status=401)


                #TAKE PASSWORD OF THE USER
                        passJsonBody = jsonBody['password']
                        currentUserPass = currentUser.password


                #CHECK IF PASSWORD IS CORRECT
                        if not check_password(passJsonBody,currentUserPass):
                            msgError = "The user does not exist or the password is incorrect"
                            detectedError = True

                #Comparar la apiKey introducida con la de la base de datos. S+i es correcta mostrart la vista
                        elif currentUser.api_key == request.headers["user-api-key"]:
                                    responseData['result'] = 'SUCCESS'
                                    responseData['movie'] = {}
                                    cont = 0
                                    for i in Movie.objects.all():
                                        responseData["movie"][cont] = {}
                                        responseData["movie"][cont]["id"] = i.movieid
                                        responseData["movie"][cont]['name'] = i.movietitle
                                        responseData["movie"][cont]['image'] = i.imageurl
                                        responseData["movie"][cont]['decription'] = i.description
                                        cont = cont + 1
                                    return JsonResponse(responseData,status=200)

                        else:
                            responseData['result'] = 'ERROR'
                            responseData['message'] = 'Invalid Api-key'
                            return JsonResponse(responseData,status=401)


                    if detectedError == True:
                            responseData['result'] = 'ERROR'
                            responseData['message'] = msgError
                            detectedError = False
                            return JsonResponse(responseData,status=401)

                else:
                    responseData['result'] = 'ERROR'
                    msgError = "Invalid JSON Format"
                    responseData['message'] = msgError
                    return JsonResponse(responseData)

                #RETURN RESPONSE
            else:
                responseData = {}
                responseData['result'] = 'ERROR'
                responseData['message'] = 'Invalid Request'
                return JsonResponse(responseData, status=400)
