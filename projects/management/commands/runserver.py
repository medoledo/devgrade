from django.contrib.staticfiles.management.commands.runserver import Command as BaseCommand
from django.contrib.staticfiles.handlers import StaticFilesHandler as BaseStaticFilesHandler


class NoCacheStaticFilesHandler(BaseStaticFilesHandler):
    """StaticFilesHandler that forces no-cache headers on every static file response."""

    def __call__(self, environ, start_response):
        def no_cache_start_response(status, headers, exc_info=None):
            # Strip any existing cache headers
            headers = [(k, v) for k, v in headers if k.lower() not in ('cache-control', 'pragma', 'expires')]
            headers.append(('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0'))
            headers.append(('Pragma', 'no-cache'))
            headers.append(('Expires', '0'))
            return start_response(status, headers, exc_info)

        return super().__call__(environ, no_cache_start_response)


class Command(BaseCommand):
    def get_handler(self, *args, **options):
        # Skip BaseCommand.get_handler (which wraps with the default StaticFilesHandler)
        # and go straight to the grandparent to get the raw WSGI handler.
        from django.core.management.commands.runserver import Command as RunserverCommand
        handler = RunserverCommand.get_handler(self, *args, **options)
        if options['use_static_handler']:
            return NoCacheStaticFilesHandler(handler)
        return handler
