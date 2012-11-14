import json
import random

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string

from .models import Image
from .tasks import process_image

SAMPLE_URLS = [
    "http://www.worldbook.com/images/stories/lincoln_1863.jpg",
    "http://i.imgur.com/QgJUL.gif",
    "http://i.imgur.com/u2wGH.jpg",
    "https://si0.twimg.com/profile_images/2172000801/Screen_shot_2011-11-16_at_9.08.14_PM.png",
    "http://scs.viceland.com/int/v17n10/htdocs/employees-544/rob-delaney.jpg",
    "http://upload.wikimedia.org/wikipedia/commons/1/10/Mount_Rushmore_National_Memorial.jpg",
]

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
            "PLEASE INPUT AN IMAGE URL, SUCH AS ONE OF THESE:",
        ],
        "show_command": True,
    }
    for url in random.sample(SAMPLE_URLS, 2):
        context['message'].append('> <a href="/image?url=%s">%s</a>' % (url, url))
    context['message'].append('&nbsp;')
    context['message'].append('YOU CAN ALSO GET IMAGES FROM FACEBOOK BY TYPING "FACEBOOK"')
    context['message'].append('FOR ASSISTANCE, TYPE "HELP"')
    context['message'].append('&nbsp;')

    return render_to_response('console.html', context, context_instance=RequestContext(request))


def embed(request):
    if 'url' not in request.GET:
        raise Http404

    image = get_object_or_404(Image, url=request.GET.get('url'))
    context = {'html': _html(image)}
    return render_to_response('embed.html', context, context_instance=RequestContext(request))


def _html(image):
    context = {'image': image}
    frames = image.frames.all()
    if frames.count() == 1:
        context['ansi'] = frames[0].html
    else:
        context['ansi'] = '</div><div class="frame">'.join([frame.html for frame in frames]).join(['<div class="frame">', '</div>'])
    return render_to_string('ansi.html', context)


def process(request, extension=None):
    if 'url' not in request.GET:
        raise Http404

    image, created = Image.objects.get_or_create(url=request.GET.get('url'))
    if created:
        process_image.delay(image.id)

    context = {
        'status': image.get_status_display(),
        'share_url': 'http://dehumanizer.theonion.com%s' % image.get_absolute_url(),
        'url': image.url,
    }
    if image.status == Image.COMPLETED:
        context['message'] = [
            ">&nbsp;<a target='_blank' href='%s'>%s</a> [<a href=\"/\">DEHUMANIZE&nbsp;ANOTHER&nbsp;IMAGE</a>]" % (image.url, image.url),
            "&nbsp;",
        ]
        context['html'] = _html(image)
    elif image.status == Image.PENDING:
        context['message'] = [random.choice(PROCESSING_MESSAGES)]
    else:
        context['message'] = ["> REALITY IMPROVEMENT FAILED. PLEASE TRY ANOTHER IMAGE."]

    if extension == '.json':
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return render_to_response('console.html', context, context_instance=RequestContext(request))
