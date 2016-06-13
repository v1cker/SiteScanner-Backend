from django.shortcuts import render
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
import datetime
# Create your views here.


def send_periodic_scan_results(entries_scanned, recivers):

    template = get_template('mail_alert/hero.html')

    number_of_sites_scanned = 0
    number_of_redirections_scanned = 0
    for entry in entries_scanned:
        if entry.is_page():
            number_of_sites_scanned += 1
        elif entry.is_redirection():
            number_of_redirections_scanned += 1
    context = {
        'date': datetime.datetime.now().date(),
        'full_date': datetime.datetime.now(),
        'number_of_entries': len(entries_scanned),
        'number_of_problems': 0,
        'sites': number_of_sites_scanned,
        'redirections': number_of_redirections_scanned
    }