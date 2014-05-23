from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import logging

class Navbar(IPlugin):
  """ Class doc """
  
  def __init__ (self):
    """ Class initialiser """
    # Make sure calling parent's __init__ method when overriding it
    super(Navbar, self).__init__()
    logging.debug('Navbar, __init__')
    
    # Get app.env
    self.manager = PluginManagerSingleton.get()
    
  def activate (self):
    """ Function doc """
    super(Navbar, self).activate()
    logging.debug('Navbar, activate')
    
    self.manager.app.env.filters.update(sort_navbar_by=self.sort_navbar_by)
  
  def deactivate (self):
    """ Function doc """
    super(Navbar, self).deactivate()
    logging.debug('Navbar, deactivate')
  
  def  sort_navbar_by(self, items, key='row', reverse=False):
    """ Function doc """
    return sorted(items, key = lambda x: x.navbar.get(key, None) , reverse=reverse)
