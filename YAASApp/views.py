import user
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test

#translation
from django.utils import translation
from django.utils.translation import ugettext as _

from forms import CreateUserForm
from forms import EditPasswordForm
from forms import EditEmailForm

from django.core.mail import send_mail

from models import Auction
from models import Bidders
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib import auth
from django.core import serializers
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.contrib import messages
#from django.contrib.auth.hanshers import make_password
from django.views.generic import ListView
import re,string
from YAASApp.views_server import *
from datetime import datetime
from datetime import timedelta
import datetime

def show_home(request):
    if request.method == "POST":
        date =  datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        request.session["startdate"] = date
        request.session["visited"] = 0
        request.session["edited"] = 0
        request.session["created"] = 0
        request.session["delete"] = 0
        option = request.POST.get('language')
        if '_login' in request.POST:
            return HttpResponseRedirect("/yaas/loginuser/")
        elif '_register' in request.POST:
            return HttpResponseRedirect("/yaas/createuser/")
        elif '_logout' in request.POST:
            return HttpResponseRedirect("/yaas/logoutuser/")
        elif '_edit' in request.POST:
            return HttpResponseRedirect("/yaas/edituser/")
        elif '_createauction'in request.POST:
            return HttpResponseRedirect("/yaas/createauction/")
        elif '_go' in request.POST:
             if option == "fi":
                 return HttpResponseRedirect("/setlanguage/fi")
             elif option =="en":
                 return HttpResponseRedirect("/setlanguage/en")
             elif option =="es":
                 return HttpResponseRedirect("/setlanguage/es")

    if request.session.get("startdate"):
        date =  datetime.datetime.now().strftime("%d-%m-%y %H:%M")
        request.session["startdate"] = request.session["startdate"]
        request.session["visited"] = request.session["visited"]
        request.session["edited"] = request.session["edited"]
        request.session["created"] = request.session["created"]
        request.session["delete"] = request.session["delete"]
    else:
        date =  datetime.datetime.now().strftime("%d-%m-%y%h%m%s")
        request.session["startdate"] = date
        request.session["visited"] = 0
        request.session["edited"] = 0
        request.session["created"] = 0
        request.session["delete"] = 0


    auction_lists = Auction.objects.all()
    context = {
        "auction_list": auction_lists,
    }
    return render_to_response('home.html', context, context_instance=RequestContext(request))


#Views about Auction
def show_Auction(request, idItem):
    print idItem
    if Auction.exists(idItem):
        request.session['visited'] = request.session['visited'] + 1
        nAuc = Auction.getByidItem(idItem)
    else:
      return HttpResponse("That blog doesn't exist")
    if '_edit' in request.POST:
        return HttpResponseRedirect("/yaas/editauction/"+str(nAuc.idItem)+"/")
    elif '_bid' in request.POST:
        return HttpResponseRedirect("/yaas/bid/"+str(nAuc.idItem)+"/")
    elif '_ban' in request.POST:
        return HttpResponseRedirect("/yaas/banauction/"+str(nAuc.idItem)+"/")
    contex = {
        "titleAuc": nAuc.titleAuc,
        "deadLine": nAuc.deadLine,
        "posted": nAuc.posted,
        "content": nAuc.content,
        "minPrice": nAuc.minPrice,
        "author": nAuc.author,
        "idItem": idItem
    }
    return render(request, "show.html", contex )

@login_required
def createAuction(request):
    if request.method == "POST" and request.POST.has_key("titleAuc") and request.POST.has_key("content") and request.POST.has_key("deadLine") and request.POST.has_key("hour") and request.POST.has_key("minu"):
        auxDay = request.POST.get('deadLine')
        auxHour = request.POST.get('hour')
        auxMin = request.POST.get('minu')
        auxDate = str(auxDay) +" "+ str(auxHour)+":" + str(auxMin)
        print type(auxDay)
        print "sale"
        auc_DeadLine = datetime.datetime.strptime(auxDate, "%Y-%m-%d %H:%M")
        auc_titleAuc=request.POST.get("titleAuc")
        auc_content=request.POST.get("content")
        auc_minPrice=request.POST.get("minPrice")
        todayDate = datetime.datetime.now()
        if todayDate < auc_DeadLine:
            if (todayDate+timedelta(3)) <=auc_DeadLine:
                print todayDate
                #request.session["created"] = request.session["created"] + 1
                print "antes de entrar al save"
                print auc_DeadLine
                #messages.add_message(request, messages.INFO, 'NEW BLOG ADDED')
                return render_to_response('confirmation.html', {"auxDate": auxDate, "auc_titleAuc": auc_titleAuc, "auc_content": auc_content, "auc_minPrice": auc_minPrice},
                                              context_instance=RequestContext(request))
            else:
                messages.add_message(request, messages.ERROR, 'The deadline has to be at least 72hrs')
                return HttpResponseRedirect("/yaas/createauction/")
        else:
            messages.add_message(request, messages.ERROR, 'You can not put a date before today')
            return HttpResponseRedirect("/yaas/createauction/")
    contex = {"idItem": id,}
    return render(request, "auction.html", contex)

@login_required
def edit_auction(request, idItem):
    if Auction.exists(idItem):
        auction = Auction.getByidItem(idItem)
    else:
        return HttpResponse("That item doens't exist")

    if request.user.username == auction.author:
        if auction.locked=="":
            # article is not locked, we lock it
            print "cookie:",request.session._get_or_create_session_key()
            auction.locked=request.session._get_or_create_session_key()
            auction.save()
        elif auction.locked!=request.session._get_or_create_session_key():
             # article is locked by others, we return an error message
                context = {
                    "titleAuc": auction.titleAuc,
                    "deadLine": auction.deadLine,
                    "posted": auction.posted,
                    "content": auction.content,
                    "minPrice": auction.minPrice,
                    "author": auction.author,
                    "idItem": idItem
                }
                return render_to_response("locked.html", context)

        if request.method == "POST" and request.POST.has_key("content"):
            # a valid POST request: save the new contents of the article
            # Always clean the input from the user
            auction = Auction.getByidItem(idItem)
            auction.content = request.POST.get("content")
            auction.locked=""
            auction.save()
            #request.session["edited"] = request.session["edited"] + 1
            #contedited = request.session["edited"]
            # Always redirect after a successful POST request
            print "entra a editar"
            print auction.content
            return HttpResponseRedirect("/yaas/")
        else:
            context = {
                    "titleAuc": auction.titleAuc,
                    "deadLine": auction.deadLine,
                    "posted": auction.posted,
                    "content": auction.content,
                    "minPrice": auction.minPrice,
                    "author": auction.author,
                    "idItem": idItem
                }
            return render(request, "editAuction.html", context)
    else:
        messages.add_message(request, messages.ERROR, "You are not the seller, only sellers can edit this")
        return HttpResponseRedirect("/yaas/")

def saveAucConf(request):
    option = request.POST.get('option')
    if option == "Yes":
        print request.POST.get('auc_DeadLine', '')
        auxDate1 = request.POST.get('auxDate', '')
        auc_DeadLine = datetime.datetime.strptime(auxDate1, "%Y-%m-%d %H:%M")
        auc_titleAuc = request.POST.get('auc_titleAuc', '')
        auc_content = request.POST.get('auc_content', '')
        auc_minPrice = request.POST.get('auc_minPrice', '')
        nAuction = Auction(titleAuc= auc_titleAuc, deadLine=auc_DeadLine, content=auc_content, minPrice=auc_minPrice)
        nAuction.author = request.user.username
        nAuction.authoremail = request.user.email
        nAuction.locked = ""
        nAuction.save()
        emailUser = request.user.email
        send_mail('Subject here', 'The auction has been created.', 'noreply@yaas.com',
                  [emailUser], fail_silently=False)
        return HttpResponseRedirect("/yaas/")
    elif option == "No":
       return HttpResponseRedirect("/yaas/createauction/")

def auctionBrowse(request):
    auction_lists = Auction.objects.all()
    context = {
        "auction_list": auction_lists,
    }
    return render_to_response('browse.html', context, context_instance=RequestContext(request))

def searchAuction(request):
    if request.method == 'POST':
        print "entra al search"
        aSearch= request.POST.get('search')
        result = Auction.objects.filter(titleAuc=aSearch)
        if result:
            nAuc = Auction.getBytitleAuc(aSearch)
            if nAuc.banded == "banded":
                messages.add_message(request, messages.INFO, "This item is banded")
                return render(request, "search.html")
            return show_Auction(request, nAuc.idItem)
    messages.add_message(request, messages.INFO, "This item doesn't exist")
    return render(request, "search.html")

def bid_auction(request, idItem):
    if Auction.exists(idItem):
        nAuc = Auction.getByidItem(idItem)
        #con esta linea entra al autor del objeto
        author = User.objects.filter(username=nAuc.author)
    if nAuc.locked=="":# article is not locked, we lock it
        print "cookie:",request.session._get_or_create_session_key()
        nAuc.locked=request.session._get_or_create_session_key()
        nAuc.save()
    elif nAuc.locked!=request.session._get_or_create_session_key():
         # article is locked by others, we return an error message
        context = {
            "titleAuc": nAuc.titleAuc,
            "deadLine": nAuc.deadLine,
            "posted": nAuc.posted,
            "content": nAuc.content,
            "minPrice": nAuc.minPrice,
            "author": nAuc.author,
            "idItem": idItem
        }
        return render_to_response("lockedbid.html", context)

    if request.method == "POST" and request.POST.has_key("minPrice"):
        from_email = 'noreply@yaas.com'
        newPrice = request.POST.get('minPrice', '')
        auxNew = float(newPrice)
        aux = nAuc.minPrice
        if auxNew > aux:
            oldBidder = nAuc.bidder
            newBidder = request.user.username
            newBidderEmail = request.user.email
            if newBidder != nAuc.author:
                if oldBidder != newBidder:
                    oldUserEmail = nAuc.bidderemail
                    authoremail = nAuc.authoremail
                    nBiddeer = Bidders(bidderName=newBidder, bidderEmail= newBidderEmail, bidItem= nAuc.idItem)
                    nBiddeer.save()
                    nAuc.minPrice = newPrice
                    nAuc.bidder = newBidder
                    nAuc.bidderemail = newBidderEmail
                    nAuc.save()
                    bidders = Bidders.objects.all()
                    emailBidders = []
                    for bider in bidders:
                        emailBidders.append(bider.bidderEmail)
                    send_mail('New bid add', 'A new bid has add to the item .', from_email ,
                            emailBidders, fail_silently=False)
                    return HttpResponseRedirect("/yaas/")
                else:
                    nAuc.locked =""
                    nAuc.save()
                    messages.add_message(request, messages.INFO, "You are the last bidder")
                    return HttpResponseRedirect("/yaas/")
        else:
            messages.add_message(request, messages.INFO, "The price have to be higher than"+ str(nAuc.minPrice))
            return HttpResponseRedirect("/yaas/bid/"+str(nAuc.idItem)+"/")

    context = {
        "titleAuc": nAuc.titleAuc,
        "minPrice": nAuc.minPrice,
        "idItem": idItem
    }
    return render(request, "bid.html", context)



#Views about User
def createUser(request):
    if request.method == 'POST':
        form =CreateUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            email = form.cleaned_data["email"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]

            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            return HttpResponseRedirect("/yaas/loginuser/")
    else:
        form =CreateUserForm()

    return render_to_response("newUser.html", {'form': form},context_instance= RequestContext(request))

def loginUser(request):
    date =  datetime.datetime.now().strftime("%d-%m-%y %H:%M")
    request.session["startdate"] = date
    request.session["visited"] = 0
    request.session["edited"] = 0
    request.session["created"] = 0
    request.session["delete"] = 0
    if request.method == "POST":
        if request.method == 'POST':
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            nextTo = request.GET.get('next', '/yaas/')
            user = auth.authenticate(username=username, password=password)
            posts = Auction.objects.all()
        if user is not None and user.is_active:
            auth.login(request,user)
            return HttpResponseRedirect(nextTo)
        else:
            messages.add_message(request, messages.INFO, 'Error: wrong Password')
    else:
        error = "Please Sign in"
        return render_to_response("loginUser.html", {'error': error},context_instance= RequestContext(request))
    return render_to_response("loginUser.html", {},context_instance= RequestContext(request))

def editUser(request):
    if request.method == "POST":
        if '_editpassword' in request.POST:
            return HttpResponseRedirect("/editpassword/")
        elif '_editemail' in request.POST:
            return HttpResponseRedirect("/editemail/")
    return render_to_response("editUser.html", {},context_instance= RequestContext(request))

def editPassword(request):
    if request.method == "POST":
        form = EditPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user = User.objects.get(username=request.user.username)
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.INFO, 'Your password has been changed')
            return HttpResponseRedirect("/yaas/")
    else:
        form = EditPasswordForm(request.POST)

    return render_to_response("editPass.html", {'form': form},context_instance= RequestContext(request))

def editEmail(request):
    if request.method == "POST":
        form = EditEmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.add_message(request, messages.INFO, 'Your email has been changed')
            return HttpResponseRedirect("/yaas/")
    else:
        form = EditEmailForm(request.POST)

    return render_to_response("editEmail.html", {'form': form},context_instance= RequestContext(request))

def logoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect("/yaas/")


#Ban a product only admin
@user_passes_test(lambda u: u.is_superuser)
def ban_auction(request, idItem):
    print "entra al ban"
    if Auction.exists(idItem):
        #request.session['visited'] = request.session['visited'] + 1
        nAuc = Auction.getByidItem(idItem)
        nAuc.banded = "banded"
        nAuc.save()
        from_email = 'noreply@yaas.com'
        bidders = Bidders.objects.all()
        emailBidders = []
        for bider in bidders:
            emailBidders.append(bider.bidderEmail)
        send_mail('New bid add', 'The item '+str(nAuc.titleAuc)+"has been banded", from_email ,
                            emailBidders, fail_silently=False)
        return HttpResponseRedirect("/yaas/")


def set_language(request, lang_code):
    print "entra"
    user_language = lang_code
    translation.activate(user_language)
    request.session[translation.LANGUAGE_SESSION_KEY] = user_language
    return HttpResponseRedirect("/yaas/")
