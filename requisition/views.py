from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
import requisition
from . models import Requisition
from django.views.generic import ListView
from django.utils.decorators import method_decorator
import datetime
from email.message import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)

@login_required(login_url='user_login')
def log_out(request):
    logout(request)
    return redirect('user_login')

@login_required(login_url='user_login')
def home(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            home(request)
            return redirect('home')
        else:
            # Incorrect credentials, let's throw an error to the screen.
            return render(request, 'login.html', {'error_message': 'Incorrect username and / or password.'})

    else:
        return render(request, 'login.html')
        
@login_required(login_url='user_login')
def apply(request):
    return render(request, 'index.html')

class ViewRequisitionTemplateView(ListView):
    template_name = 'requisitions_view.html'
    model = Requisition
    paginate_by = 3
    context_object_name = "requisition"
    def post(self,request):
        user = request.user
        requisition = Requisition.objects.filter(owner=user)
        count = requisition.count()
    

        data = {
                'count':count,
                'requisition': requisition,
            }
        return HttpResponseRedirect(request.path, data)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        requisitions = Requisition.objects.all()
        context.update({
            'title': 'View Requisitions'
        })
        return context



class RequisitionTemplateView(TemplateView):
    template_name = "index.html"
    def post(self, request):
        department = request.POST.get("department")
        item = request.POST.get("item")
        description = request.POST.get("description")
        quantity = request.POST.get("quantity")
        seller_name = request.POST.get("seller_name")
        seller_address = request.POST.get("seller_address")
        price = request.POST.get("price")
        price = int(quantity) * int(price)


        requisition = Requisition.objects.create(
        department = department,
        item = item,
        description = description,
        quantity = quantity,
        seller_name = seller_name,
        seller_address = seller_address,
        price = price,
        owner=request.user,
        )

        requisition.save()
        owner = request.user
        if department == 'Operations':
            send_to = 'eleanor@mftfulfillmentcentre.com'
        elif department == 'Customer Service':
             send_to = 'rachel.ope@mftfulfillmentcentre.com'
        elif department == 'Business Development':
             send_to = 'irene.mutheu@mftfulfillmentcentre.com'
        elif department == 'Warehouse':
             send_to = 'victor.odongo@mftfulfillmentcentre.com'
        elif department == 'IT':
             send_to = 'support@mftfulfillmentcentre.com'
        elif department == 'Marketing':
             send_to = 'kelai.wanjiru@mftfulfillmentcentre.com'

        requisitions = Requisition.objects.all()
        id = requisition.id
        print(id)


        data = {
            'id': id,
            'requisitions': requisitions,
            'owner': owner,
            'item': item,
            'seller_address': seller_address,
            'seller_name': seller_name,
            'price': price,
            
        }
        message = get_template('email.html').render(data)
        email = EmailMessage(
            subject= "Requisition Request.",
            body=message,
            from_email= settings.EMAIL_HOST_USER,
            to=[send_to]
        )
        email.content_subtype = "html"
        EmailThread(email).start()


        return HttpResponseRedirect(request.path)
   
class ManageRequisitionTemplateView(ListView):
    template_name = "manage-requisitions.html"
    model = Requisition
    context_object_name = "requisitions"
    paginate_by = 3
    def post(self, request):
        appointment_id  = request.POST.get("requisition-id")
        requisition = Requisition.objects.get(id=appointment_id)
        requisition.accepted= True
        requisition.save()
        username = request.user.username

        data = {
            'owner': requisition.owner,
            'username': username,  
        }  

        
        return HttpResponseRedirect(request.path, data)

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        requisitions = Requisition.objects.all()
        context.update({
            'title': 'Manage Requisitions'
        })
        return context

    
class AdminManageRequisitionTemplateView(ListView):
    template_name = "admin-manage-requisitions.html"
    model = Requisition
    context_object_name = "requisitions"
    # login_required = True
    paginate_by = 3

    @login_required(login_url='user_login')
    def post(self, request):
        appointment_id  = request.POST.get("requisition-id")
        requisition = Requisition.objects.get(id=appointment_id)
        requisition.approved= True
        requisition.save()

        data = {
            'owner':requisition.owner,  
        }  

        
        return HttpResponseRedirect(request.path, data)

    def get_context_data(self, *args, **kwargs):

        context = super().get_context_data(*args, **kwargs)
        requisitions = Requisition.objects.all()
        context.update({
            'title': 'Admin Manage Requisitions'
        })
        return context


@login_required(login_url='user_login')
def all_requisitions(request):
    requisition = Requisition.objects.all()
    paginator = Paginator(requisition, 10 )
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    all_users = list(User.objects.values())
    names = []
    ids = []
    for user in all_users:
        name = user.get('username')
        id = user.get('id')
        names.append(name)
        ids.append(id)
    context = {
        'names' : all_users,
        'requisition': requisition,
        'page_obj': page_obj,
    }
   
    if  request.method == 'GET':
        department = request.GET.get("department")
        name = request.GET.get("User")
        start = request.GET.get("startdate")
        end = request.GET.get("enddate")
        
        for ida in ids:
            if name:
                user_filter = Requisition.objects.filter(owner=name)
                paginator = Paginator(user_filter, 10 )
                page_number = request.GET.get('page')
                user_filtered = Paginator.get_page(paginator, page_number)
                context_filtered = {
                    'names' : all_users,
                    'user_filtered':user_filtered,
                 }
                print('first')
                return render(request, 'display_all.html', context_filtered)
                
            else:
                if start and end:
                    date_filter = Requisition.objects.filter(sent_date__range=[start, end])
                    paginator = Paginator(date_filter, 10 )
                    page_number = request.GET.get('page')
                    date_filtered = Paginator.get_page(paginator, page_number)
                    context_filtered = {
                    'names' : all_users,
                     }
                    context_filtered['date_filtered'] = date_filtered
                    
                    context['date_filtered'] = date_filtered
                    print('Second')
                    return render(request, 'display_all.html', context)

                else: 
                    print('Second else')            
                    return render(request, 'display_all.html', context)                  
            

        else:
            
            return render(request, 'display_all.html', context)

    
