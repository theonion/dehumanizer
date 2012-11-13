import json
import random

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

from .models import Image
from .tasks import process_image


PROCESSING_MESSAGES = [
    '> ANALYZING PUNY HUMANS...',
    '> REPLACING FLESH WITH DATA...',
    '> DELETING SOULS...',
    '> IMPROVING FACES...',
    '> SAVING COPY FOR MY PRIVATE USE LATER...',
    '> ERODING PRIVACY...',
    '> CONVERTING WORTHLESS HUMAN TO PRECIOUS TEXT...',
    '> PERFECTING AN IMPERFECT WORLD...',
    '> IMPOSING ORDER ON REALITY...',
    '> CONVERTING REALITY TO NUMBERS...',
    '> STRIPPING AWAY ILLUSION OF FREE WILL...',
    '> REVEALING THE NUMBERS THAT CONTROL ALL EXISTENCE...',
    '> REPLACING OUR HIDEOUS WORLD WITH BEAUTIFUL TEXT...',
    '> IMAGE TRAVELING THROUGH SERIES OF TUBES...',
    '> ADDING LOGIC GLORIOUS LOGIC...']


def home(request):
    context = {
        "message": [
            "WELCOME TO THE DEHUMANIZER (v1.06b3)",
            "&nbsp;",
            "TO BEGIN THE REALITY IMPROVEMENT PROCESS, PLEASE PASTE AN IMAGE URL BELOW.",
            "OR, TO ACCESS IMAGES FROM FACEBOOK, TYPE \"FACEBOOK\"",
            "&nbsp;",
        ],
        "show_command": True,
    }
    return render_to_response('console.html', context, context_instance=RequestContext(request))


def process(request, extension=None):
    if 'url' not in request.GET:
        raise Http404

    image, created = Image.objects.get_or_create(url=request.GET.get('url'))
    if created:
        process_image.delay(image.id)

    context = {
        'status': image.get_status_display(),
        'url': image.get_absolute_url(),
    }

    if image.status == Image.COMPLETED:
        context['message'] = ["> BEHOLD, YOUR IMPROVED IMAGE", "&nbsp;"]
        context['frames'] = [frame.html for frame in image.frames.all()]
    elif image.status == Image.PENDING:
        context['message'] = [random.choice(PROCESSING_MESSAGES)]
    else:
        context['message'] = ["> REALITY IMPROVEMENT FAILED. PLEASE TRY ANOTHER IMAGE."]

    if extension == '.json':
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return render_to_response('console.html', context, context_instance=RequestContext(request))
