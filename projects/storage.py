from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
import os


class NoCacheStaticFilesStorage(StaticFilesStorage):
    """Static file storage that appends a file-timestamp query param to bust browser cache."""

    def url(self, name):
        url = super().url(name)
        # Check all possible locations: STATIC_ROOT and STATICFILES_DIRS
        paths_to_check = []
        if self.location:
            paths_to_check.append(os.path.join(self.location, name))
        for static_dir in getattr(settings, 'STATICFILES_DIRS', []):
            paths_to_check.append(os.path.join(str(static_dir), name))

        for path in paths_to_check:
            if os.path.exists(path):
                mtime = int(os.path.getmtime(path))
                sep = '&' if '?' in url else '?'
                url = f"{url}{sep}v={mtime}"
                break
        return url
