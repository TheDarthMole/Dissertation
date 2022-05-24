from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader

from apps.accounts.models import CustomUser


# Create your views here.


@login_required(login_url="/login/")
def scoreboard(request):
    users = CustomUser.objects.all()
    # This is computationally expensive, as it's a recursive
    # call to a model query. Please excuse, done for rapid development
    # @TODO Improve efficiency
    users = sorted(users, key=lambda m: m.points, reverse=True)
    count = 1
    for user in users:
        user.leaderboard = count
        count += 1

    context = {'segment': 'scoreboard',
               'users': users}
    html_template = loader.get_template('scoreboard/scoreboard.html')
    return HttpResponse(html_template.render(context, request))
