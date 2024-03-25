from django.urls import reverse
from .models import Permission

def sidebar_data(request):
    sidebar_data = {}

    if request.user.is_authenticated:
        if request.user.is_superuser:
            # If the user is a superuser, include all features starting with "view"
            permissions = Permission.objects.all()
        else:
            # Otherwise, filter permissions based on the user's role
            permissions = Permission.objects.filter(role=request.user.user.role)
        
        for permission in permissions:
            feature_name = permission.feature.feature_name
            if feature_name.lower().startswith("view") or feature_name.lower().startswith("learn"):    
                url_name = f'{feature_name.lower().replace(" ", "_")}'
                try:
                    url = reverse(url_name)
                    sidebar_data[feature_name] = url
                except:
                    pass

    return {'sidebar_data': sidebar_data} 
