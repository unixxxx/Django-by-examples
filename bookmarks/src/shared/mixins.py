from django.http import HttpResponseBadRequest
from django.views.generic import View


class AjaxRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return super(AjaxRequiredMixin, self).dispatch(request, *args, **kwargs)
