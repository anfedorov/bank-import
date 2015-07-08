from dateutil import parser

import chrome

from passwords import logins
login_data = logins['splitwise']

b = chrome.Browser()
b.get('https://secure.splitwise.com/login')

t = b.tabs[0]
t.find_input('user_session[email]').fill(login_data.user)
t.find_input('user_session[password]').fill(login_data.pswd)
t.find_input('commit').click()  # log in button

f = t.browser.driver.find_elements_by_xpath
pend = '//*[contains(@class, "expense") and div/span[contains(@class, "negative") or contains(@class, "positive")]]'

res = []

for x in f(pend):
  dt = parser.parse(x.get_attribute('data-date'))
  desc = x.find_element_by_tag_name('a').text

  xp_amnt = './/span[contains(@class, "negative") or contains(@class, "positive")]'
  a = x.find_element_by_xpath(xp_amnt)
  amount = (-1 if 'negative' in a.get_attribute('class') else 1) * float(a.text.strip('$'))
  print dt, desc, amount

# from dateutil import parser

# from banking import Period

# rs = [x.text for x in f('//*/select[@id="StatementPeriodQuick"]/option')]
# bounds = sorted(
#   [parser.parse(r[16:]) for r in rs if r.startswith('Statement Ending')],
#   reverse=True
# )
# periods = [Period(start, end) for start, end in zip(bounds + [None], [None] + bounds)]
