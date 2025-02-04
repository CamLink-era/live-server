from django.shortcuts import render
from live.models import Live

import shutil
import os
import json
import socket
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def link(request):
  try:
    if request.method == 'POST':
      try:
        data = json.loads(request.body)
        code = data['code']
        
        user = Live(code=code)
        user.save()

        request.session['uid'] = user.id


        os.makedirs(f"live/videos/{user.id}")

        response = JsonResponse({'msg' : 'success'})

        return response
      
      except Exception as e:
        return JsonResponse({'msg':str(e)})
    else:
      return JsonResponse({'msg':'Method not supported'})

  except:
    return JsonResponse({'msg':'Unexpected error'})















@csrf_exempt
def stream(request):
  try:   

    if request.method == "POST":
      try:
          
        chunk = request.FILES['chunk']

        id = request.session.get("uid")

        number = Live.objects.filter(id = id)[0]

        path1 = os.getcwd() + f"/live/videos/{id}/{number.number}.webm"

        with open(path1,'ab') as video:
          video.write(chunk.read())

          

        number.number = number.number + 1
        number.save()



        return JsonResponse({'msg':'success'})

      except Exception as e:
        return JsonResponse({'msg':str(e)})

    else:
        return JsonResponse({'msg':"method not supported"})


  except:
    return JsonResponse({'msg':"Unexpected error"})























@csrf_exempt
def refresh(request):
  try:   

    if request.method == "GET":
      try:

        users = Live.objects.all()

        live_hosts = []

        for i in users:
          live_hosts.insert(0,i.id)

        if live_hosts == []:
          return JsonResponse({'msg':'no new link'})

        return JsonResponse({'msg':'success','live':live_hosts})

      except Exception as e:
        return JsonResponse({'msg':str(e)})

    else:
        return JsonResponse({'msg':"method not supported"})


  except:
    return JsonResponse({'msg':"Unexpected error"})




















@csrf_exempt
def play(request):
  try:   

    if request.method == "GET":
      try:
          
        data = json.loads(request.body)

        uid = data['uid']
        cid = data['cid']

        #return the requested chunk of video
        
        
        path = os.getcwd() + f"/live/videos/{uid}/{cid}.webm"

        chunk = open(path, 'rb')

        return FileResponse(chunk, content_type='video/webm')
        
      except FileNotFoundError:
        return JsonResponse({'msg':'again'})
      except Exception as e:
        return JsonResponse({'msg':str(e)})

    else:
        return JsonResponse({'msg':"method not supported"})


  except:
    return JsonResponse({'msg':"Unexpected error"})



















@csrf_exempt
def stop(request):
  try:
    if request.method == "POST":
      
      uid = request.session.get('uid')
      
      #Delete User
      Live.objects.filter(id=uid)[0].delete()
      
      #Delete folder based on User ID name
      shutil.rmtree(os.getcwd() + f"/live/videos/{uid}")
      
      return JsonResponse({'msg': 'success'})
        
    
    else:
      return JsonResponse({'error': 'Method is not allowed.'}, status=405)
  
  except Exception as e:
    return JsonResponse({'error': 'Unexpected error', 'details': str(e)}, status=500)



















@csrf_exempt
def home(request):
  try:
    if request.method == 'GET':
      try:

        livelist = []

        for i in Live.objects.all():
          livelist.insert(0,i.id)

        return render(request, 'home.html', {"live":livelist, "url":f"http://{socket.gethostbyname(socket.gethostname())}:8800/live/streaming/"})
      
      except Exception as e:
        return JsonResponse({'msg':str(e)})
    else:
      return JsonResponse({'msg':'Method not supported'})

  except:
    return JsonResponse({'msg':'Unexpected error'})








@csrf_exempt
def streaming(request):
  try:
    if request.method == 'GET':
      try:
        return render(request, 'stream.html')
      
      except Exception as e:
        return JsonResponse({'msg':str(e)})
    else:
      return JsonResponse({'msg':'Method not supported'})

  except:
    return JsonResponse({'msg':'Unexpected error'})


