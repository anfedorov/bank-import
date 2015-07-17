#!/usr/bin/env python

from banking import Transaction
import argparse
import json
import importlib

import utils
from banking import Login

p = argparse.ArgumentParser(description='Get some datums.')

p.add_argument('service', type=str, help='where to get it')
p.add_argument('-u')
p.add_argument('-p')
p.add_argument('-s', action='store_true')


args = p.parse_args()
utils.SCREEN = args.s

try:
  import passwords
  login = passwords.logins[args.service]

except:
  if not (args.u and args.p):
    import sys
    sys.stderr.write('passwords.py or (-u and -p args) are required')
    sys.exit(1)

  login = Login(args.u, args.p)

lib = importlib.import_module(args.service)

out = {}

with lib.Site() as a:
  utils.take_screenshot('site-loaded')

  a.login(login)

  utils.take_screenshot('login-done')
  a.goto('statements')

  out['balance'] = a.balance

  out['pending'] = [
    dict(zip(Transaction._fields, tx))
      for tx in a.get_transactions(pending=True)
  ]

  out['posted'] = [
    dict(zip(Transaction._fields, tx))
      for tx in a.get_transactions(pending=False)
  ]

  print json.dumps(out, indent=2)

