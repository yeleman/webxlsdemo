#!/usr/bin/env python

from datetime import date

from django.db import models
from django.contrib.auth.models import User

class MalariaReport(models.Model):

    class Meta:
        unique_together = ('health_center', 'month', 'year')

    reporter = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True)

    region = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    health_center = models.CharField(max_length=50)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    
    total_consult_u5 = models.PositiveIntegerField()
    total_consult_5p = models.PositiveIntegerField()
    total_consult_fe = models.PositiveIntegerField()

    total_malaria_u5 = models.PositiveIntegerField()
    total_malaria_5p = models.PositiveIntegerField()

    total_malaria_simple_u5 = models.PositiveIntegerField()
    total_malaria_simple_5p = models.PositiveIntegerField()

    total_malaria_severe_u5 = models.PositiveIntegerField()
    total_malaria_severe_5p = models.PositiveIntegerField()
    total_malaria_severe_fe = models.PositiveIntegerField()

    total_malaria_tested_u5 = models.PositiveIntegerField()
    total_malaria_tested_5p = models.PositiveIntegerField()
    total_malaria_tested_fe = models.PositiveIntegerField()

    total_malaria_confirmed_u5 = models.PositiveIntegerField()
    total_malaria_confirmed_5p = models.PositiveIntegerField()
    total_malaria_confirmed_fe = models.PositiveIntegerField()

    total_malaria_acttreated_u5 = models.PositiveIntegerField()
    total_malaria_acttreated_5p = models.PositiveIntegerField()


    def __unicode__(self):
        return u"%s %s %s" % (self.health_center, self.month, self.year)

    def display_name(self):
        return u"%(cscom)s - %(period)s" % {'cscom': self.health_center.upper(), 'period': self.period().strftime('%B %Y')}

    def period(self):
        return date(self.year, self.month, 1)

    def total_act(self):
        return self.total_malaria_acttreated_u5 + self.total_malaria_acttreated_5p

    def total_confirmed(self):
        return self.total_malaria_confirmed_u5 + self.total_malaria_confirmed_5p + self.total_malaria_confirmed_fe
    
