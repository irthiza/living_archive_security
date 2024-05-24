from django.db.models import Q
import operator
from functools import reduce
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth import logout


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        if self.kwargs['pk'].isdigit():
            obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        else:
            obj = get_object_or_404(queryset, slug=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class LogoutIfNotStaffMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.is_staff:
            logout(request)
            return self.handle_no_permission()
        return super(LogoutIfNotStaffMixin, self).dispatch(request, *args, **kwargs)
