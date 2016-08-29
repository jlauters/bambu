# Bambu Utils

import string
import re

def init_fields(specimen):
  ret = {}

  ret['sciNameAuth'] = ""
  ret['sciNameAuthDate'] = ""
  ret['specificEpithet'] = ""
  ret['identRemarks'] = ""
  ret['biblioCitation'] = ""
  ret['occurrenceRemark'] = ""
  ret['associatedRef'] = ""
  ret['identBy'] = ""
  ret['identRef'] = ""
  ret['recordedBy'] = ""
  ret['eventDate'] = ""
  ret['dateIdentified'] = ""
  ret['scientificName'] = ""
  ret['order'] = ""
  ret['stateProvince'] = ""
  ret['locality'] = ""
  ret['formation'] = ""

  if "dwc:scientificNameAuthorship" in specimen:
    ret['sciNameAuth'] = specimen["dwc:scientificNameAuthorship"].lower()
  
    if ' ' in ret['sciNameAuth']:
      sciNameParts = ret['sciNameAuth'].split()
      ret['sciNameAuth']     = sciNameParts[0]
      ret['sciNameAuthDate'] = sciNameParts[1]

  if "dwc:identificationRemarks" in specimen:
    ret['identRemarks'] = specimen["dwc:identificationRemarks"].lower()

  if "dcterms:bibliographicCitation" in specimen:
    ret['biblioCitation'] = specimen["dcterms:bibliographicCitation"].lower()

  if "dwc:occurrenceRemarks" in specimen:
    ret['occurrenceRemark'] = specimen["dwc:occurrenceRemarks"].lower()

  if "dwc:associatedReferences" in specimen:
    ret['associatedRef'] = specimen["dwc:associatedReferences"].lower()

  if "dwc:specificEpithet" in specimen:
    ret['specificEpithet'] = specimen["dwc:specificEpithet"].lower()

  if "dwc:identificationReferences" in specimen:
    ret['identRef'] = specimen["dwc:identificationReferences"].lower()

  if "dwc:recordedBy" in specimen:
    cleaned = specimen["dwc:recordedBy"].lower().split(',')
    ret['recordedBy'] = cleaned[0]

  if "dwc:identifiedBy" in specimen:
    cleaned = specimen["dwc:identifiedBy"].lower().split(',')
    ret['identBy'] = cleaned[0]

  if "dwc:eventDate" in specimen:
    ret['eventDate'] = specimen["dwc:eventDate"].lower()

  if "dwc:dateIdentified" in specimen:
    ret['dateIdentified'] = specimen["dwc:dateIdentified"].lower()

  if "dwc:scientificName" in specimen:
    ret['scientificName'] = specimen["dwc:scientificName"].lower()

  if "dwc:order" in specimen:
    ret['order'] = specimen["dwc:order"].lower()

  if "dwc:stateProvince" in specimen:
    ret['stateProvince'] = specimen["dwc:stateProvince"].lower()

  if "dwc:localtiy" in specimen:
    ret['locality'] = specimen["dwc:locality"].lower()

  if "dwc:formation" in specimen:
    ret['formation'] = specimen["dwc:formation"].lower()

  return ret

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
