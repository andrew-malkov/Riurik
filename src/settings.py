#######################################################################################
# Django settings for web_reports project.
import os, platform, sys
from local_settings import *

if getattr(sys, 'frozen', False):
    working_dir = sys._MEIPASS
else:
    working_dir = os.path.dirname(os.path.abspath(__file__))
print "working_dir %s" % working_dir
root = os.path.normpath(os.path.dirname(working_dir))
sys.path.append(working_dir)

try:
    from local_settings import VIRTUAL_PATHS
    virtual_paths_py = 'virtual_paths.py'
except ImportError:
    from virtual_paths_default import VIRTUAL_PATHS
    virtual_paths_py = 'virtual_paths_default.py'

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
    }
}

DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
DATABASE_OPTIONS = {'timeout': 30}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
} 

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Moscow'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.dirname( __file__ ) + '/static'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '(nf!nzz3a&uxzbdb)9*hor38)*a4&m)szzbn$&8wy*&h7t*v_-'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
)
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sessions'))
#SESSION_ENGINE = "django.contrib.sessions.backends.cache"
CACHE_BACKEND = 'locmem://'
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = False
CACHE_MIDDLEWARE_SECONDS = 600

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
)

if not os.path.exists(SESSION_FILE_PATH):
    os.makedirs(SESSION_FILE_PATH)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (

    os.path.join(os.path.dirname( __file__ ), 'templates'),
    os.path.join(os.path.dirname( __file__ ), 'plugins', 'search', 'templates'),
    os.path.join(os.path.dirname( __file__ ), 'plugins', 'github', 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'src',
    'src.plugins.search',
    'src.plugins.git',
    'src.plugins.github',
)

def appInstalled(app_name):
    return app_name in INSTALLED_APPS

if platform.system() == 'Windows':
    nodejs = os.path.join(os.environ['ProgramFiles'], 'nodejs', 'node.exe')
    coffee = os.path.join(r'C:\CoffeeScript', 'bin', 'coffee')
    COFFEESCRIPT_EXECUTABLE = '"%s" "%s"' % (nodejs, coffee)
    DASPEC_EXECUTABLE = 'daspec'
elif platform.system() == 'Linux':
    COFFEESCRIPT_EXECUTABLE = 'coffee'
else:
    COFFEESCRIPT_EXECUTABLE = None

DEFAULT = 'DEFAULT'
EXEC_TESTS_CMD='static/testLoader.html'
SUITE_SETUP_FILE_NAME = 'suite-setup.js'
SPEC_URL_FILE_NAME = '.specification.ini'
TEST_CONTEXT_FILE_NAME = '.context.ini'
GLOBAL_CONTEXT_FILE_NAME = '.settings.ini'
TEST_CONTEXT_JS_FILE_NAME = '.context.js'
JS_FILE_EXT = '.js'
INI_FILE_EXT = '.ini'
COFFEE_FILE_EXT = '.coffee'
CUCUMBER_FILE_EXT = '.feature'
DASPEC_FILE_EXT = '.daspec'
TEST_SWAP_FILE_NAME = '.%s.swp'
LIB_KEY_NAME = 'libraries'
LIB_DEFAULT_NAME = 'library.js'
APPEND_SLASH = False
CODEMIRROR_CALL_EDITOR_FOR = '^.*\.(?:js|ini|html|py)$'
INCLUDE_KEY = 'include'
EXCLUDE_KEY = 'exclude'
SUITE_SETUP = 'suite_setup'
PRODUCT_CODE_PATH = 'product_code_path'
PRODUCT_CODE_ALIAS = 'product_code_alias'

STATIC_MANAGEMENT_ASSET_PATHS = []
STATIC_MANAGEMENT_HOSTNAMES = ['http://www.riurik.com']
STATIC_MANAGEMENT_VERSIONER = 'plugins.static_management.versioners.SHA1Sum'

chaiPack = [
	'chai/chai.js',
	'chai/chai-jquery.js'
]

STATIC_MANAGEMENT = {
    'js': {
        'qunit.testLoader.js': [
            'js/jquery.min.js',
            'js/jquery.json.min.js',
            'js/dates.js',
            'js/tools.js',
            'js/riurik.js',
            'js/consoles.js',
            'js/reporting.js',
            'js/frame.js',
            'js/errors.js',
            'engines/qunit/connector.js',
            'engines/qunit/qunit.html.js',
            'engines/qunit/qunit.js',
            'engines/qunit/qunit.extentions.js'
        ]
    },
    'css': {
        
    }
}

cucumberSTATIC_MANAGEMENT = {
    'js': {
        'cucumber.testLoader.js': [
            'js/jquery.min.js',
            'js/jquery.json.min.js',
            'js/dates.js',
            'js/tools.js',
            'js/riurik.js',
            'js/consoles.js',
            'js/reporting.js',
            'js/frame.js',
            'js/errors.js',
            'engines/cucumber/connector.js',
            'engines/cucumber/cucumber.js',
        ]
    },
    'css': {
        
    }
}

mochaSTATIC_MANAGEMENT = {
    'js': {
        'mocha.testLoader.js': [
            'js/jquery.min.js',
            'js/jquery.json.min.js',
            'js/dates.js',
            'js/tools.js',
            'js/riurik.js',
            'js/consoles.js',
            'js/reporting.js',
            'js/frame.js',
            'js/errors.js',
            'engines/mocha/connector.js',
            'engines/mocha/mocha.html.js',
            'engines/mocha/mocha.js',
        ] + chaiPack
    },
    'css': {
        
    }
}

jasmineSTATIC_MANAGEMENT = {
    'js': {
        'jasmine.testLoader.js': [
            'js/jquery.min.js',
            'js/jquery.json.min.js',
            'js/dates.js',
            'js/tools.js',
            'js/riurik.js',
            'js/consoles.js',
            'js/reporting.js',
            'js/frame.js',
            'js/errors.js',
            'engines/jasmine/connector.js',
            'engines/jasmine/jasmine.js',
            'engines/jasmine/jasmine-html.js',
        ]
    },
    'css': {
        
    }
}
