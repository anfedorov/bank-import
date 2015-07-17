# from dateutil import parser

from dateutil import parser

import utils
from banking import BankingSite, Transaction


class Site(BankingSite):
  def __init__(self):
    BankingSite.__init__(self, 'https://www.capitalone.com')

  def login(self, login_data):
    bt = None
    while bt is None:
      bt = self.t.find_button('Select an account type')
    bt.click()
    self.t.find_el_xp('//*/label[@for="rbCreditCards"]').click()

    self.t.find_input('us-credit-cards-uid').fill(login_data.user)
    self.t.find_input('us-credit-cards-pw').fill(login_data.pswd)
    self.t.find_input('cbCardRemember').check()
    self.t.find_input('submit-card-us').click()

  @property
  def balance(self):
    xp = '//span[@id="current-balance-amount"]'
    return utils.parse_dols(self.t.find_el_xp(xp).text)

  def get_transactions(self, pending=False):
    f = self.t.browser.driver.find_elements_by_xpath

    if pending:
      el = self.t.find_el_xp('//span[contains(text(), "Pending Transactions")]')
      if el.text == 'View Pending Transactions':
        el.click()

      dates_xp = '//*[@id="pendingTransactionTable"]//div[contains(@class, "date")]'
      names_xp = '//*[@id="pendingTransactionTable"]//div[contains(@class, "merchant")]'
      amnts_xp = '//*[@id="pendingTransactionTable"]//div[contains(@class, "amount")]'

    else:
      dates_xp = '//*[@id="postedTransactionTable"]//div[contains(@class, "date")]/span'
      names_xp = '//*[@id="postedTransactionTable"]//div[contains(@class, "merchant")]'
      amnts_xp = '//*[@id="postedTransactionTable"]//div[contains(@class, "amount")]'

    amounts = [None]
    while amounts and any(a == None for a in amounts):
      dates = [parser.parse(x.text).isoformat() for x in f(dates_xp)]
      names = [x.text for x in f(names_xp)]
      # txtype = [x.text for x in f(pend + '/div[3]')]
      amounts = [utils.parse_dols(x.text) for x in f(amnts_xp)]

    return [
      Transaction(tdate, desc, '', amt, not pending,)
        for tdate, desc, amt in zip(dates, names, amounts)
    ]

  def goto(self, page):
    if page == 'statements':
      self.t.find_link('Transactions').click()
