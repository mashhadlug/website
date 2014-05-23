#!/usr/bin/python
# from lib import SourceTree
import jinja2
from jinja2.exceptions import TemplateNotFound
import markdown
import os
import datetime
import re
import argparse

from yapsy.PluginManager import PluginManagerSingleton
from yapsy.VersionedPluginManager import VersionedPluginManager
import logging
import shutil, errno


import yaml
from yaml import Loader, SafeLoader
def construct_yaml_str(self, node):
  # Override the default string handling function 
  # to always return unicode objects
  return self.construct_scalar(node)
Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)

def utf8 (func):
  def inner(*args, **kwargs):
    output = func(*args, **kwargs)
    if isinstance(output, str):
      output = output.decode('utf8')
    return output
  return inner

TEMPLATE_OPTIONS = {}
BASE_URL = ""


class Webtastic(object):
  """ Class doc """
  
  def __init__ (self):
    """ Class initialiser """
    # Get singleton instance
    PluginManagerSingleton.setBehaviour([
        VersionedPluginManager,
    ])
    manager = PluginManagerSingleton.get()
    
    # A referrence for plugins to access the app
    manager.app = self
    
    # Set environment
    self.env = jinja2.Environment(loader=jinja2.FileSystemLoader("./template/"),
                                  **TEMPLATE_OPTIONS)
    
    # Set ArgParser
    self.parser = argparse.ArgumentParser(description='Simple Static Web Generator')
    
    # A referrence for plugins to access the env object
    # manager.env = self.env
    
    # Set plugin's directories path
    manager.setPluginPlaces(['plugins'])
    
    # Locates and Loads the plugins
    manager.collectPlugins()
  
  def write_file (self, path, content):
    """ Function doc """
    f = open(path, 'w')
    # TODO: return by Exceptions
    f.write(content.encode('utf8'))
    f.close()
    return True
  
  def copy_tree(self, src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise
  
  def run (self):
    """ Function doc """
    # Activating all the plugins
    manager = PluginManagerSingleton.get()
    for plugin in manager.getAllPlugins():
      plugin.plugin_object.activate()
    
    # Get Arguments
    self.args = vars(self.parser.parse_args())
    
    # OUTPUT and 
    base_url = self.args['base_url']
    OUTPUT_DIR = os.path.join(os.path.abspath('html'), base_url)
    TEMPLATE_DIR = os.path.abspath('template')
    
    # Create SourceTree object from source directory
    self.sources = WebtasticSourceTree('source')
    
    # remove OUTPUT directory
    # os.system("rm -r html/")
    # Create OUTPUT directory
    os.system("mkdir -p %s" % (OUTPUT_DIR))
    # Copy TEMPLATE's content directories/files into OUTPUT directory
    # TODO: exclude partials and layout
    os.system("cp -r %s/* %s" % (TEMPLATE_DIR, OUTPUT_DIR))
    # Create Directory for every subdirectory exists in source directory
    for directory in self.sources.directories('source/'):
      directory = re.sub(r"^([^/]+)", OUTPUT_DIR, directory)
      os.system("mkdir -p %s" % directory)
    # Copy every not_source files to relative location at OUTPUT directory
    for rel_file in self.sources.rel_file_paths('source/'):
      src = rel_file
      dst = re.sub(r"^([^/]+)", OUTPUT_DIR, rel_file)
      os.system("cp %s %s" % (src, dst))
    # read every source file and compile it into OUTPUT directory
    for src_file in self.sources.src_files():
      print 'html' + src_file.link
      self.src_file = src_file
      
      # TODO: plugin's BEFORE_LOAD_TEMPLATE
      # TODO: set default layout
      try:
        # check if layout exists
        # FIXME: there should be a better way to do this you Silly.
        template = self.env.get_template(self.src_file.layout)
      except TemplateNotFound as e:
        template = self.env.get_template('%s.html' % self.src_file.layout)
      # TODO: plugin's AFTER_LOAD_TEMPLATE
      
      # TODO: add output variable
      output_file = os.path.join('html/', self.src_file.link[1:])
      
      # TODO: plugin's BEFORE_TEMPLATE_RENDER
      output_content = template.render(page=self.src_file, source=self.sources)
      output_content = re.sub("$BASE_URL", "html/", output_content)
      # TODO: plugin's AFTER_TEMPLATE_RENDER
      
      # TODO: plugin's BEFORE_WRITE_OUTPUT
      self.write_file(output_file, output_content)
      # TODO: plugin's AFTER_WRITE_OUTPUT
    
    f = open('template/style.css')
    stylesheet = f.read()
    f.close()
    base_url = self.args['base_url']
    if len(base_url) > 0 and not base_url.startswith("/"):
      base_url = '/' + base_url
    compile_stylesheet = re.sub("\$BASE_URL", base_url, stylesheet)
    f = open('%s/style.css' % 'html', 'w')
    f.write(compile_stylesheet)
    f.close()
    
    # Deactivating the plugins
    for plugin in manager.getAllPlugins():
      plugin.plugin_object.deactivate()


class WebtasticSourceTree(object):
  """ Class doc """
  # path = None
  tree = {}
  hash_tree = {}
  __files__ = []
  
  def __init__ (self, path):
    """ Class initialiser """
    # TODO: ValueError check
    # FIXME: is self needed?
    self.path = path
    
    for dirname, dirnames, filenames in os.walk(self.path):
      for filename in filenames:
        filepath = os.path.join(dirname, filename)
        self.__files__.append(filepath)
  
  def file_paths (self, path='', recursive=True):
    """ Function doc """
    filtered = []
    for f in self.__files__:
      if not recursive:
        regex_search = "(%s[^/]+$)" % path
      else:
        regex_search = "(%s.*)" % path
      matched = re.search(regex_search, f)
      if matched:
        filtered.append(matched.group())
    return filtered
  
  def src_file_paths (self, path='', recursive=True):
    """ Function doc """
    filtered = []
    for f in self.file_paths(path, recursive):
      if re.search(".md$", f):
        filtered.append(f)
    return filtered
  
  def rel_file_paths (self, path='', recursive=True):
    """ Function doc """
    filtered = []
    for f in self.file_paths(path, recursive):
      if not re.search(".md$", f):
        filtered.append(f)
    return filtered
  
  def directories (self, path='', recursive=True):
    """ Function doc """
    filtered = []
    for f in self.file_paths(path, recursive):
      directory = re.sub(r"([^/])+$", "", f)
      if directory not in filtered:
        filtered.append(directory)
    return filtered
  
  def src_files (self, path='', recursive=True):
    """ Function doc """
    res = []
    for file_path in self.src_file_paths(path, recursive):
      f = WebtasticSourceFile(file_path)
      res.append(f)
    return res


class WebtasticSourceFile(object):
  """ Class doc """
  __attributes__ = None
  __content__ = None
  
  def __init__ (self, path):
    """ Class initialiser """
    # TODO: add ERROR handlers for bad path
    self.path = path
    
    f = open(path)
    self.raw_data =f.read()
    f.close()
    try:
      # FIXME: possible only yaml content is broken
      raw_attr, raw_content = self.raw_data.split("-"*10)[1:]
      self.__attributes__ = yaml.load(raw_attr)
      self.__content__ = raw_content
    except Exception as e:
      # TODO: Raise an Exception
      print "ERROR HAPPENDED ", e.message
      pass
  
  def __getattr__ (self, key):
    """ Function doc """
    return self.__attributes__.get(key, None)
  
  @property
  @utf8
  def content (self):
    """ Function doc """
    if self.__content__:
      return self.__content__
  
  @property
  def basename (self):
    """ Function doc """
    return os.path.split(self.path)[1][:-3]
  
  @property
  def filename (self):
    """ Function doc """
    return os.path.split(self.path)[1]
  
  @property
  def name (self):
    """ Function doc """
    return os.path.split(self.path)[1]
  
  @property
  def link (self):
    """ Function doc """
    # remove `source` from the path
    if self.output is not None:
      return self.output
    else:
      root_directory = self.path.split("/")[0]
      return self.path.replace(root_directory, '').replace('.md', '.html')
  
  @property
  def ctime (self):
    """ Function doc """
    return int(os.path.getctime(self.path))
  
  @property
  def mtime (self):
    """ Function doc """
    return int(os.path.getmtime(self.path))
  
  @property
  def atime (self):
    """ Function doc """
    return int(os.path.getatime(self.path))


if __name__ == '__main__':
  logging.basicConfig(level=logging.DEBUG)
  app = Webtastic()
  app.run()
