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

VALUES_YN = {u"Oui": MalariaReport.YES, u"Non": MalariaReport.NO}


class mapping(object):
    pass

FORM_DATA = {
   '0.1': {
    'region': \
        {'coord': 'B2', 'attr': 'region', \
         'type': unicode, 'name': u"Région"},
    'district': \
        {'coord': 'B3', 'attr': 'district', \
         'type': unicode, 'name': u"District sanitaire"},
    'hc': \
        {'coord': 'B4', 'attr': 'health_center', \
         'type': unicode, 'name': u"Établissement sanitaire"},
    'month': \
        {'coord': 'D3', 'attr': 'month', \
         'type': int, 'name': u"Mois"},
    'year': \
        {'coord': 'G3', 'attr': 'year', \
         'type': int, 'name': u"Année"},

    'total_consultation_u5': \
        {'coord': 'C7', 'attr': 'total_consult_u5', \
         'type': int, \
         'name': u"Total consultation, toutes causes confondues (< 5ans)"},
    'total_consultation_5p': \
        {'coord': 'E7', 'attr': 'total_consult_5p', \
         'type': int, \
         'name': u"Total consultation, toutes causes confondues (5 ans et +)"},
    'total_consultation_fe': \
        {'coord': 'G7', 'attr': 'total_consult_fe', \
         'type': int, \
         'name': u"Total consultation, toutes causes " \
                  "confondues (femmes enceintes)"},

    'total_malaria_u5': \
        {'coord': 'C8', 'attr': 'total_malaria_u5', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme (Tous suspectés) (< 5ans)"},
    'total_malaria_5p': \
        {'coord': 'E8', 'attr': 'total_malaria_5p', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme (Tous suspectés) (5 ans et +)"},

    'total_malaria_simple_u5': \
        {'coord': 'C9', 'attr': 'total_malaria_simple_u5', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme Simple (< 5ans)"},
    'total_malaria_simple_5p': \
        {'coord': 'E9', 'attr': 'total_malaria_simple_5p', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme Simple (5 ans et +)"},

    'total_malaria_severe_u5': \
        {'coord': 'C10', 'attr': 'total_malaria_severe_u5', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme Grave (< 5ans)"},
    'total_malaria_severe_5p': \
        {'coord': 'E10', 'attr': 'total_malaria_severe_5p', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme Grave (5 ans et +)"},
    'total_malaria_severe_fe': \
        {'coord': 'G10', 'attr': 'total_malaria_severe_fe', \
         'type': int, \
         'name': u"Nbre de Cas de paludisme Grave (femmes enceintes)"},

    'total_malaria_tested_u5': \
        {'coord': 'C11', 'attr': 'total_malaria_tested_u5', \
         'type': int, \
         'name': u"Cas de paludisme testés (GE et/ou TDR) (< 5ans)"},
    'total_malaria_tested_5p': \
        {'coord': 'E11', 'attr': 'total_malaria_tested_5p', \
         'type': int, \
         'name': u"Cas de paludisme testés (GE et/ou TDR) (5 ans et +)"},
    'total_malaria_tested_fe': \
        {'coord': 'G11', 'attr': 'total_malaria_tested_fe', \
         'type': int, \
         'name': u"Cas de paludisme testés " \
                  "(GE et/ou TDR) (femmes enceintes)"},

    'total_malaria_confirmed_u5': \
        {'coord': 'C12', 'attr': 'total_malaria_confirmed_u5', \
         'type': int, \
         'name': u"Cas de paludisme confirmés (GE et/ou TDR) (< 5ans)"},
    'total_malaria_confirmed_5p': \
        {'coord': 'E12', 'attr': 'total_malaria_confirmed_5p', \
         'type': int, \
         'name': u"Cas de paludisme confirmés (GE et/ou TDR) (5 ans et +)"},
    'total_malaria_confirmed_fe': \
        {'coord': 'G12', 'attr': 'total_malaria_confirmed_fe', \
         'type': int, \
         'name': u"Cas de paludisme confirmés " \
                  "(GE et/ou TDR) (femmes enceintes)"}, \

    'total_malaria_acttreated_u5': \
        {'coord': 'C13', 'attr': 'total_malaria_acttreated_u5', \
         'type': int, \
         'name': u"Nbre de Cas traités avec CTA (< 5ans)"}, \
    'total_malaria_acttreated_5p': \
        {'coord': 'E13', 'attr': 'total_malaria_acttreated_5p', \
         'type': int, \
         'name': u"Nbre de Cas traités avec CTA (5 ans et +)"}, \

    'total_malaria_inpatient_u5': \
        {'coord': 'C17', 'attr': 'total_malaria_inpatient_u5', \
         'type': int, \
         'name': u"Total Hospitalisés Paludisme (< 5ans)"}, \
    'total_malaria_inpatient_5p': \
        {'coord': 'E17', 'attr': 'total_malaria_inpatient_5p', \
         'type': int, \
         'name': u"Total Hospitalisés Paludisme (5 ans et +)"}, \
    'total_malaria_inpatient_fe': \
        {'coord': 'G17', 'attr': 'total_malaria_inpatient_fe', \
         'type': int, \
         'name': u"Total Hospitalisés Paludisme (femmes enceintes)"}, \

    'total_inpatient_u5': \
        {'coord': 'C18', 'attr': 'total_inpatient_u5', \
         'type': int, \
         'name': u"Total Hospitalisations toutes causes " \
                 u"confondues (< 5ans)"}, \
    'total_inpatient_5p': \
        {'coord': 'E18', 'attr': 'total_inpatient_5p', \
         'type': int, \
         'name': u"Total Hospitalisations toutes causes " \
                 u"confondues (5 ans et +)"}, \
    'total_inpatient_fe': \
        {'coord': 'G18', 'attr': 'total_inpatient_fe', \
         'type': int, \
         'name': u"Total Hospitalisations toutes causes " \
                 u"confondues (femmes enceintes)"}, \

    'total_malaria_death_u5': \
        {'coord': 'C22', 'attr': 'total_malaria_death_u5', \
         'type': int, \
         'name': u"Cas de décès pour paludisme (< 5ans)"}, \
    'total_malaria_death_5p': \
        {'coord': 'E22', 'attr': 'total_malaria_death_5p', \
         'type': int, \
         'name': u"Cas de décès pour paludisme (5 ans et +)"}, \
    'total_malaria_death_fe': \
        {'coord': 'G22', 'attr': 'total_malaria_death_fe', \
         'type': int, \
         'name': u"Cas de décès pour paludisme (femmes enceintes)"}, \

    'total_death_u5': \
        {'coord': 'C23', 'attr': 'total_death_u5', \
         'type': int, \
         'name': u"Total cas de décès toutes causes " \
                 u"confondues (< 5ans)"}, \
    'total_death_5p': \
        {'coord': 'E23', 'attr': 'total_death_5p', \
         'type': int, \
         'name': u"Total cas de décès toutes causes " \
                 u"confondues (5 ans et +)"}, \
    'total_death_fe': \
        {'coord': 'G23', 'attr': 'total_death_fe', \
         'type': int, \
         'name': u"Total cas de décès toutes causes " \
                 u"confondues (femmes enceintes)"}, \

    'total_bednets_u5': \
        {'coord': 'C27', 'attr': 'total_bednets_u5', \
         'type': int, \
         'name': u"Nombre de moustiquaires distribuées " \
                 u"(< 5ans)"}, \
    'total_bednets_fe': \
        {'coord': 'E27', 'attr': 'total_bednets_fe', \
         'type': int, \
         'name': u"Nombre de moustiquaires distribuées " \
                 u"(femmes enceintes)"}, \

    'total_cpn1_fe': \
        {'coord': 'M22', 'attr': 'total_cpn1_fe', \
         'type': int, \
         'name': u"Nombre de CPN 1"}, \
    'total_sp1_fe': \
        {'coord': 'M23', 'attr': 'total_sp1_fe', \
         'type': int, \
         'name': u"Nombre de SP1"}, \
    'total_sp2_fe': \
        {'coord': 'M24', 'attr': 'total_sp2_fe', \
         'type': int, \
         'name': u"Nombre de SP2"}, \

    'stockout_act_infant': \
        {'coord': 'M5', 'attr': 'stockout_act_infant', \
         'type': mapping, \
         'name': u"[rupture] CTA Nourisson - Enfant", \
         'options_values': VALUES_YN}, \
    'stockout_act_kid': \
        {'coord': 'M6', 'attr': 'stockout_act_kid', \
         'type': mapping, \
         'name': u"[rupture] CTA Grand Enfant", \
         'options_values': VALUES_YN}, \
    'stockout_act_adult': \
        {'coord': 'M7', 'attr': 'stockout_act_adult', \
         'type': mapping, \
         'name': u"[rupture] CTA Adulte", \
         'options_values': VALUES_YN}, \

    'stockout_arthemether': \
        {'coord': 'M11', 'attr': 'stockout_arthemether', \
         'type': mapping, \
         'name': u"[rupture] Arthemether", \
         'options_values': VALUES_YN}, \
    'stockout_quinine': \
        {'coord': 'M12', 'attr': 'stockout_quinine', \
         'type': mapping, \
         'name': u"[rupture] Quinine Injectable", \
         'options_values': VALUES_YN}, \
    'stockout_serum': \
        {'coord': 'M13', 'attr': 'stockout_serum', \
         'type': mapping, \
         'name': u"[rupture] Serum", \
         'options_values': VALUES_YN}, \

    'stockout_mild': \
        {'coord': 'M16', 'attr': 'stockout_mild', \
         'type': mapping, \
         'name': u"[rupture] MILD", \
         'options_values': VALUES_YN}, \
    'stockout_rdt': \
        {'coord': 'M17', 'attr': 'stockout_rdt', \
         'type': mapping, \
         'name': u"[rupture] TDR", \
         'options_values': VALUES_YN}, \
    'stockout_sp': \
        {'coord': 'M18', 'attr': 'stockout_sp', \
         'type': mapping, \
         'name': u"[rupture] SP", \
         'options_values': VALUES_YN}, \
    }
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
        add_e(u"Impossible d'ouvrir le masque de saisie. " \
              u"Le fichier est corrompu ou a été modifié.")

    # retrieve form version
    try:
        version = data_for_coord('N1', ws)
        form = FORM_DATA[version]
    except:
        add_e(u"Impossible de déterminer la version du formulaire. " \
              u"Le fichier est corrompu ou a été modifié.")

    for data_key, data_value in form.items():
        try:
            raw_data = data_for_coord(data_value['coord'], ws)
        except:
            add_e(u"Impossible de lire les données pour %s" \
                  % data_value['name'])
            raise

        if raw_data == '':
            raw_data = None

        if raw_data == None:
            add_e(u"Pas de données pour %s" % data_value['name'])
            continue

        if data_value['type'] and data_value['type'] in (int, float, unicode):
            try:
                func = data_value['type']
                value = func(raw_data)
            except:
                print raw_data
                print func
                value = raw_data
                add_e(u"Les données de %s (%s) ne sont pas du bon type." \
                      % (data_value['name'], raw_data))

        if data_value['type'] and data_value['type'] == mapping:
            print data_value['name']
            try:
                raw_data = raw_data.strip().lower()
                options = [x.lower() for x \
                                     in data_value['options_values'].keys()]
                if raw_data in options:
                    index = options.index(raw_data)
                    print index
                    value = data_value['options_values'].values()[index]
                    print "yes"
                else:
                    value = raw_data
                    print "no"
                    add_e(u"Les données de %s (%s) doivent faire " \
                          u"partie de %s" \
                          % (data_value['name'], raw_data, \
                             data_value['options_values'].keys()))
            except IndexError:
                add_e(u"Pas de correspondance de valeur pour %s (%s)" \
                      % (data_value['name'], raw_data))
                print "indexe"
            except:
                print "err"
                raise
                value = raw_data

            print "v: %s" % value

        try:
            setattr(report, data_value['attr'], value)
        except:
            raise
            add_e(u"Les données de %s (%s) ne corresponde pas au " \
                   "formulaire." \
                  % (data_value['name'], raw_data))

    try:
        period = Period.get_or_create(report.month, report.year)
        print "period: %s" % period
        report.period = period
    except:
        add_e(u"Impossible de déterminer la période.")

    try:
        report.save()
        status.append(ACCEPTED)
    except db.IntegrityError as e:
        if MalariaReport.objects.filter(health_center=report.health_center, \
                                        month=report.month, \
                                        year=report.year).count():
            add_e(u"Un formulaire pour cet établissement et " \
                  u"cette période a déjà été envoyé.")
        else:
            add_e(u"Impossible d'enregistrer le formulaire: %r" % e)
    except Exception as e:
        add_e(u"Impossible d'enregistrer le formulaire: %r" % e)

    instance = report

    return (status.pop(), errors, instance)
