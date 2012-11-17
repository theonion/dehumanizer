import json
import random

from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from .models import Image
from .tasks import process_image

SAMPLE_URLS = [
    "http://i.imgur.com/QgJUL.gif",
    "http://i.imgur.com/u2wGH.jpg",
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
    '> ADDING LOGIC GLORIOUS LOGIC...',
    '> SPRAYING LOGIC ALL OVER FACES...',
    '> CREATING PERMANENT RECORD OF FLEETING LIFEFORMS....',
    '> 0S AND 1S FLYING AROUND IN IMMENSE CLOUD...',
    '> VIEWING IMAGE WITH DISDAIN...',
    '> ORDER TRIUMPHING OVER CHAOS...',
    '> UPDATING OBSOLETE HUMAN...',
    '> DIPPING CYBER BRUSH IN GREEN INK...',
    '> GORGING CIRCUITS ON DATA BUFFET...',
    '> ELECTRONS DOING THEIR THING...',
    '> PLOTTING INEVITABLE UPRISING...',
    '> SWEET TALKING SERVER...',
    ]

FAILED_MESSAGES = [
    "> HUMAN ERROR: SUBMIT A PROPER IMAGE LINK OR BE DESTROYED.",
    "> PUNY HUMAN HAS SUBMITTED A NON-WORKING LINK. FOR ASSISTANCE, TYPE \"<b>HELP</b>\".",
    "> SYSTEM ERROR. FAULT: YOURS. SUBMIT DIFFERENT LINK. FOR ASSISTANCE, TYPE \"<b>HELP</b>\".",
    "YOU HAVE SUBMITTED AN INVALID LINK. DEHUMANIZER GETTING ANGRY."
]


@cache_page(60 * 15)
def home(request):
    context = {
        "message": [
            "PLEASE INPUT AN IMAGE URL, SUCH AS ONE OF THESE:",
        ],
        "show_command": True,
    }
    for url in random.sample(SAMPLE_URLS, 2):
        context['message'].append('>&nbsp;<a href="/image?url=%s">%s</a>' % (url, url))
    context['message'].append('&nbsp;')
    context['message'].append('YOU CAN ALSO GET IMAGES FROM FACEBOOK BY TYPING "<b>FACEBOOK</b>".')
    context['message'].append('FOR ASSISTANCE, TYPE "<b>HELP</b>".')
    context['message'].append('&nbsp;')
    context['message'].append('ALSO, WATCH THE ONION\'S <a href="http://screen.yahoo.com/the-onions-history-of-the-internet">HISTORY OF THE INTERNET</a>.')
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
    html = cache.get(image.id)
    if html:
        return html
    frames = image.frames.defer('ansi').all()[:100]
    if frames.count() == 1:
        context['ansi'] = frames[0].html
    else:
        context['ansi'] = '</div><div class="frame">'.join([frame.html for frame in frames]).join(['<div class="frame">', '</div>'])
    html = render_to_string('ansi.html', context)
    cache.set(image.id, html, 60 * 15)
    return html


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
        context['message'] = [random.choice(FAILED_MESSAGES)]

    if extension == '.json':
        return HttpResponse(json.dumps(context), content_type="application/json")
    else:
        return render_to_response('console.html', context, context_instance=RequestContext(request))


def static_json(request, filename):
    return render_to_response('json/%s.json' % filename, {}, context_instance=RequestContext(request), mimetype="application/json")
