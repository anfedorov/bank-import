import chrome

from passwords import logins
login_data = logins['capitalone']

b = chrome.Browser()
b.get('https://www.capitalone.com/')

t = b.tabs[0]
bt = t.find_button('Select an account type')
if bt is not None:
  bt.click()
  t.find_el_xp('//*/label[@for="rbCreditCards"]').click()

t.find_input('us-credit-cards-uid').fill(login_data.user)
t.find_input('us-credit-cards-pw').fill(login_data.pswd)
t.find_input('cbCardRemember').check()
t.find_input('submit-card-us').click()

t.find_link('Transactions').click()

f = t.browser.driver.find_elements_by_xpath
pend = '//*[@id="postedTransactionTable"]/div[@role="row"]/div'

dates = [x.text for x in f(pend + '/div[1]/span')]
names = [x.text for x in f(pend + '/div/div')]
txtype = [x.text for x in f(pend + '/div[3]')]
amnt = [float(x.text.replace('$', '').replace(',', '')) for x in f(pend + '[2]')]

print zip(dates, names, txtype, amnt)


# from dateutil import parser

# from banking import Period

# rs = [x.text for x in f('//*/select[@id="StatementPeriodQuick"]/option')]
# bounds = sorted(
#   [parser.parse(r[16:]) for r in rs if r.startswith('Statement Ending')],
#   reverse=True
# )
# periods = [Period(start, end) for start, end in zip(bounds + [None], [None] + bounds)]
