from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Count

from api.utils.constants import MEDIUM_FIELD_LIMIT, LONG_FIELD_LIMIT, HACKATHON_FEATURED_LIMIT, COORD_MAX_DIGITS, \
    COORD_MAX_DECIMAL_PLACES
from api.utils.enums import HACKATHON_TYPE

""" 
Hackathon Model
"""


class HackathonQueryset(models.query.QuerySet):
    # Current condition for Featured Hackathons is having >= 50 members - set by HACKATHON_FEATURED_LIMIT
    def featured(self):
        return self.annotate(num_hackers=Count('hacker')).filter(num_hackers__gte=HACKATHON_FEATURED_LIMIT)

    def start_date(self, start_date):
        return self.filter(start__date__gte=start_date)

    def end_date(self, end_date):
        return self.filter(end__date__lte=end_date)


class HackathonManager(models.Manager):
    def get_queryset(self):
        return HackathonQueryset(self.model)

    def featured(self):
        return self.get_queryset().featured()

    def start_date(self, start_date):
        return self.get_queryset().start_date(start_date=start_date)

    def end_date(self, end_date):
        return self.get_queryset().end_date(end_date=end_date)


class Hackathon(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    name = models.CharField(max_length=MEDIUM_FIELD_LIMIT)
    version = models.PositiveIntegerField(default=1)
    description = models.TextField()
    logo = models.TextField(null=True)
    hackathon_type = models.TextField(choices=HACKATHON_TYPE)
    location = models.CharField(max_length=LONG_FIELD_LIMIT)
    latitude = models.DecimalField(max_digits=COORD_MAX_DIGITS, decimal_places=COORD_MAX_DECIMAL_PLACES)
    longitude = models.DecimalField(max_digits=COORD_MAX_DIGITS, decimal_places=COORD_MAX_DECIMAL_PLACES)

    shipping_address = models.CharField(max_length=LONG_FIELD_LIMIT)
    travel_reimbursements = models.TextField()
    university_name = models.CharField(max_length=LONG_FIELD_LIMIT, null=True)
    contact_email = models.EmailField()

    start = models.DateTimeField()
    end = models.DateTimeField()
    social_links = JSONField()
    bus_routes = JSONField()
    timetable = JSONField()
    sponsors = JSONField()
    judges = JSONField()
    speakers = JSONField()
    prizes = JSONField()

    # Link to HackathonManager
    objects = HackathonManager()
