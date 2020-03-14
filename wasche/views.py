from PIL import Image
import cv2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pyzbar.pyzbar as pyzbar
from django.shortcuts import render
from delivery_executives.models import Deliver_Executive
import json
import base64
import io
import numpy as np
import os
import requests
import pyqrcode
# import keras
# from keras.preprocessing import image
# from keras.applications import imagenet_utils
# from keras.applications.mobilenet import preprocess_input
# from keras.applications import MobileNet
# import win32print
# import win32ui
from PIL import ImageWin
# import cv2

#mobile = keras.applications.mobilenet.MobileNet()


root_url = "http://wasche-services.herokuapp.com"
root_url = "http://localhost:8000"
tot = 0
classes = {
    "Upper Wear":[
"jersey",
"military_uniform",
"stole",
"sweatshirt",
"trench_coat"
    ],
    "Lower Wear":[
"hoopskirt",
"jean",
"miniskirt",
"overskirt"
    ],
    "Inner Wear":[
        "bikini",
        "brassiere",
        "swimming_trunks",
        "diaper"
    ],
    "Other":[
        "apron",
        "bath_towel",
        # "bow_tie",
        "cardigan",
        "doormat",
        "fur_coat",
        "handkerchief",
        "lab_coat",
        "maillot",
        "mitten",
        "velvet",
        "neck_brace",
        "vestment",
        "guacamole",
        "pajama",
        "poncho",
        "quilt",
        "theater_curtain",
        "sarong",
        "shower_curtain",
        "sock",
        "suit"
    ],
    "Full Wear":[
        "gown",
        "kimono"
    ]
}

c2 = {
	"Lower Wear":[
	"leg",
	"jean",
	"jeans",
	"trouser",
	"pants",
	"denim",
	"standing"
	],
	"Inner Wear":[
	"pantie",
	"lingerie",
	"diaper",
	"top",
	"undergarment",
	"bra",
	"brassiere",
	"protective garment"
	
	],
	"Upper Wear":[
	"suit",
	"jacket",
	"jersey",
	"bulletproof vest",
	"apron",
	"shirt","sleeve","top","t-shirt"
	],
	"Other":[
	"womans's clothing",
	"tie",
	"garment",
	"fashion",
	"dress",
	"clothing",
	"clothes",
	"full",
	"outfit",
	"dressed"
	]
	
}
api_key = 'acc_24f50e74ddbaf36'
api_secret = 'c234ca7dec045a9235ecb19e8dbf7a3b'

# def process_image_and_detect(imagepath):
  
  
#   img = image.load_img(img_path, target_size=(299, 299))
#   x = image.img_to_array(img)
#   timg = cv2.cvtColor(x,cv2.COLOR_BGR2GRAY)
#   c = timg>=90
#   if np.count_nonzero(c)>=42000:
    

#     x = np.expand_dims(x, axis=0)
#     x = preprocess_input(x)

#     preds = minsr.predict(x)
#     preds =  decode_predictions(preds, top=3)[0][0]
#     if preds[2]>0.5:
#       for i,j in classes.items():
#         if preds[1] in j:
#           txt = "\nDetected   :  " + preds[1] + "\n\nConfidence  :  "  +  str(preds[2]) + "\n" + i
#           return [i,txt]
#   else:
#     return []
#   return []

def process_image_and_detect_imagga(filename):
  acc=50
  response = requests.post(
      'https://api.imagga.com/v2/tags?limit=10',
      auth=(api_key, api_secret),
      files={'image': open(filename, 'rb')})

  res = response.json()
  if "result" in res:
    res = res["result"]["tags"]
    f=False
    while True:
      for i in res:
        if (i["tag"]["en"] in c2["Lower Wear"]):
          if i["confidence"]>=acc:
            if not (i["tag"]["en"]=="standing" and i["confidence"]>=44):						
              f=True
              txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nLower Wear"
              return ["Lower Wear",i["confidence"]]
            
        elif i["tag"]["en"] in c2["Upper Wear"]:
          if i["confidence"]>=acc:
            f=True
            txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nUpper Wear"
            return ["Upper Wear",i["confidence"]]
        
        elif i["tag"]["en"] in c2["Inner Wear"]:
          if i["confidence"]>=acc:
            f=True
            txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nInner Wear"
            return ["Inner Wear",i["confidence"]]
        
      if f==True:
        break
      else:
        acc = acc-5
      if acc<=10:
        break
    acc=50
    if f==False:
      while True:
        for i in res:
          if i["tag"]["en"] in c2["Other"]:
            if i["confidence"]>=acc:
              f=True
              txt = "\nDetected   :  " + i["tag"]["en"] + "\n\nConfidence  :  "  +  str(i["confidence"]) + "\nOther"
              return ["Other",i["confidence"]]
              
        if f==True:
          break
        else:
          acc = acc-5
        if acc<=10:
          break
  else:
    return []
  return []


@csrf_exempt
def p1(request):
    path = os.path.abspath(".") + "\\wasche\\" + request.POST["path"]
    path = path.replace("\\","/")
    print(path)
    # img = Image.open(request.POST["path"])
    img = cv2.imread(path)
    img = cv2.resize(img,(140,140))
    print(img.shape)
    decoded = pyzbar.decode(img)
    print(decoded)
    if len(decoded)>=1:
        dd = decoded[0].data.decode('utf-8')
        
        if "wasche-services" in dd:
            ddd = json.loads(dd)
            ddd = ddd["wasche-services"] 
            res = requests.post(root_url+"/api/notify_initial/",data={"data":json.dumps({"name":ddd["name"],"id":ddd["id"],"type":"initial","msg":"Hey Laundrer, The Delivery Executive is on his way make sure you have your clothes ready.","title":"Notification"})})
            if res.text=="Success":
                print("Successs")
                de = Deliver_Executive.objects.get(id=int(ddd["id"]),name = ddd["name"])
                cn = de.contract_name.contract_name
                return HttpResponse(json.dumps({"name":ddd["name"],"dest":cn}))
            else:
                print("There was an error please contact the technical department.")
                return HttpResponse("There was an error please contact the technical department.")
        else:
            return HttpResponse("Not Found")

    else:
        return HttpResponse("Not Found")

def process(request):
    return render(request,"process.html")

def process2(request):
    return render(request,"process2.html")


def process_image(user,filename):
  
  if user["cred"]["email"]!="":
    result = process_image_and_detect_imagga(filename)
    print(result)
    if len(result)>0:
      # for i,j in classes.items():
      #   if result in j:
          # predicted = i
      # found = True
      data = user["cred"]
      # data["data"] = i
      data["data"] = result[0]
      
      qr = pyqrcode.create(json.dumps(data))
      qr.png("qrcode_"+ str(user["data"]["t"]) + "_" + result[0] +".png",scale=8)
      
      # text = "Detected {} => {}".format(result,i)

      # cv2.putText(frame, text, (10, 10),
      #     cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
      user["data"]["t"] = user["data"]["t"] + 1
      user["data"][result[0]] = user["data"][result[0]] + 1
      return result
  return ""

from application.models import Plans
from user.models import User
from datetime import datetime
from wasche.custom_settings import settings as cust_settings
def detect_user(img,user):
  decoded = pyzbar.decode(img)
  print("calling")
  print(decoded)
  if len(decoded) >= 1:
    dd = decoded[0].data.decode('utf-8')
    # print("saasddssad")
    print(dd)
    print("\n\nPrevious user  :  ",user["cred"]["email"],"\n\n")
    if "email" in dd:
      dd = json.loads(dd)
      try:
        print("Found Email : ",dd["email"])
        if user["cred"]["email"]!=dd["email"]:
          print("Modifying Existing user")
          u = User.objects.get(email=dd["email"])
          p = Plans.objects.get(user=u)
          print(datetime.strptime(datetime.now(tz=cust_settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p"))
          diff = p.end_date - datetime.strptime(datetime.now(tz=cust_settings.ist_info).strftime("%Y-%m-%d %H:%M:%S %p"),"%Y-%m-%d %H:%M:%S %p")
          print(diff)
          if diff.days<0:
            user["cred"]["email"] = dd["email"]
            return {"res":True,"p":False,"u":u}
          elif diff.days==0:
            user["cred"]["email"] = dd["email"]
            return {"res":True,"p":False,"u":u}
          else:
            
            # if dd["email"] != user["cred"]["email"]:
              # if user["cred"]["email"]!="":
              #   user["type"] = "po"
              #   user["data"]["p"] = True
              #   user["data"]["t"] = user["data"]["t"] + 1
              #   user["msg"] = "Your order has been processed."
              #   user["data"]["start"] = False
              #   user["title"] = "Order Details"
              #   req = requests.post(root_url+"/dashboard/update/",data={"user":json.dumps(user)})

                # print(req)
                
                # print_image("qrcode.png")
        
            user["data"] = {"Upper Wear":0,"Lower Wear":0,"Inner Wear":0,"Other":0}
            user["cred"]["email"] = dd["email"]
            user["cred"]["contract_name"] = dd["contract_name"]
            user["cred"]["contract_address"] = dd["contract_address"]
            user["cred"]["first_name"] = dd["first_name"]
            user["cred"]["last_name"] = dd["last_name"]
            user["cred"]["gender"] = dd["gender"]
            user["type"] = "co"
            user["data"]["start"] = True
            user["data"]["s"]=0
            user["data"]["c"]=0
            user["data"]["f"]=0
            user["data"]["t"] = 0
            # text = "User  :  {}".format(user["cred"]["email"])

            # cv2.putText(img, text, (10, 10),
            # cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
            print(user)
            req = requests.post(root_url+"/dashboard/update_new/",data={"user":json.dumps(user)})
            # print(req)
            print(req.text)
            req = req.json()
            user["date"] = req["date"]
            user["time"] = req["time"]
            return {"res":True,"p":True}
      except Exception as exp:
        print("Error while finding data : " , exp)

  return {"res":False,"p":False}

def notifyUser(t,user_n,f,tit,msg,onesig):
    data = {"t":t,"e":user_n,"f":f,"tit":tit,"msg":msg,"onesignal":onesig}
    req = requests.post("https://wasche-services.herokuapp.com/dashboard/user_notification/",data={"data":json.dumps(data)})
    print(req.text)

@csrf_exempt
def search_user(request):
    imgstr = json.loads(request.POST["data"])
    imgstr = imgstr["img"]
    imgstr = imgstr.replace(" ","+")
    image_bytes = io.BytesIO(base64.b64decode(imgstr))
    im = Image.open(image_bytes)
    im.save("qr.png")
    user =  json.loads(request.POST["user"])
    arr = np.array(im)[:,:]
    print(user)
    u= detect_user(arr,user)
    print("Result  :  ",u,user)
    
    if u["res"]==True:
        if u["p"]==False:
            notifyUser("tracking",user["cred"]["email"],"Admin","Wrong Order","We received order for the plan expired.",True)
        return HttpResponse(json.dumps({"user":user,"res":{"res":u["res"],"p":u["p"]}}))
    return HttpResponse("no")


@csrf_exempt
def detect_cloth(request):
    path = os.path.abspath(".") + "/" + request.POST["path"]
    path = path.replace("\\","/")
    user = json.loads(request.POST["user"])
    print(path)
    result = process_image(user,path)
    res = "Not Detected"
    if result!="":
        res = "{}  -  {:.2f}%".format(result[0],result[1])
        # res = result[0] + "  -  " + str(result[1])
    return HttpResponse(json.dumps({"user":user,"res":res}))

from delivery_executives.models import Deliver_Executive,ongoing_delivery

@csrf_exempt
def complete_order(request):
    users = json.loads(request.POST["user"])
    for user in users:
        try:
            user["type"] = "pd"

            user["data"]["p"] = False
            user["data"]["s"] = user["data"]["t"]
            user["data"]["c"] = 1
            user["msg"] = "Your order has completed. It may reach you in another 2 hours."
            user["data"]["start"] = False
            user["title"] = "Order Details"
            # print("\n\nSaving : ",user,"\n\n")
            req = requests.post(root_url+"/dashboard/update_data/",data={"user":json.dumps(user)})
        except Exception as exp:
            print("Error :  ",exp)

    return HttpResponse("complete")

from dashboard.views import onsignal
from user.models import Notifications
from tracking_system.models import Tracker
@csrf_exempt
def update_tracker(request):
    user = json.loads(request.POST["user"])
    print("Type   :  ",request.POST["type"])
    if request.POST["type"] == "po":
      try:
        
        ded = Deliver_Executive.objects.filter(contract_name = user["cred"]["contract_name"])
        for dedd in ded:
          deod = ongoing_delivery.objects.filter(name=dedd)
          for deodd in deod:
            if deodd.on_going=="initialized":
              deodd.on_going = "Processing Order"
              deodd.save()
          user["type"] = "po"
          user["data"]["p"] = False
          user["data"]["s"] = user["data"]["t"]
          user["data"]["c"] = 1
          user["msg"] = "Your order has been processed."
          user["data"]["start"] = False
          user["title"] = "Order Details"
          # print("\n\nSaving : ",user,"\n\n")
          req = requests.post(root_url+"/dashboard/update_data/",data={"user":json.dumps(user)})
      except Exception as exp:
          print("Error :  ",exp)
    elif request.POST["type"] == "di":
      try:
        ded = Deliver_Executive.objects.filter(contract_name = user["cred"]["contract_name"])
        for dedd in ded:
          deod = ongoing_delivery.objects.filter(name=dedd)
          for deodd in deod:
            if deodd.on_going=="Processing Order":
              deodd.on_going = "Started Delivery"
              deodd.save()
        u = User.objects.get(email=user["cred"]["email"])
        t = Tracker.objects.filter(track_id = u,date = user["date"],time=user["time"])
        dat = {}
        
        print(len(t))
        for ii in t:
            ii.update_operation({"type":"di"})
            ii.save()
        notifyUser("tracking",user["cred"]["email"],"Admin","Order Information","Your order has completed. It may reach you in another 2 hours.",True)
        
      except Exception as exp:
        print("Error  :  ",exp)
    elif request.POST["type"] == "pd":
      try:
        
        ded = Deliver_Executive.objects.filter(contract_name = user["cred"]["contract_name"])
        for dedd in ded:
          deod = ongoing_delivery.objects.filter(name=dedd)
          for deodd in deod:
            if deodd.on_going=="Started Delivery":
              deodd.on_going = "Completed Delivery"
              deodd.save()
        u = User.objects.get(email=user["cred"]["email"])
        t = Tracker.objects.filter(track_id = u,date = user["date"],time=user["time"])
        dat = {}
        
        print(len(t))
        for ii in t:
            ii.update_operation({"type":"pd"})
            ii.save()
        notifyUser("tracking",user["cred"]["email"],"Admin","Order Conpletion","Hey, your order has arrived.",True)
        
      except Exception as exp:
        print("Error  :  ",exp)
    elif request.POST["type"] == "qc":
      try:
        u = User.objects.get(email=user["cred"]["email"])
        t = Tracker.objects.filter(track_id = u,date = user["date"],time=user["time"])
        dat = {}
        
        print(len(t))
        for ii in t:
            ii.update_operation({"type":"qc"})
            ii.save()
        # noti = Notifications(type_msg = "tracking",email = u,sent_from = "Admin",title = "Order Conpletion",msg="Hey, your order has arrived.",seen=False)
        # noti.save()
        # onsignal("Your order has been recieved at our warehouse. You can track the order details in tracking page.",u)
        # onsignal("Hey, your order has arrived.",u)
      except Exception as exp:
        print("Error  :  ",exp)
    return HttpResponse("complete")


    return HttpResponse("complete")



from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
def upload_detect(request):
  res = "Not Detected"
  try:
    # file_to_up = request.FILES["image"]
    image = request.FILES['image']
    # print(file_to_up)
    print(request.FILES)
    tmp_file = os.path.join("", image.name)
    path = default_storage.save(tmp_file, ContentFile(image.read()))
    print(path)
    result = process_image_and_detect_imagga("media/"+path)
    print(result)
    if len(result)>0:
      if result!="":
          return HttpResponse(json.dumps({"c":result[0],"a":"{0:.2f}".format(result[1]),"path":path}))
          # res = result[0] + "  -  " + str(result[1])
  except Exception as err:
    print(err)
    

  return HttpResponse(json.dumps({"c":res,"path":path}))

def detect_file_url(request):
  return render(request,"detector.html")
