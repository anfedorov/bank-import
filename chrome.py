import time

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys


class Browser(object):
  Tabs = None

  def __init__(self, url=None, cookies=None):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])

    self.driver = webdriver.Chrome(chrome_options=options)

    if url is not None:
      self.get(url)

    if cookies is not None:
      for c in cookies:
        self.driver.add_cookie(c)

    self.driver.implicitly_wait(30)

  def get_cookies(self):
    return self.driver.get_cookies()

  def switch_to_window(self, wh):
    if self.driver.current_window_handle != wh:
      self.driver.switch_to_window(wh)

  def get(self, url):
    self.driver.get(url)

  def __repr__(self):
    return '<Browser (%s tabs)>' % len(self.tabs)

  def quit(self):
    self.driver.quit()

  @property
  def tabs(self):
    T = self.Tabs or Tab
    return [T(self, window_handle) for window_handle in self.driver.window_handles]


class Tab(object):
  def __init__(self, browser, window_handle):
    self.browser = browser
    self.window_handle = window_handle

  def _switch_tab_temporarily(fn):
    from functools import wraps
    @wraps(fn)
    def wrapped(self, *args, **kwargs):
      wh = self.browser.driver.current_window_handle
      self.browser.switch_to_window(self.window_handle)
      ret = fn(self, *args, **kwargs)
      self.browser.switch_to_window(wh)
      return ret
    return wrapped

  @property
  def title(self):
    return self.browser.driver.title

  def __repr__(self):
    wh = self.browser.driver.current_window_handle
    self.browser.switch_to_window(self.window_handle)
    title = self.title
    wh = self.browser.switch_to_window(wh)
    return '<Tab %s>' % title

  @_switch_tab_temporarily
  def load_page(self, path_or_url):
    if path_or_url.startswith('http'):
      url = path_or_url

    elif self.DOMAIN is not None:
      url = '%s%s' % (self.DOMAIN, path_or_url)

    else:
      print 'domain is %s, path_or_url is %s. wtf?' % (self.DOMAIN, path_or_url)

    self.browser.get(url)

  @staticmethod
  def find_elems(finder, timeout=3):
    start = time.time()
    while True:
      try:
        es = finder()
        if len(es) > 0:
          return es

      except webdriver.remote.errorhandler.ElementNotVisibleException:
        pass

      if time.time() > (start + timeout):
        return []

  def find_el_xp(self, xp):
    return self.browser.driver.find_element_by_xpath(xp)

  def find_elems_xp(self, xp):
    return self.browser.driver.find_elements_by_xpath(xp)

  @_switch_tab_temporarily
  def find_link(self, text, n=0, timeout=3):
    finder = lambda: self.browser.driver.find_elements_by_partial_link_text(text)
    es = self.find_elems(finder, timeout=timeout)
    if len(es) > 1:
      print 'warning: more than one link found with text="%s"' % text
    return es and es[n]

  @_switch_tab_temporarily
  def find_button(self, text, button_type=None, timeout=3):
    xp = '//*/button'
    if button_type is not None:
      xp += '[@type="%s"]' % button_type
    finder = lambda: self.browser.driver.find_elements_by_xpath(xp)
    es = [e for e in self.find_elems(finder, timeout=timeout) if text in e.text]
    if len(es) > 1:
      print 'warning: more than one link found with text="%s"' % text
    return es and es[0]

  @_switch_tab_temporarily
  def find_input(self, name_or_elem):
    if isinstance(name_or_elem, basestring):
      xp = '//*/input[@name="%s"]' % name_or_elem
      es = [e for e in self.browser.driver.find_elements_by_xpath(xp) if e.is_displayed()]
      elem = (es + [None])[0]

    else:
      elem = name_or_elem

    if elem.get_attribute('type') == 'checkbox':
      return Checkbox(self, elem)
    else:
      return Input(self, elem)


class Elem(object):
  def __init__(self, tab, elem):
    self.tab = tab
    self.elem = elem

  def click(self):
    ret = self.elem.click()
    if hasattr(self, 'driver'):
      self.driver.implicitly_wait(30)
    return ret


  def center_position(self):
    raise NotImplemented()


class Input(Elem):
  def __init__(self, tab, elem):
    self.tab = tab
    self.elem = elem

  def __repr__(self):
    return '<Input %s>' % self.elem

  def fill(self, text):
    while 1:
      v = self.elem.get_attribute('value')
      if text == v:
        return
      elif text.startswith(v):
        self.elem.send_keys(text[len(v):][0])
      else:
        self.elem.send_keys(u'\x08')

      # l = len(self.elem.get_attribute('value'))
      # self.elem.send_keys(text[0])
      # chars_added = len(self.elem.get_attribute('value')) - l
      # text = text[chars_added:]



class Checkbox(Input):
  def check(self):
    if not self.checked:
      self.elem.click()

  def uncheck(self):
    if self.checked:
      self.elem.click()

  @property
  def checked(self):
    return self.elem.get_attribute('checked') == 'true'



class Link(Elem):
  def __repr__(self):
    return '<Link %s>' % self.elem

class Button(Elem):
  def __repr__(self):
    return '<Button %s>' % self.elem

class Site(object):
  pass
