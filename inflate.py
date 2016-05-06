# Data inflation
#
# @author: jlauters
#
# provide mechanism to inflate keys to full length from PBDB and allow for expansion of compressed or semi-compressed objects

# inflate PBDB Publication
def inflatePub( publication ):

  inflated = {
    'object_id': '',
    'record_type': '',
    'ref_type': '',
    'associated_records': '',
    'reference': '',
    'first_auth_int': '',
    'first_auth_last': '',
    'second_auth_int': '',
    'second_auth_last': '',
    'other_authors': '',
    'published_year': '',
    'document_title': '',
    'value_title': '',
    'editors': '',
    'volume': '',
    'series_num': '',
    'first_page_num': '',
    'last_page_num': '',
    'value_type': '',
    'language': '',
    'doi': '',
    'comments': '',
    'auth_num': '',
    'enterer': '',
    'modifier': '',
    'date_created': '',
    'date_modified': ''
  }

  for key in publication.iterkeys():

    value = publication[key]

    if 'oid' == key:
      inflated['object_id'] = value
    if 'typ' == key:
      inflated['record_type'] = value
    if 'rtp' == key:
      inflated['ref_type'] = value
    if 'rct' == key:
      inflated['associated_records'] = value
    if 'ref' == key:
      inflated['reference'] = value
    if 'ai1' == key:
      inflated['first_auth_int'] = value
    if 'al1' == key:
      inflated['first_auth_last'] = value
    if 'ai2' == key:
      inflated['second_author_int'] = value
    if 'al2' == key:
      inflated['second_author_last'] = value
    if 'oau' == key:
      inflated['other_authors'] = value
    if 'pby' == key:
      inflated['published_year'] = value
    if 'tit' == key:
      inflated['document_title'] = value
    if 'pbt' == key:
      inflated['value_title'] = value
    if 'eds' == key:
      inflated['editors'] = value
    if 'vol' == key:
      inflated['volume'] = value
    if 'num' == key:
      inflated['series_num'] = value
    if 'pgf' == key:
      inflated['first_page_num'] = value
    if 'pgl' == key:
      inflated['last_page_num'] = value
    if 'pty' == key:
      inflated['value_type'] = value
    if 'lng' == key:   
      inflated['language'] = value 
    if 'doi' == key:
      inflated['doi'] = value
    if 'cmt' == key:
      inflated['comments'] = value
    if 'ati' == key:
      inflated['auth_num'] = value
    if 'eni' == key:
      inflated['enterer_num'] = value
    if 'mdi' == key:
      inflated['modifier_num'] = value
    if 'ath' == key:
      inflated['authorizer'] = value
    if 'ent' == key:
      inflated['enterer'] = value
    if 'mdf' == key:
      inflated['modifier'] = value
    if 'dcr' == key:
      inflated['date_created'] = value
    if 'dmd' == key:
      inflated['date_modified'] = value

  return inflated
