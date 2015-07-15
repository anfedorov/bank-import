tsv = lambda xs: '\t'.join(map(str, xs))

def parse_dols(s):
  try:
    return float(s.replace('$', '').replace(',', ''))
  except:
    return None

