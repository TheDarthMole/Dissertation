from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from apps.learn.models import ExploitType
from apps.progression.models import Progression


# Create your views here.

def chunk_results(list, n):
    return [list[i:i+n] for i in range(0, len(list), n)]


@login_required(login_url="/login/")
def progression(request):
    context = {'segment': 'progression',
               'chunked_exploit_types': list(chunk_results(ExploitType.objects.all(), 3)),
               'progress_obj': Progression(request.user)}
    html_template = loader.get_template('progression/progression.html')
    return HttpResponse(html_template.render(context, request))
