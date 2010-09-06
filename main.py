# App Name: Redirector
# Author: Ivan De Marino - ivan.de.marino@gmail.com
# Forked from: http://blog.dantup.com/2010/01/generic-redirection-script-for-google-app-engine

import webob
import urlparse
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.api import memcache

import config


# Check if a URL exists, trying a URL Fetch
def check_url_exists(url):
   # Search the Memcache
   memcachekey = "check_url_exists-" + url;
   result = memcache.get(memcachekey) if config.MEMCACHE_ACTIVE else None;
   
   # Nothing in Memcache
   if ( result == None ):
      logging.debug("Existence of URL '%s' not in Memcache" % (url) );
      try:
         response = urlfetch.fetch(url, allow_truncated=True, deadline=10); # Wait as much as possible: 10 sec
         if ( response.status_code == 200 ):
            logging.debug("Verified URL '%s' existence" % (url));
            result = True;
         else:
            logging.error("Unable to Verify URL '%s' existence" % (url));
            result = False;
      except:
         # In case of InvalidURLError or DownloadError
         logging.error("Exception while Verifying URL '%s' existence" % (url));
         result = False;
      
      # Store the result in Memcache for config.MEMCACHE_EXPIRES_IN_SECONDS
      memcache.set(memcachekey, result, time=config.MEMCACHE_EXPIRES_IN_SECONDS);
   
   return result;


# Generates the URL to redirect to
def get_redirect_url(url):
   # Search the Memcache
   memcachekey = "get_redirect_url-" + url;
   result = memcache.get(memcachekey) if config.MEMCACHE_ACTIVE else None;
   
   # Nothing in Memcache
   if ( result == None ):
      logging.debug("Redirect for URL '%s' not in Memcache" % (url) );
      scheme, netloc, path, query, fragment = urlparse.urlsplit(url);
	
      # Discard any port number from the hostname
      netloc = netloc.split(':', 1)[0];
	
   	# Fix empty paths to be just '/' for consistency
      if path == '':
         path = '/';
	
   	# Check if we have a mapping for this domain
      if netloc in config.URLS:
         # Grab the redirect info tuple
         redirect_info = config.URLS[netloc];
         # Root redirects
         if redirect_info[1]:
            result = 'http://' + redirect_info[0] + '/';
            logging.debug("Redirecting to Root: " + result);
         # Paths
         else:
            result = urlparse.urlunsplit(['http', redirect_info[0], path, query, fragment]);
            logging.debug("Redirecting to Precise Path: " + result);
      # No mapping, so return None
      else:
         logging.debug("No Mapping found for: " + url);
         result = None;
   	
      # Store the result in Memcache for config.MEMCACHE_EXPIRES_IN_SECONDS
      memcache.set(memcachekey, result, time=config.MEMCACHE_EXPIRES_IN_SECONDS);

   return result;
		

# Main Request Handler
class MainHandler(webapp.RequestHandler):
   def get(self):
      # Perform redirect
      url = get_redirect_url(self.request.url);

      # Check that we were able to build a URL and that this URL actually exists
      if url and check_url_exists(url):
         logging.info("Redirecting URL '%s' to URL '%s'" % (self.request.url, url) );
         self.redirect(url, permanent=True);
      else:
         # Log that we didn't know what this was, and redirect to a good default
         logging.error("Unable to Redirect URL '%s'" % (self.request.url) );
         mail.send_mail_to_admins(
            sender=config.ERROR_EMAIL_SENDER,
            subject=config.ERROR_EMAIL_SUBJECT,
            body=config.ERROR_EMAIL_BODY + self.request.url
         );
         self.redirect(config.DEFAULT_URL, permanent=True);


application = webapp.WSGIApplication([("/.*", MainHandler)], debug=True);


def main():
   logging.getLogger().setLevel(config.LOGGING_LEVEL);
   run_wsgi_app(application);


if __name__ == "__main__":
   main();

   