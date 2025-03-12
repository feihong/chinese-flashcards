"""
List cards that are due more than 30 days from now, whose last review lasted less than 0.4 seconds.
"""
import itertools
import requests

def invoke(action, **params):
  data = {'action': action, 'version': 6}
  if params:
    data['params'] = params
  r = requests.post('http://127.0.0.1:8765', json=data)
  return r.json()

def get_cards():
  card_ids = invoke('findCards', query='note:Chinese prop:due>30')['result']
  print(f'Found {len(card_ids)} Chinese cards due more than 30 days from now')
  return card_ids

def get_card_reviews(card_ids) -> dict:
  reviews = invoke('getReviewsOfCards', cards=card_ids)['result']

  for key in list(reviews.keys()):
    review = reviews[key][-1] # only look at latest review
    if review['time'] > 400:
      # ignore if review duration was more than 0.4 seconds
      del reviews[key]
    else:
      reviews[key] = review

  return reviews

card_ids = get_cards()
reviews = get_card_reviews(card_ids)

sorted_reviews = list((k, v['time']) for k, v in reviews.items())
sorted_reviews.sort(key=lambda t: t[1])

for batch in itertools.batched(sorted_reviews, n=10):
  print(f'({batch[0][1]} ms)', 'cid:' + ','.join(t[0] for t in batch))

print(f'\nThere are {len(reviews)} sloppily-reviewed cards')
