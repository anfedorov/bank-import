import chrome

from passwords import logins
login_data = logins['chase']

b = chrome.Browser()
b.get('https://www.chase.com/')

t = b.tabs[0]
t.find_input('usr_name').fill(login_data.user)
t.find_input('usr_password').fill(login_data.pswd)
t.find_input('remember').check()
t.find_link('Log In to').click()

t.find_link('See activity').click()

f = t.browser.driver.find_elements_by_xpath
pend = '//*[@id="Posted"]/table[contains(@class, "card-activity")]/tbody/tr/'

tdates = [x.text for x in f(pend + '/td[2]')]
pdates = [x.text for x in f(pend + '/td[3]')]
types = [x.text for x in f(pend + '/td[4]')]
descs = [x.text for x in f(pend + '/td[5]')]
amounts = [float(x.text.replace('$', '').replace(',', '')) for x in f(pend + '/td[7]')]

print zip(tdates, pdates, types, descs, amounts)


# from dateutil import parser

# from banking import Period

# rs = [x.text for x in f('//*/select[@id="StatementPeriodQuick"]/option')]
# bounds = sorted(
#   [parser.parse(r[16:]) for r in rs if r.startswith('Statement Ending')],
#   reverse=True
# )
# periods = [Period(start, end) for start, end in zip(bounds + [None], [None] + bounds)]
