import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .forms import InquiryForm

logger = logging.getLogger('core')


ROOMS = [
    {
        'name': 'Deluxe Annapurna View Room',
        'form_value': 'Deluxe Mountain View',
        'image': 'images/bedroom1.jpg',
        'description': (
            'Wake up to the Annapurna range from bed. A warm, contemporary '
            'retreat with handcrafted Nepali touches and floor-to-ceiling '
            'mountain views.'
        ),
        'badges': ['King Bed', 'Private Balcony', 'High-Speed Wi-Fi', 'Mountain Panorama', 'Ensuite Bath'],
        'size': '32 sqm',
        'capacity': '2 Adults + 1 Child',
    },
    {
        'name': 'Executive Mountain Suite',
        'form_value': 'Executive Suite',
        'image': 'images/bedroom2.jpg',
        'description': (
            'A spacious suite for guests who want extra room to unwind, '
            'with a private sitting area and uninterrupted views of '
            'Machhapuchhre.'
        ),
        'badges': ['King Bed', 'Private Balcony', 'High-Speed Wi-Fi', 'Mountain Panorama', 'Ensuite Bath'],
        'size': '46 sqm',
        'capacity': '2 Adults + 2 Children',
    },
]

GALLERY = [
    {'image': 'images/views1.jpg', 'caption': 'Sunrise over the Annapurna range'},
    {'image': 'images/views2.jpg', 'caption': 'Machhapuchhre (Fishtail Peak) at first light'},
    {'image': 'images/view3.jpg', 'caption': 'Mist settling over the Pokhara valley'},
    {'image': 'images/view4.jpg', 'caption': 'Twilight contours across the Himalaya'},
]

GALLERY_CATEGORIES = [
    {'slug': 'mountain', 'label': 'Mountain Views'},
    {'slug': 'dining', 'label': 'Ambiance & Dining'},
    {'slug': 'rooms', 'label': 'Rooms & Suites'},
]

GALLERY_FULL = [
    {'image': 'images/views1.jpg', 'caption': 'Sunrise over the Annapurna range', 'category': 'mountain'},
    {'image': 'images/views2.jpg', 'caption': 'Machhapuchhre (Fishtail Peak) at first light', 'category': 'mountain'},
    {'image': 'images/view3.jpg', 'caption': 'Mist settling over the Pokhara valley', 'category': 'mountain'},
    {'image': 'images/view4.jpg', 'caption': 'Twilight contours across the Himalaya', 'category': 'mountain'},
    {'image': 'images/cafeteria1.jpg', 'caption': 'Panoramic rooftop seating at sunset', 'category': 'dining'},
    {'image': 'images/cafeteria2.jpg', 'caption': 'Artisan Himalayan coffee and organic breakfast', 'category': 'dining'},
    {'image': 'images/bedroom1.jpg', 'caption': 'Deluxe Annapurna View Room', 'category': 'rooms'},
    {'image': 'images/bedroom2.jpg', 'caption': 'Executive Mountain Suite', 'category': 'rooms'},
]

AMENITIES = [
    {'name': '24/7 Front Desk', 'icon': 'desk'},
    {'name': 'High-Speed Wi-Fi', 'icon': 'wifi'},
    {'name': 'Hot Shower', 'icon': 'shower'},
    {'name': 'Airport / Bus Station Pick-up', 'icon': 'shuttle'},
    {'name': 'Trekking & Paragliding Assistance', 'icon': 'mountain'},
    {'name': 'Rooftop Observation Deck', 'icon': 'deck'},
]

ATTRACTIONS = [
    {
        'name': 'Phewa Lake Boating',
        'description': 'Glide across the mirrored waters of Phewa Lake, framed by the Annapurna skyline, just minutes from the hotel.',
    },
    {
        'name': 'World Peace Pagoda',
        'description': 'A serene hilltop stupa overlooking the lake and valley, reached by boat and a gentle forest walk.',
    },
    {
        'name': 'Sarangkot Sunrise Point',
        'description': 'Rise early for one of the finest sunrise panoramas in Nepal, with the Annapurnas glowing gold.',
    },
    {
        "name": "Devi's Fall",
        'description': 'A dramatic waterfall that vanishes underground, one of Pokhara\'s most photographed natural landmarks.',
    },
]


def _nav_links(request):
    """Nav anchors should scroll in-page on the homepage, and jump to the
    dedicated page (or the homepage section) from anywhere else."""
    is_index = bool(request.resolver_match) and request.resolver_match.url_name == 'index'
    return {
        'home_prefix': '' if is_index else reverse('index'),
        'rooms_link': '#rooms' if is_index else reverse('rooms'),
        'gallery_link': '#gallery' if is_index else reverse('gallery'),
    }


def _room_choices():
    return [choice for choice in InquiryForm.base_fields['room_preference'].choices]


def index(request):
    context = {
        'rooms': ROOMS,
        'gallery': GALLERY,
        'amenities': AMENITIES,
        'attractions': ATTRACTIONS,
        'room_choices': _room_choices(),
    }
    context.update(_nav_links(request))
    return render(request, 'index.html', context)


def rooms(request):
    context = {
        'rooms': ROOMS,
        'room_choices': _room_choices(),
    }
    context.update(_nav_links(request))
    return render(request, 'rooms.html', context)


def gallery(request):
    context = {
        'gallery_full': GALLERY_FULL,
        'gallery_categories': GALLERY_CATEGORIES,
    }
    context.update(_nav_links(request))
    return render(request, 'gallery.html', context)


def _wants_json(request):
    return (
        request.headers.get('x-requested-with') == 'XMLHttpRequest'
        or 'application/json' in request.headers.get('accept', '')
    )


def inquiry(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = InquiryForm(request.POST)
    wants_json = _wants_json(request)

    if not form.is_valid():
        message = 'Please correct the highlighted fields and try again.'
        if wants_json:
            return JsonResponse(
                {'status': 'error', 'message': message, 'errors': form.errors},
                status=400,
            )
        messages.error(request, message)
        return redirect('/#contact')

    data = form.cleaned_data
    submitted_at = timezone.now()

    email_context = {
        'full_name': data['full_name'],
        'email': data['email'],
        'phone': data['phone'],
        'check_in': data['check_in'],
        'check_out': data['check_out'],
        'room_preference': data['room_preference'],
        'adults': data['adults'],
        'children': data['children'],
        'message': data['message'],
        'submitted_at': submitted_at,
        'hotel_receiver_email': settings.HOTEL_RECEIVER_EMAIL,
    }

    try:
        hotel_email = EmailMessage(
            subject=f"New Reservation Inquiry from {data['full_name']} — Hotel Pokhara Eye",
            body=render_to_string('emails/hotel_notification.txt', email_context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.HOTEL_RECEIVER_EMAIL],
            reply_to=[data['email']],
        )
        hotel_email.send(fail_silently=False)

        guest_email = EmailMessage(
            subject='We have received your inquiry — Hotel Pokhara Eye',
            body=render_to_string('emails/guest_confirmation.txt', email_context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[data['email']],
        )
        guest_email.send(fail_silently=False)
    except Exception:
        logger.exception('Failed to dispatch inquiry emails for %s <%s>', data['full_name'], data['email'])
        message = (
            'Your inquiry details were received, but our email confirmation '
            'service is temporarily unavailable. Please call or WhatsApp us '
            'directly so we can assist you without delay.'
        )
        if wants_json:
            return JsonResponse({'status': 'error', 'message': message}, status=200)
        messages.warning(request, message)
        return redirect('/#contact')

    message = (
        f"Thank you, {data['full_name']}! Your inquiry has been received. "
        "Our team will review your dates and reach out shortly with availability and details."
    )
    if wants_json:
        return JsonResponse({'status': 'success', 'message': message})
    messages.success(request, message)
    return redirect('/#contact')
