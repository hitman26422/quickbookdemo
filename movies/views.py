from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from random import *
from datetime import date, datetime
import urllib.request
import urllib.parse
import json
import smtplib

import base64
from django.core.files.storage import FileSystemStorage

@csrf_exempt
def upmovie(request):
    if request.method == 'POST':
         loc=request.POST['loc']
         date=request.POST['dated']
         name=request.POST['mname']
         client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
         db=client.movies
         result=db.moviename.update({"NAME":name},{'$set': {"LOCATIONS":[]}})
         if result:
            date=date+"T18:30:00.000Z"
            new = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S.000Z')
            li = list(loc.split(","))
            res=[]
            for i in li:
                res.append(int(i))
            result=db.moviename.update({"NAME":name},{'$set': {"LOCATIONS":res,"ENDDATE":new}})   
            if result:
                context="ok"
            else:
                context="fail"
         else:
            context="fail"
         return HttpResponse(context)        
    if request.method == 'GET':
         name=request.GET['mname']
         client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
         db=client.movies
         result=db.moviename.remove( { "NAME": name })
         if result:
            context="ok"
         else:
            context="fail"
         return HttpResponse(context)        
         
@csrf_exempt
def getenddate(request):
    if request.method == 'GET':
         mname=request.GET['name']
         client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
         db=client.movies
         result=db.moviename.find({"NAME":mname})
         date="OK"
         for y in result:
            date=json_serial(y['ENDDATE'])
         return HttpResponse(date) 
    if request.method == 'POST':
         date=request.POST['date']
         client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
         db=client.movies
         locid=request.session["location"];
         getscreen=db.theatre.find({"locationid":int(locid)})
         find=False
         find1=False
         find2=False
         timings=[]
         newtimings=[]
         screens=[' 8:30am SCREEN1',
    '9:00am SCREEN2',
    '9:30am SCREEN3',
    '10:30am SCREEN1',
    '12:15pm SCREEN2',
    '12:30pm SCREEN3',
    '3:00pm SCREEN1',
    '3:30pm SCREEN2',
    '4:30pm SCREEN3',
    '6:30pm SCREEN1',
    '7:30pm SCREEN2',  '7:15pm SCREEN3' , '6:30pm SCREEN2']
         if getscreen:
                    for x in getscreen:
                        for y in x['screen1']:
                            if  y.find(date) != -1: 
                                key=y.replace(date, '')
                                timings.append(key)
                                find=True
                        for y in x['screen2']:
                            if y.find(date) != -1: 
                                key=y.replace(date, '')
                                timings.append(key)
                                find1=True
                        for y in x['screen3']:
                            if y.find(date) != -1: 
                                key=y.replace(date, '')
                                timings.append(key)
                                find2=True
                    if find ==True or find2 == True or find1 == True:
                            for list2 in screens:
                                if  any(list2 in s for s in timings):
                                    None
                                else:
                                    newtimings.append(list2)
                            context=json.dumps(newtimings)
                    else:
                        context="ok"
         return HttpResponse(context)

@csrf_exempt
def updatescreen(request):
    if request.method == 'POST':
         mname=request.POST['mname']
         screen=request.POST['location']
         date=request.POST['dated']
         li = list(screen.split(","))
         screen1=[]
         screen2=[]
         screen3=[]
         for l in li:
             l=date+" "+mname+" "+l
             t=l[-7:];
             if t == "SCREEN1":
                screen1.append(l)
             if t == "SCREEN2":
                screen2.append(l)
             if t == "SCREEN3":
                screen3.append(l)
         result=False
         client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
         db=client.movies
         location=db.theatre.find({"$and":[{"locationid":int(request.session["location"]),"moviename":mname}]}).count()
         if location == 0:
            result=db.theatre.update({"$and":[{"locationid":int(request.session["location"])}]},{ "$push" : { "moviename":mname } })
            if result:
                if screen1:
                    result=db.theatre.update({"$and":[{"moviename":mname,"locationid":int(request.session["location"])}]},{ "$push" : { "screen1": { "$each":screen1} } })
                if screen2:
                    result=db.theatre.update({"$and":[{"moviename":mname,"locationid":int(request.session["location"])}]},{ "$push" : { "screen2": { "$each":screen2} } })
                if screen3:
                    result=db.theatre.update({"$and":[{"moviename":mname,"locationid":int(request.session["location"])}]},{ "$push" : { "screen3": { "$each":screen3} } })
            if result:
                  context="ok"
            else:
                context="fail" 
         else:
            result=False
            if screen1:
                result=db.theatre.update({"$and":[{"moviename":mname,"locationid":int(request.session["location"])}]},{ "$push" : { "screen1": { "$each":screen1} } })
            if screen2:
                result=db.theatre.update({"$and":[{"moviename":mname,"locationid":int(request.session["location"])}]},{ "$push" : { "screen2": { "$each":screen2} } })
            if screen3:
                result=db.theatre.update({"$and":[{"moviename":mname,"locationid":int(request.session["location"])}]},{ "$push" : { "screen3": { "$each":screen3} } })
            print('false')
            if result:
                  context="ok"
            else:
                context="fail"
         print(context)
         return HttpResponse(context)

@csrf_exempt
def enter(request):
    if request.method == 'POST':
        locer=request.POST['getlocation']   
        request.session["location"]=locer
        client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
        db=client.movies
        result=db.moviename.find({"LOCATIONS":int(locer)})
        present = datetime.now()
        name=[]
        if result:
            for x in result:
                if x['ENDDATE'] >=present:
                    name.append(x['NAME'])
        if not name:
            context="no";
        else:
            context=json.dumps(name)
        return HttpResponse(context)
    
def uploads(request):
    if request.method == 'POST' and request.FILES['myfile']:
        moviename=request.POST['moviename']
        locer=request.POST['loca']
        date=request.POST['date']
        moviename=moviename.upper()
        client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
        db=client.movies
        exit=db.moviename.find({'NAME': moviename }).count()
        if exit== 0:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            with open(filename, "rb") as img_file:
                my_string = base64.b64encode(img_file.read())
            typefile=myfile.content_type
            my_string=my_string.decode("utf-8") 
            fs.delete(filename)
            url="data:"+typefile+";base64,"+my_string
            location=db.location.find()
            cities=[]
            idofcity=[]
            for y in location:
                cities.append(y['name'])
                idofcity.append(y['location_id'])
            cities=zip(cities,idofcity)
            date=date+"T18:30:00.000Z"
            new = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S.000Z')
            li = list(locer.split(","))
            res=[]
            for i in li:
                res.append(int(i))
            insert={'NAME':moviename,'IMAGE':url,'LOCATIONS':res,'ENDDATE': new}
            result=db.moviename.insert(insert)
            name=[]
            imgeurl=[]
            if result:
                result=db.moviename.find()
                present = datetime.now()
                if result:
                    for x in result:
                        if x['ENDDATE'] >=present:
                            imgeurl.append(x['IMAGE'])
                            name.append(x['NAME'])
                            cinname=x['NAME']
                        if len(imgeurl) == 0:
                            moviestate="no"
                        else:
                            moviestate=zip(imgeurl,name)
                        context={
                        "locations":cities,
                        "movies":moviestate,
                        'uploaded_file_url':url
                        }
            else:
                result=db.moviename.find()
                present = datetime.now()
                if result:
                    for x in result:
                        if x['ENDDATE'] >=present:
                            imgeurl.append(x['IMAGE'])
                            name.append(x['NAME'])
                            cinname=x['NAME']
                        if len(imgeurl) == 0:
                            moviestate="no"
                        else:
                            moviestate=zip(imgeurl,name)
                context={
                   "movies":moviestate,
                    "locations":cities,
                }
        else:
            name=[]
            imgeurl=[]
            result=db.moviename.find()
            present = datetime.now()
	    moviestate=None
            if result:
                for x in result:
                    if x['ENDDATE'] >=present:
                        imgeurl.append(x['IMAGE'])
                        name.append(x['NAME'])
                        cinname=x['NAME']
                        if len(imgeurl) == 0:
                            moviestate="no"
                        else:
                            moviestate=zip(imgeurl,name)
            location=db.location.find()
            cities=[]
            idofcity=[]
            for y in location:
                cities.append(y['name'])
                idofcity.append(y['location_id'])
            cities=zip(cities,idofcity)
            context={
            "locations":cities,
            "movies":moviestate,
            'exist':"yes"
            }
        return render(request, 'tesr.html',context)
    else :
        name=[]
        imgeurl=[]
        client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
        db=client.movies
        location=db.location.find()
        cities=[]
        idofcity=[]
        for y in location:
            cities.append(y['name'])
            idofcity.append(y['location_id'])
        cities=zip(cities,idofcity)
        result=db.moviename.find()
        present = datetime.now()
        if result:
            for x in result:
                if x['ENDDATE'] >=present:
                    imgeurl.append(x['IMAGE'])
                    name.append(x['NAME'])
                    cinname=x['NAME']
                    if len(imgeurl) == 0:
                        moviestate="no"
                    else:
                        moviestate=zip(imgeurl,name)
        context={
        "locations":cities,
        "movies":moviestate,
        }
    return render(request, 'tesr.html',context)

def admin(request):
        if request.session.has_key('email') and request.session['email']=="naveenusharma@gmail.com":
            client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
            db=client.movies
            location=db.location.find()
            cities=[]
            idofcity=[]
            name=[]
            imgeurl=[]	
            for y in location:
                cities.append(y['name'])
                idofcity.append(y['location_id'])
            cities=zip(cities,idofcity)
            result=db.moviename.find()
            present = datetime.now()
            if result:
                for x in result:
                    if x['ENDDATE'] >=present:
                        imgeurl.append(x['IMAGE'])
                        name.append(x['NAME'])
                        cinname=x['NAME']
                if len(imgeurl) == 0:
                    moviestate=None
                else:
                    moviestate=zip(imgeurl,name)
            context={
            "locations":cities,
            "movies":moviestate,
            }
            return render(request, 'tesr.html',context)
        else:
            return render(request, 'index.html')            


a = []
for k in range(1,21):
    a+= [k]

colum=[]
alpha = 'a'
for i in range(0,15): 
    colum.append(alpha) 
    alpha = chr(ord(alpha) + 1) 

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

@csrf_exempt
def sendseattomob(request):
	if request.method == 'POST':
			movietimeandscreen=request.POST.get('timeandscreen')
			moviedate=request.POST.get('sdate')
			moviename=request.POST.get('name')
			movieseats=request.POST.get('sseats')
			loc=request.POST.get('location')
			src=request.POST.get('src')
			cash=request.POST.get('cash')
			remain=request.session["wallet"]-int(cash);
			theatreid=request.session["theatreid"]
			mobile=request.session['mobile']
			message="THANKS FOR USING QUICK BOOK \n"+moviename+"\n"+loc+"\n"+moviedate+"\n"+movietimeandscreen+"\nseats:"+movieseats+"amount:"+cash
			p =  sendapi('Ok2xjxr8mFM-qpeKpJXJ04vsL80zRJn4t8KKxpsgGM',mobile,message)
			global status,context,data,reval
			context=None
			status=None
			print(p)
			data = p.decode('utf-8')
			reval=json.loads(data)
			names= extract_values(reval, 'status')
			for x in names:
				status=x
			if status=="failure":
				context='NO'
			elif status=="success":
				context='OK'
			else:
				context='no'			
			return HttpResponse(context)		

@csrf_exempt
def checkseats(request):
		if request.method == 'POST':
			movietimeandscreen=request.POST.get('timeandscreen')
			moviedate=request.POST.get('sdate')
			moviename=request.POST.get('name')
			movieseats=request.POST.get('sseats')
			src=request.POST.get('src')
			cash=request.POST.get('cash')
			remain=request.session["wallet"]-int(cash);
			theatreid=request.session["theatreid"]
			global context
			context="fail"
			client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
			db=client.movies
			screen=movietimeandscreen[-7:];
			movieseats=movieseats.split(',')
			getallocation=db.screen.find({"$and":[{"showtime":movietimeandscreen,"DATE":moviedate,"theatreid":theatreid}]}).count()
			if getallocation==0:
				insert=db.screen.insert({"showtime":movietimeandscreen,"DATE":moviedate,"theatreid":theatreid, screen:movieseats})
				if insert:
					context="ok"
					inserto=db.booking.insert({"email":request.session['email'],"moviename":moviename,"mobile":request.session['mobile'],"showtime":movietimeandscreen,"src":src,"DATE":moviedate,"theatreid":theatreid, screen:movieseats,"amount":int(cash)})	
					if inserto:
						if db.login.update_one({"email":request.session['email']},{"$set":{"wallet":int(remain)}}):
								context="ok"
								request.session["wallet"]=int(remain);
						context="ok"
			else:
				listofscreen=[]
				getallocation=db.screen.find({"$and":[{"showtime":movietimeandscreen,"DATE":moviedate,"theatreid":theatreid}]})
				for x in getallocation:
					listofscreen.append(x[screen])
				if movieseats in listofscreen: 
					update=db.screen.update({"$and":[{"showtime":movietimeandscreen,"DATE":moviedate,"theatreid":theatreid}]},{ "$push" : { screen: { "$each":movieseats} } })
					if update:
						insert=db.booking.insert({"email":request.session['email'],"moviename":moviename,"mobile":request.session['mobile'],"showtime":movietimeandscreen,"src":src,"DATE":moviedate,"theatreid":theatreid, screen:movieseats,"amount":int(cash)})	
						if insert:
							if db.login.update_one({"email":request.session['email']},{"$set":{"wallet":int(remain)}}):
								context="ok"
								request.session["wallet"]=int(remain);
		return HttpResponse(context)						
@csrf_exempt
def getscreendetails(request):
		if request.method == 'POST':
			movietime=locations=request.POST.get('screenandtime')
			moviedate=request.POST.get('moviedate')
			selectedseats=[]
			client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
			db=client.movies
			getallocation=db.screen.find({"$and":[{"showtime":movietime,"DATE":moviedate,"theatreid":request.session["theatreid"]}]})
			screen=movietime[-7:];
			for x in getallocation:
				selectedseats.append(x[screen])
			selectedseats=json.dumps(selectedseats)
			return HttpResponse(selectedseats)								
@csrf_exempt
def getscreening(request):
        if request.method == 'POST':
            locations=request.POST.get('locationid')
            moviename=request.POST.get('moviename')
            client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
            db=client.movies
            if request.POST.get('moto'):
                getscreen=db.theatre.find({"$and":[{"locationid":int(locations),"moviename":moviename}]})
                timings=[]
                find=False
                find1=False
                find2=False
                if getscreen:
                    for x in getscreen:
                        for y in x['screen1']:
                            if (y.find(moviename) != -1): 
                                timings.append(y.strip(moviename))
                                find=True
                        for y in x['screen2']:
                            if (y.find(moviename) != -1): 
                                timings.append(y.strip(moviename))
                                find1=True
                        for y in x['screen3']:
                            if (y.find(moviename) != -1): 
                                timings.append(y.strip(moviename))
                                find2=True
                        request.session["theatreid"]=x['theatreid']
                    if find ==True or find2 == True or find1 == True:
                        get=request.session[moviename]
                        timings.append(get)
                        timings=json.dumps(timings)
                else:
                    timings="NO"
                if not timings:
                    timings="NO"

                return HttpResponse(timings)                    
            if request.POST.get('dateend'):
                locations=request.POST.get('locationid')
                moviename=request.POST.get('moviename')
                date=request.POST.get('dateend')
                client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
                db=client.movies
                getscreen=db.theatre.find({"$and":[{"locationid":int(locations),"moviename":moviename}]})
                timings=[]
                find=False
                find1=False
                find2=False
                if getscreen:
                    for x in getscreen:
                        for y in x['screen1']:
                            if (y.find(moviename) != -1) and (y.find(date) != -1): 
                                key=y.replace(moviename,'')
                                key=key.replace(date, '')
                                timings.append(key)
                                find=True
                        for y in x['screen2']:
                            if (y.find(moviename) != -1) and (y.find(date) != -1): 
                                key=y.replace(moviename,'')
                                key=key.replace(date, '')
                                timings.append(key)
                                find1=True
                        for y in x['screen3']:
                            if (y.find(moviename) != -1) and (y.find(date) != -1): 
                                key=y.replace(moviename,'')
                                key=key.replace(date, '')
                                timings.append(key)
                                find2=True
                                request.session["theatreid"]=x['theatreid']
                    if find ==True or find2 == True or find1 == True:
                        get=request.session[moviename]
                        timings.append(get)
                        timings=json.dumps(timings)
                else:
                    timings="NO"
                if not timings:
                    timings="NO"
   
                return HttpResponse(timings)                    
	
@csrf_exempt
def getmovies(request):
    if request.session.has_key('username'):
        if request.method == 'GET':
            locations=request.GET.get('locationid')
            client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
            db=client.movies
            location=db.location.find()
            cities=[]
            idofcity=[]
            for y in location:
                cities.append(y['name'])
                idofcity.append(y['location_id'])
            cities=zip(cities,idofcity)
            imgeurl=[]
            name=[]
            locname=db.location.find({"location_id":int(locations)})
            locnameend=" "
            for l in locname:
                locnameend=l['name']
            result=db.moviename.find({"LOCATIONS":int(locations)})
            present = datetime.now()
            if result:
                for x in result:
                    if x['ENDDATE'] >=present:
                        imgeurl.append(x['IMAGE'])
                        name.append(x['NAME'])
                        cinname=x['NAME']
                        request.session[cinname]=json_serial(x['ENDDATE'])
                if len(imgeurl) == 0:
                    moviestate="no"
                else:
                    moviestate=zip(imgeurl,name)
            bookedmovies=db.booking.find({"email":request.session['email']})
            moviesbooked=[]
            showtime=[]
            date=[]
            seats=[]
            amount=[]
            moviename=[]
            src=[]
            bookedcount=0
            present = datetime.now().date()
            for l in bookedmovies: 
                date_time_obj = datetime.strptime(l['DATE'], '%Y-%m-%d')
                if date_time_obj.date()>=present:
                    if l['showtime']:
                        showtime.append(l['showtime'])
                        screen=l['showtime']
                        screen=screen[-7:];
                    if l['DATE']:
                        date.append(l['DATE'])      
                        bookedcount=bookedcount+1;
                    if l[screen]:
                        seats.append(l[screen])     
                    if l['moviename']:
                        moviename.append(l['moviename'])        
                    if l['src']:
                        src.append(l['src'])        
                    if l['amount']:
                        amount.append(l['amount'])
            moviesbooked=zip(showtime,date,seats,amount,moviename,src)
            context={
            'name':request.session['username'],
            'email':request.session['email'],
            'password':request.session['password'], 
            'verify':request.session['verify'],
            'mobile':request.session['mobile'],
            'loop':a,
            'loopinrow':colum,
            "locations":cities,
            'movies':moviestate,
            'locname':locnameend,
            'currentlocation':locations,
            "wallet":request.session['wallet'],
            'booked':moviesbooked,
            "count":bookedcount
            }
            return render(request, 'Modify/profile.html',context)
    else:
        return redirect(index)


@csrf_exempt
def updatepsw(request):
	if request.method == 'POST':
		email=request.POST.get('email')
		password=request.POST.get('psw')
		client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
		db=client.movies
		print(password)
		update=db.login.update_one({"email":email},{"$set":{"password":password}})
		if update:
			context='ok'
		else:
			context='fail'
		return HttpResponse(context)					
		
@csrf_exempt
def sendemail(request):
	if request.method == 'POST':
		token=request.POST.get('tokens')
		email=request.POST.get('email')
		msg = 'THIS MESSAGE IS FROM QUICK BOOK YOUR TOKEN IS.'+token
		seemail = "dcebatch28@gmail.com"
		password="Rohitvijay264"
		SUBJECT='CHANGE PASSWORD'
		message = 'Subject: {}\n\n{}'.format(SUBJECT, msg)
		server = smtplib.SMTP('smtp.gmail.com',587) #port 465 or 587
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(seemail,password)
		try:
			server.sendmail(seemail,email,message)
			server.close()
			context='ok'
		except:
			context='fail'
		return HttpResponse(context)					

@csrf_exempt
def changemobile(request):
	if request.method == 'POST':
		mobile=request.POST.get('mobile')
		email=request.POST.get('email')
		client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
		db=client.movies
		update=db.login.update_one({"email":email},{"$set":{"mobile":mobile,"verify":"false"}})
		if update:
			context='OK'
		else:
			context='fail'
		return HttpResponse(context)					
		
@csrf_exempt
def validateotp(request):
	if request.method == 'POST':
		otp=request.POST.get('otp')
		email=request.POST.get('email')
		client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
		db=client.movies
		result=db.otp.find({"$and":[ {"email": email ,"otp":int(otp)}]}).count()
		global context
		context=None
		if result==1:
			insert1={'email':email}
			result1=db.otp.delete_many(insert1)
			if result1:
				update=db.login.update_one({"email":email},{"$set":{"verify":"True"}})
				if update:
					context='OK'
				else:
					context='fail'
			else:
				context ='no'		
		else:
			context='no'
		return HttpResponse(context)					

@csrf_exempt
def deleteotp(request):
	if request.method == 'POST':
		email=request.POST.get('email')
		client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
		db=client.movies
		insert={'email':email}
		result=db.otp.delete_many(insert)
		if result:
			context ='ok'
		else:
			context ='fail'		
		print(context)
		return HttpResponse(context)		
		
def extract_values(obj, key):
	"""Pull all values of specified key from nested JSON."""
	arr = []

	def extract(obj, arr, key):
		"""Recursively search for values of key in JSON tree."""
		if isinstance(obj, dict):
			for k, v in obj.items():
				if isinstance(v, (dict, list)):
					extract(v, arr, key)
				elif k == key:
					arr.append(v)
		elif isinstance(obj, list):
			for item in obj:
				extract(item, arr, key)
		return arr

	results = extract(obj, arr, key)
	return results


def sendapi(apikey, numbers, message):
	data =  urllib.parse.urlencode({'apikey': apikey, 'numbers': numbers,
		'message' : message})
	data = data.encode('utf-8')
	request = urllib.request.Request("https://api.textlocal.in/send/?")
	f = urllib.request.urlopen(request, data)
	fr = f.read()
	return(fr)
 
#disabling csrf (cross site request forgery)
@csrf_exempt
def sendSMS(request):
	if request.method == 'POST':
		mobile=request.POST.get('MOBILE')
		otp=randint(000000, 999999);
		message='OTP FOR QUICK BOOK VERIFICATION OTP:'+str(otp)
		client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
		db=client.movies
		email=request.session['email']
		insert={'email':email,'otp':otp}
		result=db.otp.insert(insert)
		if result:
			p =  sendapi('Ok2xjxr8mFM-qpeKpJXJ04vsL80zRJn4t8KKxpsgGM',mobile,message)
			global status,context,data,reval
			context=None
			status=None
			print(p)
			data = p.decode('utf-8')
			reval=json.loads(data)
			names= extract_values(reval, 'status')
			for x in names:
				status=x
			if status=="failure":
				context='NO'
			elif status=="success":
				context='OK'
			else:
				context='no'			
		else:
				context='NO'
		return HttpResponse(context)	
	else:
		return HttpResponse('no')	
	 
#disabling csrf (cross site request forgery)
@csrf_exempt
def google(request):
	if request.method == 'POST':
			email=request.POST.get('e_name')
			client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
			db=client.movies
			insert={'email':email}
			result=db.login.find(insert)
			
			global demail,dpsw,name,verify,mobile
			demail=None
			dpsw=None
			name=None
			verify=None
			mobile=None
			wallet=None
			for x in  result:
				demail=(x['email'])
				dpsw=(x['password'])
				name=(x['name'])
				verify=(x['verify'])
				mobile=(x['mobile'])
				wallet=(x['wallet'])
			print(demail)
			print(dpsw)

			request.session['username'] =name
			request.session['password'] =dpsw
			request.session['email']=demail 
			request.session['verify']=verify 
			request.session['mobile']=mobile 
			request.session['wallet']=wallet
			if demail==email:
				context ='ok'
			else:
				context ='fail'
			if name == None:
				context='fail'
		#adding the values in a context variable 
			print(context)
		#getting our showdata template
			return HttpResponse(context)
	else:
		return render(request, 'index.html')

#disabling csrf (cross site request forgery)
@csrf_exempt
def checkdata(request):
	if request.method == 'POST':
			email=request.POST.get('e_name')
			client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
			db=client.movies
			insert={'email':email}
			result=db.login.find_one(insert)
			if result==None:
				context ='OK'
			else:
				context ='fail'
		#adding the values in a context variable 
			print(context)
		#getting our showdata template
			return HttpResponse(context)
	else:
		return render(request, 'Modify/register.html')
#disabling csrf (cross site request forgery)
@csrf_exempt
def signup(request):
	if request.method == 'POST':
			name=request.POST.get('name')
			email=request.POST.get('email')
			psw=request.POST.get('pw1')
			mobile=request.POST.get('mobile')
			client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
			db=client.movies
			insert={'name':name,'email':email,'mobile':mobile,'password':psw,'verify':'false','wallet':500}
			result=db.login.insert_one(insert)
			if result:
				context='OK'	
			else:
				context='NO'
			return HttpResponse(context)
	else:
		return render(request, 'Modify/register.html')

def index(request):
	if request.session.has_key('username'):
		return redirect(profile)
	else:
		return render(request, 'index.html')

def register(request):
		return render(request, 'Modify/register.html')


def profile(request):
        if request.session.has_key('username'):
            client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
            db=client.movies
            locations=db.location.find()
            cities=[]
            idofcity=[]
            for y in locations:
                cities.append(y['name'])
                idofcity.append(y['location_id'])
            cities=zip(cities,idofcity)
            bookedmovies=db.booking.find({"email":request.session['email']})
            moviesbooked=[]
            showtime=[]
            date=[]
            seats=[]
            amount=[]
            moviename=[]
            src=[]
            bookedcount=0
            present = datetime.now().date()
            for l in bookedmovies: 
                date_time_obj = datetime.strptime(l['DATE'], '%Y-%m-%d')
                if date_time_obj.date()>=present:
                    if l['showtime']:
                        showtime.append(l['showtime'])
                        screen=l['showtime']
                        screen=screen[-7:];
                    if l['DATE']:
                        date.append(l['DATE'])      
                        bookedcount=bookedcount+1;
                    if l[screen]:
                        seats.append(l[screen])     
                    if l['moviename']:
                        moviename.append(l['moviename'])        
                    if l['src']:
                        src.append(l['src'])        
                    if l['amount']:
                        amount.append(l['amount'])
            moviesbooked=zip(showtime,date,seats,amount,moviename,src)
            context={
            'name':request.session['username'],
            'email':request.session['email'],
            'password':request.session['password'], 
            'verify':request.session['verify'],
            'mobile':request.session['mobile'],
            'loop':a,
            'loopinrow':colum,
            "locations":cities,
            "wallet":request.session['wallet'],
            "booked":moviesbooked,
            "count":bookedcount
            }
            return render(request, 'Modify/profile.html',context)
        else:
            return redirect(index)
	
@csrf_exempt
def signin(request):
		if request.method=='POST':
			email=request.POST.get('demail')
			password=request.POST.get('dpsw')
			client = MongoClient("mongodb+srv://naveen:Rohit%40264@cluster0-xsqfd.mongodb.net/test?retryWrites=true&w=majority")
			db=client.movies
			result=db.login.find({"$and":[ {"email": email ,"password":password }]})
			global demail,dpsw,name,verify,mobile
			demail=None
			dpsw=None
			name=None
			verify=None
			mobile=None
			wallet=None
			for x in  result:
				demail=(x['email'])
				dpsw=(x['password'])
				name=(x['name'])
				verify=(x['verify'])
				mobile=(x['mobile'])
				wallet=(x['wallet'])
			print(demail)
			print(verify)

			request.session['username'] =name
			request.session['password'] =dpsw
			request.session['email']=demail 
			request.session['verify']=verify 
			request.session['mobile']=mobile
			request.session['wallet']=wallet
			if (demail==email) and (dpsw==password):
				context ='OK'
			else:
				context ='fail'		
			
			print(context)
			return HttpResponse(context)
		else:
				return render(request, 'index.html')			

def logout(request):
		try:
			del request.session['username']
			del request.session['password']
			del request.session['email']
			del request.session['mobile']
			del request.session['verify']
			del request.session['wallet']
			del request.session['theatreid']
		except:
			pass
		return render(request,'index.html')			
