from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManagerSingleton
import markdown
import logging
import re

class Markdown(IPlugin):
  """ Class doc """
  
  def __init__ (self):
    """ Class initialiser """
    # Make sure calling parent's __init__ method when overriding it
    super(Markdown, self).__init__()
    logging.debug('Markdown, __init__')
    
    # Get app.env
    manager = PluginManagerSingleton.get()
    self.env = manager.app.env
  
  def activate (self):
    """ Function doc """
    # Make sure calling parent's activate method when overriding it
    super(Markdown, self).activate()
    logging.debug('Markdown, activate')
    
    # Adding markdown filter to app.env
    self.env.filters.update(markdown=self.markdown_filter)
    self.env.filters.update(markdown_short_story=self.markdown_short_story_filter)
    self.env.filters.update(markdown_less_story=self.markdown_less_story_filter)
  
  def deactivate (self):
    """ Function doc """
    # Make sure calling parent's deactivate method when overriding it
    super(Markdown, self).deactivate()
    logging.debug('Markdown, deactivate')
  
  def markdown_filter (self, content):
    """ Function doc """
    if content is not None:
      return markdown.markdown(content)
    return ''
  
  def markdown_short_story_filter (self, content):
    if content is not None:
      less = more = ""
      if "<!--more-->" in content:
        less, more = content.split("<!--more-->")
      titles = []
      for title in re.findall("((\* )?##[^\n]+)", more):
        titles.append(title[0])
      short_story_body = less + '\n\n'.join(titles)
      return short_story_body
    return ''
  
  def markdown_less_story_filter (self, content):
    if content is not None:
      less = more = ""
      if "<!--more-->" in content:
        less, more = content.split("<!--more-->")
        return less
    return ''
