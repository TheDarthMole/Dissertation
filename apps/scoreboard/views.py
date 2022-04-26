from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from apps.accounts.models import CustomUser

# Create your views here.



@login_required(login_url="/login/")
def scoreboard(request):
    context = {'segment': 'scoreboard',
               'users': CustomUser.objects.all()}
    html_template = loader.get_template('scoreboard/scoreboard.html')
    return HttpResponse(html_template.render(context, request))
