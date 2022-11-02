from . models import Requisition

def get_notification(request):
    count = Requisition.objects.filter(accepted=False).count()
    count = Requisition.objects.filter(approved=False).count()
    
    data = {
        'count':count,
        
    }
    return data







