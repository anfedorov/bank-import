tsv = lambda xs: '\t'.join(map(str, xs))

def parse_dols(s):
  try:
    return float(s.replace('$', '').replace(',', ''))
  except:
    return None


def run_bash(s):
  import subprocess
  subprocess.Popen(s.split(), stdout=subprocess.PIPE, shell=True)
  # process = subprocess.Popen(s.split(), stdout=subprocess.PIPE, shell=True)
  return

SCREEN = False
def take_screenshot(label, save_path='/tmp/shots'):
  if SCREEN:
    from datetime import datetime
    fname = 'screenshot-%s-%s.jpg' % (datetime.now().isoformat(), label)
    path = '%s/%s' % (save_path, fname)
    return run_bash('xwd -root -silent | xwdtopnm | pnmtojpeg > %s' % path)
