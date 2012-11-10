import json

from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import Image
from .tasks import process_image


def home(request):
    context = {
        "message": [
            "WELCOME TO THE DEHUMANIZER...",
            "&nbsp;",
            "PLEASE PASTE OR TYPE AN IMAGE URL BELOW, OR TYPE \"FACEBOOK\" TO PICK AN IMAGE FROM YOUR FACEBOOK ACCOUNT."
        ],
        "show_command": True,
    }
    return render_to_response('console.html', context, context_instance=RequestContext(request))


def process(request, format=None):
    if 'url' not in request.GET:
        raise Http404

    image, created = Image.objects.get_or_create(url=request.GET.get('url'))
    if created:
        process_image.delay(image)

    context = {
        'status': image.get_status_display(),
        'message': image.message(),
        'url': image.get_absolute_url(),
    }

    if format == 'json':
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        if image.status == Image.COMPLETED:
            HttpResponseRedirect(image.get_absolute_url)
        return render_to_response('console.html', context, context_instance=RequestContext(request))
