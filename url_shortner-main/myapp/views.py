from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import url_info

# Create your views here.


def hello(request):
    return HttpResponse("HELLO USERS")


def homepage(request):

    dict = {
        "submitted": False,
        "error": False
    }

    if (request.method == 'POST'):

        # data is dictionary
        data = request.POST  

        #reading data from dictionary
        long_url = data['longurl']
        custom_name = data['custom_name']

        # printing in terminal
        print(long_url)
        print(custom_name)

        #if value is unique try will execute
        #if value is not unique it will pass error=true
        
        try:
            # creating object (will make row in database)
            obj = url_info(long_url=long_url, short_url=custom_name)

            # save object in database
            obj.save()

            #reading date and clicks from object created
            date = obj.date
            clicks = obj.clicks

            # making dictionary to pass it to HTML page
            dict["submitted"] = True
            dict["long_url"] = long_url
            dict["short_url"] = request.build_absolute_uri() + custom_name
            dict["date"] = date
            dict["clicks"] = clicks
            
        except:
            dict["error"] = True

    return render(request, "index.html", dict)

def redirect_url(request, short_url):
    row = url_info.objects.filter(short_url = short_url)
    
    if len(row) == 0:
        return HttpResponse("NO URL EXIST")
    
    obj = row[0]
    long_url = obj.long_url
    
    obj.clicks = obj.clicks + 1
    obj.save()
    
    return redirect(long_url)  

def all_analytics(request):
    obj=url_info.objects.all()
    dict={
        "obj":obj
    }
    return render(request,"all_analytics.html",dict)
