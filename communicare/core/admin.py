import weasyprint
from django.contrib import admin, messages
from django.conf import settings
from django.contrib.admin import SimpleListFilter
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from ..core.models import Event, Customer, Place, City, FederativeUnit, Source, Testimony, Registration, \
    source_verbose_name

admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.index_title = settings.ADMIN_INDEX_TITLE


@admin.register(FederativeUnit)
class FederativeUnitModelAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityModelAdmin(admin.ModelAdmin):
    search_fields = ('name', 'uf__initials')
    ordering = ('name',)


@admin.register(Place)
class PlaceModelAdmin(admin.ModelAdmin):
    autocomplete_fields = ('city',)


@admin.register(Source)
class SourceModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    autocomplete_fields = ('city',)


class RegistrationInline(admin.TabularInline):
    model = Event.registrations.through
    extra = 0
    autocomplete_fields = ('customer',)
    readonly_fields = ('contract_sent', 'send_contract')
    fields = ('customer', 'contract_sent', 'send_contract')

    class Media:
        js = ("admin/js/send_contract.js",
              "js/jquery/jquery.js")

    def send_contract(self, obj):
        return mark_safe('<a href="javascript:void(0)" onclick="send_contract('+str(obj.pk)+')">Enviar contrato</a>')

    send_contract.short_description = ""


@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    inlines = [
        RegistrationInline,
    ]
    prepopulated_fields = {'slug': ("title", "subtitle")}
    list_display = ('title', 'subtitle', 'start_date')


@admin.register(Testimony)
class TestimonyModelAdmin(admin.ModelAdmin):
    list_display = ('customer',)
    autocomplete_fields = ('customer',)


@admin.register(Registration)
class RegistrationModelAdmin(admin.ModelAdmin):
    class EventFilter(SimpleListFilter):
        title = Event._meta.verbose_name
        parameter_name = 'event'

        def lookups(self, request, model_admin):
            events = set([r for r in Event.objects.all()])
            return [(r.id, str(r)) for r in events]

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(event__id__exact=self.value())
            else:
                messages.add_message(request, messages.WARNING, 'Escolha um ' + self.title)
                return queryset.filter(event__id__exact=0)
    list_filter = (EventFilter,)
    search_fields = ('customer__name',)
    list_display = ('customer', 'contract_sent', 'financial_generated', 'financial_observations', 'nf_status',
                    'get_customer_source')

    def get_customer_source(self, obj):
        return obj.customer.source
    get_customer_source.short_description = source_verbose_name
    get_customer_source.admin_order_field = 'customer__source'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.method == 'POST':
            if '_contrato' in request.POST:
                super(RegistrationModelAdmin, self).change_view(request, object_id, form_url, extra_context)

                if Registration.objects.filter(pk=object_id).exists():
                    registration_obj = Registration.objects.get(pk=object_id)

                    if registration_obj.customer.email not in [None, '']:
                        d = {
                            'event': registration_obj.event,
                            'customer': registration_obj.customer
                        }
                        text_content = render_to_string('core/contract_email.txt', d)
                        html_content = render_to_string('core/contract_email.html', d)
                        subject, to = 'Contrato (%s)' % registration_obj.event.title, registration_obj.customer.email

                        # Contrato em PDF
                        context = {
                            'title': subject,
                            'registration': registration_obj
                        }
                        html = render_to_string('core/contract.html', context)
                        pdf_file = weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf()




                        msg = EmailMultiAlternatives(subject=subject, body=text_content, to=[to])
                        msg.attach_alternative(html_content, "text/html")
                        file_name = subject
                        msg.attach(file_name, pdf_file, 'application/pdf')
                        msg.send()

                        registration_obj.contract_sent = True
                        registration_obj.save()

                        self.message_user(
                            request,
                            "Contrato enviado com sucesso para '{}'.".format(registration_obj.customer.email),
                            messages.SUCCESS)
                    else:
                        self.message_user(
                            request,
                            "{} sem e-mail informado!".format(Registration._meta.verbose_name),
                            messages.ERROR)
                return HttpResponseRedirect("../")

        return super(RegistrationModelAdmin, self).change_view(request, object_id, form_url,
                                                               extra_context=extra_context)
