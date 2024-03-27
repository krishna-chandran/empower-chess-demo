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
            
            # Split feature_name by "_" and get the second part if available
            words = feature_name.split()
            # print('words',words)
            # print("lenght",len(words))
            if len(words) > 1:
                second_word = words[1]
                
                
                # print("second word", second_word)
                # Remove last character if it's 's'
                if second_word.endswith('s'):
                    second_word = second_word[:-1]
                    # print("second words", second_word)
                
                sidebar_name = second_word.capitalize()  
                # print('sidebar name:',sidebar_name)
                
                
                # url_name = ('view_'+second_word + 's').replace(' ', '_').lower()
                # print('url name:',url_name)
                # url = reverse(url_name)
                url_name = ('/'+second_word + 's').lower()
                url = url_name
                # print('Url:',url)
                sidebar_data[sidebar_name] = url
    print(sidebar_data)

    return {'sidebar_data': sidebar_data}