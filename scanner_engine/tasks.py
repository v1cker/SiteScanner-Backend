import datetime
from celery import task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template
from register_site.models import EntriesIndex
from scanner_engine.models import WatchersIndex, RedirectionsIndex
from scanner_engine.utils.redirection.utils import run_redirection_scan, has_problems_rediretion
from scanner_engine.utils.watcher.utils import run_watcher_scan, has_problems_watcher

logger = get_task_logger(__name__)


@task()
def automatic_scan_task(should_mail_the_user=True):
    logger.info("Run automatic scan...")

    number_of_entries_scanned = 0
    number_of_problems_found = 0

    for entry in EntriesIndex.objects.all():
        number_of_entries_scanned += 1

        if entry.has_redirections():
            if len(RedirectionsIndex.objects.filter(entry=entry)) < 1:
                raise ValueError('Wrong number of Redirections. Should be at least 1, found %d' % (len(RedirectionsIndex.objects.filter(entry=entry))))
            redirections = RedirectionsIndex.objects.filter(entry=entry)
            for redirection in redirections:
                scan_result = run_redirection_scan(redirection)
                if has_problems_rediretion(scan_result):
                    number_of_problems_found += 1

    if should_mail_the_user:
        template = get_template("mail_alert/hero.html")

        context = {
            'date': datetime.datetime.now().date(),
            'full_date': datetime.datetime.now(),
            'number_of_entries': number_of_entries_scanned,
            'number_of_problems': number_of_problems_found
        }

        mail_subject = "Automatyczny skan!"
        mail_message = template.render(context)
        from_email = settings.EMAIL_HOST_USER
        to_emails = [settings.PRIVATE_TARGET_EMAIL]
        message = EmailMessage(mail_subject, mail_message, from_email, to_emails)
        message.content_subtype = "html"
        message.send(fail_silently=True)
