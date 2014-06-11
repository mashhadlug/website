from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import logging
import os

class Pagination(IPlugin):
  """ Class doc """
  
  def __init__ (self):
    """ Class initialiser """
    # Make sure calling parent's __init__ method when overriding it
    super(Pagination, self).__init__()
    logging.debug('Pagination, __init__')
    
    # Get app.env
    self.manager = PluginManagerSingleton.get()
    
  def activate (self):
    """ Function doc """
    super(Pagination, self).activate()
    logging.debug('Pagination, activate')
    
    self.manager.app.env.globals.update(pagination=self.pagination)
  
  def deactivate (self):
    """ Function doc """
    super(Pagination, self).deactivate()
    logging.debug('Pagination, deactivate')
  
  def pagination(self, content, path, page, prefix="pagination_"):
    filepath = os.path.join(path, "pagination_%s.html" % page)
    f = open(filepath, "w")
    f.write(content.encode('utf8'))
    f.close()
    return ""
