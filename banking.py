from collections import namedtuple

from chrome import Site

Login = namedtuple('Login', ['user', 'pswd'])

# todo - turn this into a class and allow to pull down details
Transaction = namedtuple('Transaction', ['date', 'payee', 'description', 'amount', 'posted',])

# todo - make into a class which can pull out all transactions
Period = namedtuple('TranscationPeriod', ['start', 'end'])



class BankingSite(Site):
  def login(self, login_info):
    raise NotImplementedError()
