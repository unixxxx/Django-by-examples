from django.http import HttpResponseBadRequest


class AjaxRequiredMixin():
    def dispatch(self, request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return super(AjaxRequiredMixin).dispatch(request, args, kwargs)
