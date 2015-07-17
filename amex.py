from dateutil import parser

import utils
from banking import BankingSite, Transaction


class Site(BankingSite):
  def __init__(self):
    BankingSite.__init__(self, 'https://www.americanexpress.com/')

  def login(self, login):
    # add check if already logged in
    self.t.find_input('UserID').fill(login.user)
    self.t.find_input('Password').fill(login.pswd)
    self.t.find_input('REMEMBERME').check()
    self.t.find_link('Log In').click()

  @property
  def page(self):
    if self.b.driver.title.endswith('Online Statement'):
      return 'statements'
    else:
      return None

  def goto(self, page):
    if page == 'statements':
      self.t.find_link('Statements & Activity').click()

  @property
  def balance(self):
    xp = '//span[contains(text(), "Outstanding Balance")]/following-sibling::span'
    return utils.parse_dols(self.t.find_el_xp(xp).text)

  def get_transactions(self, pending=False):
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


# class Statements(Page):
#   def __repr__(self):
#     return '<Statements>'

#   @property
#   def available_periods(self):
#     # todo - fix this
#     from banking import Period
#     b = self.t.find_button('Recent Activity')
#     b.click()
#     ps = self.t.browser.driver.find_elements_by_xpath('//*[contains(@class, "periodListDescription")]')

#     ret = [[False]]
#     while not all(all(x) for x in ret):
#       ret = [p.text.split(' to ') for p in ps]

#     for i, x in enumerate(ret):
#       start = None
#       end = None
#       if len(x) == 1:
#         if x[0].lower().startswith('period ending '):
#           end = parser.parse(x[14:])
#         else:
#           print "I don't even '%s'" % x[0]

#       elif len(x) == 2:
#         start, end = x
#         start = parser.parse(start)
#         if end == 'Present':
#           end = None
#         else:
#           end = parser.parse(end)

#       else:
#         print "I don't even '%s'" % x

#       ret[i] = Period(start, end)

#     b.click()
#     return ret
