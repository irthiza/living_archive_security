from django.contrib.humanize.templatetags.humanize import naturaltime
from django.urls import reverse
import calendar
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.utils.http import urlencode
import re


def choices_with_label(choices):
    return [("", "Select from items"), ] + list(choices)[1:]


def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    """Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    """
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url


def month_list():
    months = []
    for month_idx in range(1, 13):
        months.append((month_idx, calendar.month_name[month_idx]))
    return months


def day_list():
    day = []
    for index in range(1, 32):
        day.append((index, index))
    return day


def last_year_month():
    now = timezone.now()
    month = now.month - 1
    year = now.year
    if now.month == 1:
        month = 12
        year = now.year - 1
    return {
        'year': year,
        'month': month
    }


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


def reformat_string(created_at):
    if created_at:
        if (timezone.now() - created_at).days > 6:
            return created_at.strftime("%b %d, %Y")
        new_string = naturaltime(created_at).replace('\xa0', ' ')
        if ',' in new_string:
            return f"{new_string.split(',')[0]} ago"
        return new_string
    return None


class PermissionRequiredMixin(UserPassesTestMixin):
    permission_required = None

    def test_func(self):
        if self.permission_required is None:
            raise ValueError("You must set the 'permission_required' attribute on your view.")

        user = self.request.user
        if user.has_perm(self.permission_required):
            return True
        else:
            raise PermissionDenied
