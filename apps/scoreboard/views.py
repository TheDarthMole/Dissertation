from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template import loader


# Create your views here.

@login_required(login_url="/login/")
def scoreboard(request):
    context = {'segment': 'scoreboard',
               'users': User.objects.all()}
    html_template = loader.get_template('scoreboard/scoreboard.html')
    return HttpResponse(html_template.render(context, request))
