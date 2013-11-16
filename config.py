import os
import logging

# Default URL: if no Redirect URL can be generated, traffic will be diverted here
DEFAULT_URL = 'http://default.new-domain.com/'

# Mapping of Source URLs to Target URLs.
# You can choose to map in 2 ways:
#    1) to the new URL maintaining the same Path (i.e. 'www.old.com/p/a/t/h/index.html -> www.new.com/p/a/t/h/index.html')
#    2) or to discard the Path (i.e. 'www.old.com/p/a/t/h/index.html -> www.new.com')
# Format:
#    URLS = { 'Old Domain': ('New Domain', 'Discard URL Path part and Redirect to Root?'), ... }
URLS = {
   '%s.appspot.com' % (os.environ['APPLICATION_ID']) : ('www.new-domain.com', False),
   'www.old-domain.com' : ('www.new-domain.com', False),
   'downloads.old-domain.com': ('downloads.new-domain.com', False),
   'stuff.old-domain.com': ('stuff.new-domain.com', True),
};

# Send email message when redirect error occurs
ERROR_EMAIL_ACTIVE = True;
ERROR_EMAIL_SENDER = '"Redirector for new-domain.com" <your@email.com>';
ERROR_EMAIL_SUBJECT = 'Redirect Script Error';
ERROR_EMAIL_BODY = 'Unable to redirect this url: ';

# Check if the destination URL exists BEFORE redirecting
CHECK_URL_EXISTANCE = True;

# Memcache redirection results
MEMCACHE_ACTIVE = True;
MEMCACHE_EXPIRES_IN_SECONDS = 86400; # 1 day

# Logging level
LOGGING_LEVEL = logging.WARNING;
