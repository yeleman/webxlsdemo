#!/usr/bin/env python
# encoding=utf-8

import re

import xlrd

from models import *
from django import db

XLS_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ACCEPTED = 0
REJECTED = 1
UNKNOWN = -1

STATUSES = {
    ACCEPTED: u"accepté",
    REJECTED: u"refusé",
    UNKNOWN: u"inconnu?",
}


def verbose_status(status):
    return STATUSES[status]

def data_for_coord(coord, ws):

    letter, line = re.match(r'([a-zA-Z]+)([0-9]+)', coord).groups()
    row = int(line) - 1
    column = XLS_LETTERS.index(letter.upper())
    return ws.row_values(row)[column]


FORM_DATA = {
    'region': {'coord': 'B2', 'attr': 'region', 'type': unicode, 'name': u"Région"},
    'district': {'coord': 'B3', 'attr': 'district', 'type': unicode, 'name': u"District sanitaire"},
    'hc': {'coord': 'B4', 'attr': 'health_center', 'type': unicode, 'name': u"Établissement sanitaire"},
    'month': {'coord': 'D3', 'attr': 'month', 'type': int, 'name': u"Mois"},
    'year': {'coord': 'G3', 'attr': 'year', 'type': int, 'name': u"Année"},

    'total_consultation_u5': {'coord': 'C7', 'attr': 'total_consult_u5', 'type': int, 'name': u"Total consultation, toutes causes confondues (< 5ans)"},
    'total_consultation_5p': {'coord': 'E7', 'attr': 'total_consult_5p', 'type': int, 'name': u"Total consultation, toutes causes confondues (5 ans et +)"},
    'total_consultation_fe': {'coord': 'G7', 'attr': 'total_consult_fe', 'type': int, 'name': u"Total consultation, toutes causes confondues (femmes enceintes)"},

    'total_malaria_u5': {'coord': 'C8', 'attr': 'total_malaria_u5', 'type': int, 'name': u"Nbre de Cas de paludisme (Tous suspectés) (< 5ans)"},
    'total_malaria_5p': {'coord': 'E8', 'attr': 'total_malaria_5p', 'type': int, 'name': u"Nbre de Cas de paludisme (Tous suspectés) (5 ans et +)"},

    'total_malaria_simple_u5': {'coord': 'C9', 'attr': 'total_malaria_simple_u5', 'type': int, 'name': u"Nbre de Cas de paludisme Simple (< 5ans)"},
    'total_malaria_simple_5p': {'coord': 'E9', 'attr': 'total_malaria_simple_5p', 'type': int, 'name': u"Nbre de Cas de paludisme Simple (5 ans et +)"},

    'total_malaria_severe_u5': {'coord': 'C10', 'attr': 'total_malaria_severe_u5', 'type': int, 'name': u"Nbre de Cas de paludisme Grave (< 5ans)"},
    'total_malaria_severe_5p': {'coord': 'E10', 'attr': 'total_malaria_severe_5p', 'type': int, 'name': u"Nbre de Cas de paludisme Grave (5 ans et +)"},
    'total_malaria_severe_fe': {'coord': 'G10', 'attr': 'total_malaria_severe_fe', 'type': int, 'name': u"Nbre de Cas de paludisme Grave (femmes enceintes)"},

    'total_malaria_tested_u5': {'coord': 'C11', 'attr': 'total_malaria_tested_u5', 'type': int, 'name': u"Cas de paludisme testés (GE et/ou TDR) (< 5ans)"},
    'total_malaria_tested_5p': {'coord': 'E11', 'attr': 'total_malaria_tested_5p', 'type': int, 'name': u"Cas de paludisme testés (GE et/ou TDR) (5 ans et +)"},
    'total_malaria_tested_fe': {'coord': 'G11', 'attr': 'total_malaria_tested_fe', 'type': int, 'name': u"Cas de paludisme testés (GE et/ou TDR) (femmes enceintes)"},

    'total_malaria_confirmed_u5': {'coord': 'C12', 'attr': 'total_malaria_confirmed_u5', 'type': int, 'name': u"Cas de paludisme confirmés (GE et/ou TDR) (< 5ans)"},
    'total_malaria_confirmed_5p': {'coord': 'E12', 'attr': 'total_malaria_confirmed_5p', 'type': int, 'name': u"Cas de paludisme confirmés (GE et/ou TDR) (5 ans et +)"},
    'total_malaria_confirmed_fe': {'coord': 'G12', 'attr': 'total_malaria_confirmed_fe', 'type': int, 'name': u"Cas de paludisme confirmés (GE et/ou TDR) (femmes enceintes)"},

    'total_malaria_acttreated_u5': {'coord': 'C13', 'attr': 'total_malaria_acttreated_u5', 'type': int, 'name': u"Nbre de Cas traités avec CTA (< 5ans)"},
    'total_malaria_acttreated_5p': {'coord': 'E13', 'attr': 'total_malaria_acttreated_5p', 'type': int, 'name': u"Nbre de Cas traités avec CTA (5 ans et +)"},
}


def analyze_xls_form(filepath, reporter):

    status = [UNKNOWN]
    instance = None
    errors = []
    warnings = []

    def add_e(message):
        errors.append(message)
        status.append(REJECTED)

    report = MalariaReport(reporter=reporter)

    try:
        book = xlrd.open_workbook(filepath)
        ws = book.sheet_by_name("Form")
    except:
        add_e(u"Impossible d'ouvrir le masque de saisie. Le fichier est corrompu ou a été modifié.")

    for data_key, data_value in FORM_DATA.items():
        try:
            raw_data = data_for_coord(data_value['coord'], ws)
        except:
            add_e(u"Impossible de lire les données pour %s" % data_value['name'])
            raise

        if raw_data == '':
            raw_data = None

        if not raw_data:
            add_e(u"Pas de données pour %s" % data_value['name'])
            continue

        if data_value['type']:
            try:
                func = data_value['type']
                value = func(raw_data)
            except:
                print raw_data
                print func
                value = raw_data
                add_e(u"Les données de %s (%s) ne sont pas du bon type." % (data_value['name'], raw_data))
        try:
            setattr(report, data_value['attr'], value)
        except:
            raise
            add_e(u"Les données de %s (%s) ne corresponde pas au formulaire." % (data_value['name'], raw_data))

    try:
        report.save()
        status.append(ACCEPTED)
    except db.IntegrityError as e:
        if MalariaReport.objects.filter(health_center=report.health_center, month=report.month, year=report.year).count():
            add_e(u"Un formulaire pour cet établissement et cette période a déjà été envoyé.")
        else:
            #add_e(u"Impossible d'enregistrer le formulaire: %r" % e)
            pass
    except Exception as e:
        add_e(u"Impossible d'enregistrer le formulaire: %r" % e)

    instance = report

    return (status.pop(), errors, instance)
