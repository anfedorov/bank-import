# from dateutil import parser

import utils
from banking import BankingSite, Transaction


class Site(BankingSite):
  def __init__(self):
    BankingSite.__init__(self, 'https://www.chase.com')

  def login(self, login_data):
    self.t.find_input('usr_name').fill(login_data.user)
    self.t.find_input('usr_password').fill(login_data.pswd)
    self.t.find_input('remember').check()
    self.t.find_link('Log In to').click()

  @property
  def balance(self):
    xp = '//td[contains(text(), "Current balance")]/following-sibling::td'
    return utils.parse_dols(self.t.find_el_xp(xp).text)

  def get_transactions(self, pending=False):
    f = self.t.browser.driver.find_elements_by_xpath

    tbl = 'Pending' if pending else 'Posted'

    pend = '//*[@id="%s"]/table[contains(@class, "card-activity")]/tbody/tr/' % tbl

    tdates = [x.text for x in f(pend + '/td[2]')]
    # pdates = [x.text for x in f(pend + '/td[3]')]
    # types = [x.text for x in f(pend + '/td[4]')]
    descs = [x.text for x in f(pend + '/td[5]')]
    amounts = [utils.parse_dols(x.text) for x in f(pend + '/td[7]')]

    return [
      Transaction(tdate, desc, '', amount, not pending,)
        for tdate, desc, amount in zip(tdates, descs, amounts)
    ]

  def goto(self, page):
    if page == 'statements':
      self.t.find_link('See activity').click()
