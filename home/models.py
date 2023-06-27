from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
<<<<<<< HEAD
    ]
=======
    ]
>>>>>>> b1999d3d7ff74dc4b5437d30557a1bc46edeac3c
