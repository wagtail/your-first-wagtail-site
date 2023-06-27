### Authors

You probably want your blog to have authors, which is an essential feature of blogs. The way to go about this is to have a fixed list, managed by the site owner through a separate area of the [Admin interface](https://guide.wagtail.org/en-latest/concepts/wagtail-interfaces/#admin-interface).

First, define an `Author` model. This model isn't a page in its own right. You have to define it as a standard Django `models.Model` rather than inheriting from `Page`. Wagtail introduces the concept of **Snippets** for reusable pieces of content, but they don't exist as part of the page tree themselves. You can manage **Snippets** through the [Admin interface](https://guide.wagtail.org/en-latest/concepts/wagtail-interfaces/#admin-interface). You can register a model as a **Snippet** by adding the `@register_snippet` decorator. Also, you can use all the fields types that you've used so far on pages on snippets too. 

To create Authors and give each author an author image as well as a name, add the following to `blog/models.py`:

```{eval-rst}
.. code-block:: python
    :emphasize-lines: 1,5-22

    from wagtail.snippets.models import register_snippet
    
    # ... Keep BlogIndexPage, BlogPage, BlogPageGalleryImage models, and then add the Author model:
    
    @register_snippet
    class Author(models.Model):
        name = models.CharField(max_length=255)
        author_image = models.ForeignKey(
            'wagtailimages.Image', null=True, blank=True,
            on_delete=models.SET_NULL, related_name='+'
        )
    
        panels = [
            FieldPanel('name'),
            FieldPanel('author_image'),
        ]
    
        def __str__(self):
            return self.name
    
        class Meta:
            verbose_name_plural = 'Authors'
```

```{note}
Note that you are using `panels` rather than `content_panels` here. Since snippets generally have no need for fields such as slug or publish date, the editing interface for them is not split into separate 'content' / 'promote' / 'settings' tabs. So there is no need to distinguish between 'content panels' and 'promote panels'.
```

Migrate this change by running `python manage.py makemigrations` and `python manage.py migrate`. Create a few categories through the **Snippets** area which now appears in your Wagtail [Admin interface](https://guide.wagtail.org/en-latest/concepts/wagtail-interfaces/#admin-interface).

You can now add authors to the `BlogPage` model, as a `many-to-many` field. The field type to use for this is `ParentalManyToManyField`. This field is a variation of the standard Django `ManyToManyField` that ensures the selected objects are properly associated with the page record in the revision history. It operates in a similar manner to how `ParentalKey` replaces `ForeignKey` for `one-to-many` relations. To add authors to the `BlogPage`, modify `models.py` in your blog app folder:

```{eval-rst}
.. code-block:: python
    :emphasize-lines: 3,6,9,18,22-30

    # New imports added for forms and ParentalManyToManyField, and MultiFieldPanel

    from django import forms
    from django.db import models
    
    from modelcluster.fields import ParentalKey, ParentalManyToManyField
    from wagtail.models import Page, Orderable
    from wagtail.fields import RichTextField
    from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
    from wagtail.search import index
    from wagtail.snippets.models import register_snippet

    
    class BlogPage(Page):
        date = models.DateField("Post date")
        intro = models.CharField(max_length=250)
        body = RichTextField(blank=True)
        authors = ParentalManyToManyField('blog.Author', blank=True)
    
        # ... Keep the main_image method and search_fields definition. Modify your     content_panels:
    
        content_panels = Page.content_panels + [
            MultiFieldPanel([
                FieldPanel('date'),
                FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            ], heading="Blog information"),
            FieldPanel('intro'),
            FieldPanel('body'),
            InlinePanel('gallery_images', label="Gallery images"),
        ]
```

In the preceding model modification, you used the `widget` keyword argument on the `FieldPanel` definition to specify a checkbox-based widget instead of the default multiple select boxes. Using the `widget` keyword argument makes your model more user-friendly. Also, you used a `MultiFieldPanel` in `content_panels` to group the `date` and `Authors` fields together for readability.

Finally, update the `blog_page.html` template to display the Authors:

```{eval-rst}
.. code-block:: html+django
    :emphasize-lines: 5-17
    
    {% block content %}
        <h1>{{ page.title }}</h1>
        <p class="meta">{{ page.date }}</p>
    
        {% with authors=page.authors.all %}
            {% if authors %}
                <h3>Posted in:</h3>
                <ul>
                    {% for author in authors %}
                        <li style="display: inline">
                            {% image author.author_image fill-80x120 style="vertical-align: middle" %}
                            {{ author.name }}
                        </li>
                    {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    
        <div class="intro">{{ page.intro }}</div>
    
        {{ page.body|richtext }}
    
        {% for item in page.gallery_images.all %}
            <div style="float: left; margin: 10px">
                {% image item.image fill-320x240 %}
                <p>{{ item.caption }}</p>
            </div>
        {% endfor %}
    
        <p><a href="{{ page.get_parent.url }}">Return to blog</a></p>
    
    {% endblock %}
```

Now go to your Admin interface, in the [Sidebar](https://guide.wagtail.org/en-latest/how-to-guides/find-your-way-around/#the-sidebar), you can see the new **Snippets** option. Click this to create your authors. After creating your authors, go to your blog posts and add authors to them.

!["Second Post" page, with title, date, authors, intro, body, and a gallery of three images](../_static/images/tutorial/tutorial_10.png)