import uuid
from django.urls.base import reverse
from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

class Record(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=15, default='en')
    voice_record = models.FileField(upload_to="static/records",)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    pdf = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Record"
        verbose_name_plural = "Records"

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("library:record_detail", kwargs={"id": str(self.id)})

class Search(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    language = models.CharField(max_length=15, default='en')
    voice_record = models.FileField(upload_to="static/searches",)
    user = models.ForeignKey(User, on_delete= models.CASCADE)

    class Meta:
        verbose_name = "Search"
        verbose_name_plural = "Searches"

    def __str__(self):
        return str(self.id)

    def get_results_url(self):
        return reverse("library:search_result", kwargs={"id": str(self.id)})


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        verbose_name =_(u'Title'),
        help_text = _(u'Commentary Title'),
        max_length = 255
    )
    book = models.FileField(
        verbose_name = _(u'E-book'),
        help_text = _(u'Upload a pdf document.'),
        upload_to = 'static/uploads/pdfs'
    )
    thumbnail = models.ImageField(
        #verbose_name = _(u'Thumbnail'),
        help_text = _(u'The thumbnail'),
        upload_to = 'static/uploads/pdfs',
        blank = True,
        null = True
    )
    description = models.TextField(
        verbose_name=_(u'Title'),
        help_text=_(u'Commentary Title'),
        max_length=255,
        blank=True,
        null=True
    )

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

