from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
import datetime,time


class Trends(models.Model):
    now = datetime.datetime.utcnow()
    for_js = int(time.mktime(now.timetuple())) * 1000

    app_name = models.CharField(null=True,max_length=200)
    date = models.DecimalField(default=for_js, max_digits=15, decimal_places=0)
    total_transfer_size = models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    total_requests = models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    html_transfer_size = models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    html_requests = models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    js_transfer_size =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    js_requests =  models.DecimalField(null=True, max_digits = 11, decimal_places = 0)
    css_transfer_size =  models.DecimalField(null=True, max_digits = 11, decimal_places = 0)
    css_requests =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    image_transfer_size =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    image_requests =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    flash_transfer_size =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    flash_requests =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    font_transfer_size =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    font_requests =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    other_transfer_size =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    other_requests =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    tcp_connections =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    doc_size =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    dom_elements =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    domains =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    max_reqs_on_1_domain =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)
    cacheable_resources =  models.DecimalField(null=True,max_digits = 11, decimal_places = 0)











# Create your models here.
