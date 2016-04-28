# Bambu Utils

import string

def normalize(s):
  for p in string.punctuation:
    if "-" == p:
      s = s.replace(p, ' ')
    else:
      s = s.replace(p, '')

  return s.lower().strip()

def scanPage(ocr):
  stripped = ""

  if ocr is not None:
    stripped = repr( ocr.strip() )
    stripped = re.sub(ur"\\n", "", stripped)

  return stripped
