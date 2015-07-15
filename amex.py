from dateutil import parser

import chrome
import utils
from banking import BankingSite


class AmexSite(BankingSite):
  def __init__(self):
    self.b = chrome.Browser()
    self.b.get('https://www.americanexpress.com/')
    self.t = self.b.tabs[0]

  def login(self, login):
    # add check if already logged in
    self.t.find_input('UserID').fill(login.user)
    self.t.find_input('Password').fill(login.pswd)
    self.t.find_input('REMEMBERME').check()
    self.t.find_link('Log In').click()

  @property
  def page(self):
    if self.b.driver.title.endswith('Online Statement'):
      return Statements(self.t)
    else:
      return None

  def goto(self, page):
    if page == 'statements':
      self.t.find_link('Statements & Activity').click()


class Page(object):
  # todo - method for reading table into list of dicts
  def __init__(self, t):
    self.t = t


class Statements(Page):
  def __repr__(self):
    return '<Statements>'

  @property
  def available_periods(self):
    from banking import Period
    b = self.t.find_button('Recent Activity')
    b.click()
    ps = self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "periodListDescription")]')

    ret = [[False]]
    while not all(all(x) for x in ret):
      ret = [p.text.split(' to ') for p in ps]

    for i, x in enumerate(ret):
      start = None
      end = None
      if len(x) == 1:
        if x[0].lower().startswith('period ending '):
          end = parser.parse(x[14:])
        else:
          print "I don't even '%s'" % x[0]

      elif len(x) == 2:
        start, end = x
        start = parser.parse(start)
        if end == 'Present':
          end = None
        else:
          end = parser.parse(end)

      else:
        print "I don't even '%s'" % x

      ret[i] = Period(start, end)

    b.click()
    return ret

  def get_transactions(self, pending=False):
    from banking import Transaction

    if pending:
      self.t.find_button('Pending Charges').click()
    else:
      self.t.find_button('Posted Transactions').click()

    dates = [parser.parse(' '.join([x.text for x in xs])).isoformat() for xs in zip(
      self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "estmt-date")]'),
      self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "estmt-month")]'),
      self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "estmt-year")]')
    )]

    descs = [x.text for x in
      self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "desc-trans")]')
    ]

    amounts = [utils.parse_dols(x.text) for x in
      self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "colAmount")]')
    ]

    return [
      Transaction(dt, desc, '', amt, not pending)
        for dt, desc, amt in zip(dates, descs, amounts)
          if amt > 0
    ]


if __name__ == '__main__':
  import argparse

  p = argparse.ArgumentParser(description='Get some datums.')

  p.add_argument('action', type=str, help='what do we do')

  # p.add_argument('--latest-tx', dest='latest_tx',
  #                               action='store_true',
  #                               default=False,
  #                               help='quick import')

  args = p.parse_args()

  if args.action == 'get-latest':
    import passwords
    import json
    from banking import Transaction
    a = AmexSite()
    a.login(passwords.logins['amex'])
    a.goto('statements')

    out = {}

    out['pending'] = [
      dict(zip(Transaction._fields, tx))
        for tx in a.page.get_transactions(pending=True)
    ]

    out['posted'] = [
      dict(zip(Transaction._fields, tx))
        for tx in a.page.get_transactions(pending=False)
    ]

    print json.dumps(out, indent=2)

    # print a.page.available_periods
