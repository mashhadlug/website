from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import logging
import datetime

class Simple(IPlugin):
  """ Class doc """
  
  def __init__ (self):
    """ Class initialiser """
    # Make sure calling parent's __init__ method when overriding it
    super(Simple, self).__init__()
    logging.debug('Defaults, __init__')
    
    # Get app.env
    self.manager = PluginManagerSingleton.get()
    
  def activate (self):
    """ Function doc """
    super(Simple, self).activate()
    logging.debug('Defaults, activate')
    
    manager = PluginManagerSingleton.get()
    manager.app.parser.add_argument('-u', '--base-url',
      metavar='BASE_URL', type=str, default="",
      help='default base_url is /')
    
    manager.app.env.filters.update(date_printable=self.date_printable)
    manager.app.env.filters.update(date_iso=self.date_iso)
    manager.app.env.filters.update(link=self.link)
    manager.app.env.filters.update(sort_ctime=self.sort_ctime)
    manager.app.env.filters.update(sort_navbar_by=self.sort_navbar_by)
    manager.app.env.filters.update(sort_by_name=self.sort_by_name)
    manager.app.env.filters.update(sort_by_published=self.sort_by_published)
  
  def deactivate (self):
    """ Function doc """
    super(Simple, self).deactivate()
    logging.debug('Defaults, deactivate')
  
  def date_printable (self, timestamp, format="%B %d, %Y"):
    date = datetime.datetime.fromtimestamp(timestamp)
    return datetime.datetime.strftime(date, format)
  
  def date_iso (self, timestamp):
    date = datetime.datetime.fromtimestamp(timestamp)
    # FIXME: it's nice to be timezone-aware
    return datetime.datetime.strftime(date, "%Y-%m-%dT%H:%M:%SZ")

  def link (self, link):
    if link.startswith('http'):
      return link
    else:
      manager = PluginManagerSingleton.get()
      base_url = manager.app.args['base_url']
      if len(base_url) > 0 and not base_url.startswith("http") and not base_url.startswith("/"):
        base_url = "/" + base_url
      return base_url + link
  
  def sort_ctime (self, items, reverse=False):
    return sorted(items, key = lambda x: x.ctime , reverse=reverse)
  
  def sort_by_name (self, items, reverse=False):
    return sorted(items, key = lambda x: x.name , reverse=reverse)
  
  def sort_by_published (self, items, reverse=False):
    return sorted(items, key = lambda x: x.published , reverse=reverse)
  
  def  sort_navbar_by(self, items, key='row', reverse=False):
    """ Function doc """
    navbar_items = filter(lambda x: x.navbar!=None,  items)
    return sorted(navbar_items, key = lambda x: x.navbar.get(key, None) , reverse=reverse)
