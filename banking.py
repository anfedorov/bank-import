from collections import namedtuple

from chrome import Site, Browser

Login = namedtuple('Login', ['user', 'pswd'])

# todo - turn this into a class and allow to pull down details
Transaction = namedtuple('Transaction', ['date', 'payee', 'description', 'amount', 'posted',])

# todo - make into a class which can pull out all transactions
Period = namedtuple('TranscationPeriod', ['start', 'end'])



class BankingSite(Site):
  def __init__(self, url):
    self.url = url

  def __enter__(self):
    self.b = Browser()
    self.b.get(self.url)
    self.t = self.b.tabs[0]
    return self

  def __exit__(self, type, value, traceback):
    self.b.close()

  def login(self, login_info):
    raise NotImplementedError()
