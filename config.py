import os
import logging

# Default URL: if no Redirect URL can be generated, traffic will be diverted here
DEFAULT_URL = 'http://www.ivandemarino.me/'

# Old Domain: New Domain, Map urls (redirect to Root ('mydomain.com/'))
URLS = {
   '%s.appspot.com' % (os.environ['APPLICATION_ID']) : ('blog.ivandemarino.me', False),
   'redirector.ivandemarino.me' : ('blog.ivandemarino.me', False),
   'detronizator.org': ('blog.ivandemarino.me', False),
	'www.detronizator.org': ('blog.ivandemarino.me', False),
	'downloads.detronizator.org': ('www.ivandemarino.me', True),
};

ERROR_EMAIL_SENDER = '"Redirector (blog.ivandemarino.me)" <detronizator@gmail.com>';
ERROR_EMAIL_SUBJECT = 'Redirect Script Error';
ERROR_EMAIL_BODY = 'Unable to redirect this url: ';

CHECK_URL_EXISTANCE = True;

MEMCACHE_ACTIVE = True;
MEMCACHE_EXPIRES_IN_SECONDS = 86400; # 1 day

LOGGING_LEVEL = logging.WARNING;