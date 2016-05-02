# bambu
CLI driven schedulable data harvester to feed data to ePANDDA Search API

#### taxa_by_ref.py
Get aggregate list of taxon names associated with publication

Output:

```javascript
Ref ID: 25746
[
  {'acc': '', 'acr': '', 'acn': '', 'rtp': 'O', 'tid': 'txn:81899', 'tdf': 'recombined as', 'rank': 3, 'name': 'Balaena glacialis'},
  {'acc': '', 'acr': '', 'acn': '', 'rtp': 'O', 'tid': 'txn:64683', 'tdf': '', 'rank': 3, 'name': 'Balaena mysticetus'},
  {'acc': '', 'acr': '', 'acn': '', 'rtp': 'O', 'tid': 'txn:68469', 'tdf': '', 'rank': 3, 'name': 'Balaenoptera acutorostrata'}, 
  {'acc': '', 'acr': '', 'acn': '', 'rtp': 'O', 'tid': 'txn:64491', 'tdf': '', 'rank': 3, 'name': 'Megaptera novaeangliae'},
  {'acc': '', 'acr': '', 'acn': '', 'rtp': 'O', 'tid': 'txn:36676', 'tdf': '', 'rank': 5, 'name': 'Balaena'},
  {'acc': '', 'acr': '', 'acn': '', 'rtp': 'O', 'tid': 'txn:36652', 'tdf': '', 'rank': 13, 'name': 'Cetacea'}
]
```
