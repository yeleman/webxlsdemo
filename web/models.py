#!/usr/bin/env python

from datetime import date

from django.db import models
from django.contrib.auth.models import User


class Period(models.Model):

    class Meta:
        unique_together = ('month', 'year')

    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    def __unicode__(self):
        return u"%d %d" % (self.month, self.year)

    @classmethod
    def get_or_create(cls, month, year):
        try:
            period = cls.objects.get(month=month, year=year)
            return period
        except cls.DoesNotExist:
            period = Period(month=month, year=year)
            period.save()
            return period
        return None


class MalariaReport(models.Model):

    YES = 'Y'
    NO = 'N'
    YN_CHOICES = ((YES, u"Oui"), (NO, u"Non"))

    class Meta:
        unique_together = ('health_center', 'period')

    reporter = models.ForeignKey(User)
    upload_date = models.DateTimeField(auto_now_add=True)
    period = models.ForeignKey('Period')

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

    total_malaria_inpatient_u5 = models.PositiveIntegerField()
    total_malaria_inpatient_5p = models.PositiveIntegerField()
    total_malaria_inpatient_fe = models.PositiveIntegerField()

    total_inpatient_u5 = models.PositiveIntegerField()
    total_inpatient_5p = models.PositiveIntegerField()
    total_inpatient_fe = models.PositiveIntegerField()

    total_malaria_death_u5 = models.PositiveIntegerField()
    total_malaria_death_5p = models.PositiveIntegerField()
    total_malaria_death_fe = models.PositiveIntegerField()

    total_death_u5 = models.PositiveIntegerField()
    total_death_5p = models.PositiveIntegerField()
    total_death_fe = models.PositiveIntegerField()

    total_bednets_u5 = models.PositiveIntegerField()
    total_bednets_fe = models.PositiveIntegerField()

    total_cpn1_fe = models.PositiveIntegerField()
    total_sp1_fe = models.PositiveIntegerField()
    total_sp2_fe = models.PositiveIntegerField()

    stockout_act_infant = models.CharField(max_length=1, choices=YN_CHOICES)
    stockout_act_kid = models.CharField(max_length=1, choices=YN_CHOICES)
    stockout_act_adult = models.CharField(max_length=1, choices=YN_CHOICES)

    stockout_arthemether = models.CharField(max_length=1, choices=YN_CHOICES)
    stockout_quinine = models.CharField(max_length=1, choices=YN_CHOICES)
    stockout_serum = models.CharField(max_length=1, choices=YN_CHOICES)

    stockout_mild = models.CharField(max_length=1, choices=YN_CHOICES)
    stockout_rdt = models.CharField(max_length=1, choices=YN_CHOICES)
    stockout_sp = models.CharField(max_length=1, choices=YN_CHOICES)

    def __unicode__(self):
        return u"%s %s %s" % (self.health_center, self.month, self.year)

    def display_name(self):
        return u"%(cscom)s - %(period)s" \
               % {'cscom': self.health_center.upper(), 'period': self.period}

    def total_act(self):
        return self.total_malaria_acttreated_u5 + \
               self.total_malaria_acttreated_5p

    def total_confirmed(self):
        return self.total_malaria_confirmed_u5 + \
               self.total_malaria_confirmed_5p + \
               self.total_malaria_confirmed_fe
