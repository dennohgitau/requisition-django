from django.shortcuts import render
from requisition.models import Requisition
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
import threading
from django.template.loader import render_to_string, get_template
from django.conf import settings


# Create your views here.


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


@login_required(login_url='user_login')
def accept(request):
    id  = request.GET.get("id")
    requisition = Requisition.objects.get(id=id)
    if requisition.accepted == False:
        owner = requisition.owner
        item = requisition.item
        seller_name = requisition.seller_name
        seller_address = requisition.seller_address
        price = requisition.price

        requisition.accepted= True
        requisition.save()
        data = {
                'id': id,
                'owner': owner,
                'item': item,
                'seller_name': seller_name,
                'seller_address': seller_address,
                'price': price,
                
            }
        message = get_template('admin-email.html').render(data)
        email = EmailMessage(
                subject= "Requisition Approval Request.",
                body=message,
                from_email= settings.EMAIL_HOST_USER,
                to=['godwins.juma@mftfulfillmentcentre.com']
            )
        email.content_subtype = "html"
        EmailThread(email).start()
        return HttpResponse("Accepted")
    else:
        return HttpResponse("Requisition is Already Accepted!")

@login_required(login_url='user_login')
def reject(request):
    id  = request.GET.get("id")
    requisition = Requisition.objects.get(id=id)
    requisition.accepted= False
    owner = requisition.owner
    item = requisition.item
    sent_to = owner.email 
    requisition.save()
    data={
        'item': item,
        'sent_to': sent_to

    }
    message = get_template('rejected-email.html').render(data)
    email = EmailMessage(
        subject= "Requisition Request.",
        body=message,
        from_email= settings.EMAIL_HOST_USER,
        to=[sent_to]
    )
    email.content_subtype = "html"
    EmailThread(email).start()
    return HttpResponse("Rejected")

@login_required(login_url='user_login')
def approve(request):
    id  = request.GET.get("id")
    requisition = Requisition.objects.get(id=id)
    if requisition.approved == False:
        requisition.approved = True
        requisition.save()
        owner = requisition.owner
        item = requisition.item
        seller_name = requisition.seller_name
        seller_address = requisition.seller_address
        price = requisition.price
        send_to = owner.email
        data = {
                'id': id,
                'owner': owner,
                'item': item,
                'seller_address': seller_address,
                'seller_name': seller_name,
                'price': price,
                
            }
        message = get_template('approved-email.html').render(data)
        email = EmailMessage(
                subject= "Requisition Approved.",
                body=message,
                from_email= settings.EMAIL_HOST_USER,
                to=[send_to]
            )
        email.content_subtype = "html"
        EmailThread(email).start()


        return HttpResponse("Approved")
    else:
        return HttpResponse("Requisition Already Approved!")

@login_required(login_url='user_login')
def not_approve(request):
    id  = request.GET.get("id")
    requisition = Requisition.objects.get(id=id)
    requisition.accepted= False
    requisition.approved = False
    requisition.rejected = True
    owner = requisition.owner
    item = requisition.item
    sent_to = owner.email 
    requisition.save()
    data={
        'item': item,
        'sent_to': sent_to

    }
    message = get_template('rejected-email.html').render(data)
    email = EmailMessage(
        subject= "Requisition Request.",
        body=message,
        from_email= settings.EMAIL_HOST_USER,
        to=[sent_to]
    )
    email.content_subtype = "html"
    EmailThread(email).start()
    return HttpResponse("Rejected")




