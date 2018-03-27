import json
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
try:
    from django.utils.encoding import force_unicode as force_text  # Django < 1.5
except ImportError as e:
    from django.utils.encoding import force_text  # Django 1.5 / python3
from django.utils.functional import Promise
from django.utils.translation import ugettext as _
from django.utils.cache import add_never_cache_headers
from django.views.generic.base import TemplateView
from django.utils.timezone import utc,localtime
import logging
logger = logging.getLogger(__name__)


class LazyEncoder(DjangoJSONEncoder):
    """Encodes django's lazy i18n strings
    """
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        elif isinstance(obj, datetime.datetime):
            # 处理时间为本地时间
            # return localtime(obj.replace(tzinfo=utc)).strftime("%Y-%m-%d %H:%M:%S")
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super(LazyEncoder, self).default(obj)


class JSONResponseMixin(object):
    is_clean = False

    def render_to_response(self, context):
        """ Returns a JSON response containing 'context' as payload
        """
        return self.get_json_response(context)

    def get_json_response(self, content, **httpresponse_kwargs):
        """ Construct an `HttpResponse` object.
        """
        response = HttpResponse(content,
                                content_type='application/json',
                                **httpresponse_kwargs)
        add_never_cache_headers(response)
        return response

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.request = request
        response = None

        try:
            func_val = self.get_context_data(**kwargs)
            if not self.is_clean:
                assert isinstance(func_val, dict)
                response = dict(func_val)
                if 'error' not in response and 'sError' not in response:
                    response['result'] = 'ok'
                else:
                    response['result'] = 'error'
            else:
                response = func_val
        except KeyboardInterrupt:
            # Allow keyboard interrupts through for debugging.
            raise
        except Exception as e:
            logger.error('JSON view error: %s' % request.path, exc_info=True)

            # Come what may, we're returning JSON.
            if hasattr(e, 'message'):
                msg = e.message
                msg += str(e)
            else:
                msg = _('Internal error') + ': ' + str(e)
            response = {'result': 'error',
                        'sError': msg,
                        'text': msg}

        dump = json.dumps(response, cls=LazyEncoder)
        return self.render_to_response(dump)


class JSONResponseView(JSONResponseMixin, TemplateView):
    pass
