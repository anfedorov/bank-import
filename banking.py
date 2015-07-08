from collections import namedtuple

from chrome import Site

# todo - turn this into a class and allow to pull down details
Transaction = namedtuple('Transaction', ['date', 'description', 'amount'])

# todo - make into a class which can pull out all transactions
Period = namedtuple('TranscationPeriod', ['start', 'end'])

class BankingSite(Site):
  def login(self, login_info):
    raise NotImplementedError()

  @property
  def transactions(self, period):
    raise NotImplementedError()
