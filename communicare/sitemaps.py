from django.contrib import sitemaps
from django.urls import reverse


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return [
            'home', 'gallery', 'privacy_policy', 'cookies_statement',
            'treinamento_oratoria', 'curso_hipnose', 'treinamento_inteligencia_emocional',
            'atendimento_coaching', 'atendimento_hipnoterapia'
        ]

    def location(self, item):
        return reverse(item)