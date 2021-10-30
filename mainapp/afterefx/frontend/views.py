from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext
from django.db import  connection,transaction
import base64
from django.views.decorators.csrf import csrf_exempt
import uuid
from datetime import datetime
from django.core.mail import send_mail
from django.contrib import messages
from .dash_apps.finished_apps import mygraph

@csrf_exempt 
def home(request):
    successmessage = ''
    successmessagenews = ''
    errormessage = ''
    

    if request.method == "POST":

        tempname = request.POST.get('name')
        tempemail = request.POST.get('email')
        tempsubject = request.POST.get('subject')
        tempmessage = request.POST.get('message')
        tempemailnewsletter = request.POST.get('emailnewsletter')
        fromemail = 'olof@afterefx.com'
        fromemailname = 'Afterefx Support'
        tomail = 'rashad@afterefx.com'
        NewsletterFromEmail = 'rashad@afterefx.com'
        NewsletterToEmail = 'olof@afterefx.com'
        NewsletterFromEmailName = 'Afterefx Support'
        NewsletterSubject = 'Request for Newsletter Subscription'
        NewsletterMessage = 'You received a request for news letter subscription from'
        NewsletterToEmail = 'rashad@afterefx.com'
        """ if request.POST.get('btnsendmessage'):
            subject = 'New Request - ' + tempsubject
            body = "<h3>" + tempname + "</h3>" + "<h4>" + tempemail + "</h4>" +"<p>" + tempmessage + "</p>"

            send_mail(subject , body, fromemail, [fromemail], fail_silently=False)
            successmessage = 'Your message has been sent successfully. Thank you!'
            return render(request, 'frontend/home.html' , { 'successmess': successmessage, 'errormess': errormessage, 'successmessnews': successmessagenews})
        else:
            bodymsg = NewsletterMessage + " " + tempemailnewsletter

            send_mail(NewsletterSubject , bodymsg, NewsletterFromEmail, [NewsletterToEmail], fail_silently=False)
            successmessagenews = 'Thanks for joining our newsletter'
            return render(request, 'frontend/home.html' , { 'successmess': successmessage, 'errormess': errormessage, 'successmessnews': successmessagenews})
             """
    else:
        if 'registersuccess' in request.COOKIES:
            messages.success(request, 'Successfully Registered. Please Contact Afterefx Support for Access!')
            
        response = render(request, 'frontend/home.html' , { 'successmess': successmessage, 'errormess': errormessage, 'successmessnews': successmessagenews})
        if 'registersuccess' in request.COOKIES:
            response.delete_cookie('registersuccess')
        return response



def about(request):
    return render(request, 'frontend/about.html')

@csrf_exempt 
def login(request):
    errormessage = ''
    successmessage = ''
    if request.method == "POST":
        if request.POST.get('loginbtn'):

            # response1 =  redirect(dashboardanalytics)
            # response1.set_cookie('email',  'abc@gmail.com')
            # response1.set_cookie('name', 'abc')
            #
            # return response1


            loginusername = request.POST.get('l_username')
            loginpassword = request.POST.get('l_password')
            
            finalpass = 'Y'
            cursor = connection.cursor()
            
            
            query1 = "select * from U_USER_LOGIN_DETAILS where  EMAIL = %s"
            
            convertpassword = ''
            cursor.execute(query1, [loginusername])
            row = cursor.fetchall()
            datafinal = list(row)

            #return HttpResponse(datafinal)

            if len(datafinal) < 1:
                errormessage = 'Email Not Registered'
                return render(request, 'frontend/login.html' , { 'errormess' : errormessage, 'successmess' : successmessage})

            if datafinal[0][5] == 'N':
                errormessage = 'Access Denied. Please Contact Afterefx Support!'
                return render(request, 'frontend/login.html' , { 'errormess' : errormessage, 'successmess' : successmessage})
            

            if len(datafinal) > 0:
                convertpassword = str(base64.b64decode(datafinal[0][3]).decode('utf-8'))



            if len(datafinal) > 0 and loginpassword == convertpassword:
                

                cursornext = connection.cursor()
                query2 = "select * from U_USER_DETAILS where  USER_ID = %s"
                cursornext.execute(query2, [datafinal[0][0]])
                rownext = cursornext.fetchall()
                datainner = list(rownext)

                """  request.session['email'] = datafinal[0][2]
                request.session['name'] = datainner[0][2]+ " " + datainner[0][4] """
                context_instance = RequestContext(request)
                
                response =  redirect(dashboardanalytics)
                response.set_cookie('email',  datainner[0][2])
                response.set_cookie('name', datainner[0][2]+ " " + datainner[0][4])

                return response
                #return redirect(dashboardhome, name = datafinal[0][2], email = datafinal[0][2])
            else:
                errormessage = 'The password you have entered is incorrect.'
                return render(request, 'frontend/login.html' , { 'errormess' : errormessage, 'successmess' : successmessage})
            
            
        else:
            registerfirstname = request.POST.get('r_firstname')
            registerlastname = request.POST.get('r_lastname')
            registeremail = request.POST.get('r_email')
            registerpassword = request.POST.get('r_password')
            uidvalue = uuid.uuid4()
            now = datetime.now()
            dt_string = now.strftime("%Y/%m/%d %H:%M:%S")

            now2 = datetime(9999, 12, 31)
            dt_string2 = now2.strftime("%Y/%m/%d %H:%M:%S")
            cursorinsert = connection.cursor()
            insertquery = "INSERT INTO U_USER_DETAILS(USER_ID, EFF_START_DT, FIRST_NM, LAST_NM) VALUES( %s ,%s, %s, %s )"
            cursorinsert.execute(insertquery, (uidvalue, now, registerfirstname, registerlastname))
            transaction.commit()

            passwordenc = registerpassword.encode("utf-8")
            encpass = base64.b64encode(passwordenc)

            

            cursorinsert2 = connection.cursor()
            insertquery2 = "INSERT INTO U_USER_LOGIN_DETAILS(USER_ID, EFF_START_DT,  EFF_END_DT, EMAIL, PASSWORD) VALUES( %s ,%s,  %s, %s, %s )"
            cursorinsert2.execute(insertquery2, (uidvalue, now, now2, registeremail, encpass))
            transaction.commit()
            #successmessage = 'Successfully Registered. Please Contact Afterefx Support for Access!'
            #messages.info(request, 'Successfully Registered. Please Contact Afterefx Support for Access!')
            #messages.success(request, 'Successfully Registered. Please Contact Afterefx Support for Access!')
            response =  redirect(home)

            response.set_cookie('registersuccess',  'Successfully Registered. Please Contact Afterefx Support for Access!')

            return response;

    else:
        return render(request, 'frontend/login.html', { 'errormess' : errormessage, 'successmess' : successmessage})

@csrf_exempt 
def dashboardhome(request):
    name = ''
    email = ''
    if 'email' in request.COOKIES:
        email = request.COOKIES['email']
    if 'name' in request.COOKIES:
        name = request.COOKIES['name']
    

    
    if 'email' in request.COOKIES:
        return render(request, 'frontend/dashhome.html', {'namedata' : name, 'emaildata': email})
    else:
        return redirect(login)
    #return render(request, 'frontend/dashboardbase.html', {'namedata' : name, 'emaildata': email})


@csrf_exempt 
def dashboardanalytics(request):
    name = ''
    email = ''
    if 'email' in request.COOKIES:
        email = request.COOKIES['email']
    if 'name' in request.COOKIES:
        name = request.COOKIES['name']
    

    
    if 'email' in request.COOKIES:
        return render(request, 'frontend/dashanalytics.html', {'namedata' : name, 'emaildata': email})
    else:
        return redirect(login)
    #return render(request, 'frontend/dashboardbase.html', {'namedata' : name, 'emaildata': email})
    

def dashboardlogout(request):
    """ del request.session['email']
    del request.session['name']
    request.session.modified = True """
    response = redirect(login)
    response.delete_cookie('email')
    response.delete_cookie('name')
    return response


def requestDemoapi(request, name, email, subject, message):
    fromemail = 'olof@afterefx.com'
    fromemailname = 'Afterefx Support'
    tomail = 'rashad@afterefx.com'
    
    
    subject = 'New Request - ' + subject
    body =  name +  email +  message 

    send_mail(subject , body, fromemail, [tomail], fail_silently=False)
    successmessage = 'Your message has been sent successfully. Thank you!'
    
    
    return JsonResponse({'successmessage': successmessage})
    

def sendnewsletter(request, emailnewsletter):
    NewsletterFromEmail = 'rashad@afterefx.com'
    NewsletterToEmail = 'olof@afterefx.com'
    NewsletterFromEmailName = 'Afterefx Support'
    NewsletterSubject = 'Request for Newsletter Subscription'
    NewsletterMessage = 'You received a request for news letter subscription from'
    NewsletterToEmail = 'rashad@afterefx.com'
    bodymsg = NewsletterMessage + " " + emailnewsletter

    send_mail(NewsletterSubject , bodymsg, NewsletterFromEmail, [NewsletterToEmail], fail_silently=False)
    successmessagenews = 'Thanks for joining our newsletter'
    
    return JsonResponse({'successmessage': successmessagenews})
