#!/usr/bin/env python

from banking import Transaction
import argparse
import json
import importlib

from banking import Login

p = argparse.ArgumentParser(description='Get some datums.')

p.add_argument('service', type=str, help='where to get it')
p.add_argument('-u')
p.add_argument('-p')

args = p.parse_args()

try:
  import passwords
  login = passwords.logins[args.service]

except:
  if not (args.user and args.password):
    import sys
    sys.stderr.write('passwords.py or (-u and -p args) are required')
    sys.exit(1)

  login = Login(args.user, args.password)

lib = importlib.import_module(args.service)

out = {}

a = lib.Site()
a.login(login)

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

