# Django settings for UniformZulu project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DEVELOPMENT = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/Users/Jeje/Documents/Django_Projects/UniformZulu/media/'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "/Users/Jeje/Documents/Django_Projects/UniformZulu/templates",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
#    'facebook.djangofb.FacebookMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
#    'facebookconnect.middleware.FacebookConnectMiddleware',
    'recaptcha_django.middleware.ReCaptchaMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

AUTHENTICATION_BACKENDS = (
#    'facebookconnect.models.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.comments',
    'django_extensions',
    'registration',
    'notification',
    'recaptcha_django',
    'debug_toolbar',
#    'facebookconnect',
    'south',
    'UniformZulu.googlecharts',
    'UniformZulu.uniformzulu',
)

FACEBOOK_API_KEY = '876536164b1da9367e9cf80c849471cb'
FACEBOOK_SECRET_KEY = 'ef6ffedd867a5c758fe00c0651c45f95'
FACEBOOK_INTERNAL = True

# debug-toolbar
INTERNAL_IPS = ('127.0.0.1',)
LBAR_PANELS = (
	    'debug_toolbar.panels.version.VersionDebugPanel',
	    'debug_toolbar.panels.timer.TimerDebugPanel',
	    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
	    'debug_toolbar.panels.headers.HeaderDebugPanel',
	    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
	    'debug_toolbar.panels.template.TemplateDebugPanel',
#	    'debug_toolbar.panels.sql.SQLDebugPanel',
	    'debug_toolbar.panels.signals.SignalDebugPanel',
	    'debug_toolbar.panels.logger.LoggingPanel',
	)
