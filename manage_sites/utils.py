from django.utils import timezone


def calculate_time_passed(date):
    time_passed = timezone.now() - date
    # If it's less than one day, show value in hours.
    if time_passed.days > 0:
        time_passed = str(time_passed.days) + ' days'
    # If it's less than an hour, show value in minutes
    elif time_passed.seconds/60/60 > 0:
        time_passed = str(time_passed.seconds/60/60) + ' hours'
    else:
        time_passed = str(time_passed.seconds/60) + ' minutes'

    return time_passed