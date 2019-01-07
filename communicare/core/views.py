from django.conf import settings
from django.core import mail
from django.http import JsonResponse
from django.views.generic import TemplateView

from ..core.forms import ContactForm


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['contact_form'] = ContactForm()
        return context


def contact(request):
    if request.method == 'POST':
        response_data = {}

        # send email using the request.POST dictionary
        to = request.POST.get('email')
        from_ = str(settings.DEFAULT_FROM_EMAIL),

        message = "{name} / {email} / {phone} disse: ".format(
            name=request.POST.get('name'),
            email=to,
            phone=request.POST.get('phone'),
        )
        message += "\n\n{0}".format(request.POST.get('message'))
        email = mail.EmailMessage(
            subject='Contato pelo site.',
            body=message,
            to=from_,
            reply_to=[to],
        )
        email.send()
        response_data['result'] = 'Obrigado pelo seu contato!<br>' \
                                  'O interesse pelo curso foi cadastrado com sucesso, ' \
                                  'retornaremos o mais rápido possível.'

        return JsonResponse(response_data)
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})
