from bs4 import BeautifulSoup

import requests
import json

def getDescriptionProduct(bs):
  try:
    title = bs.h1.get_text()
  except AttributeError as err:
    print(f"[DESCRIPTION PRODUCT ERROR] Error: {err}")
    return None
  return title

def getPrice(bs):
  try:
    price = 'R$ ' + bs.find(
      'span',
      { 'class': 'price-template__text' }
    ).get_text()
  except AttributeError as err:
    print(f"[PRICE ERROR] Error: {err}")
    return None
  return price

def getImage(bs):
  try:
    image = bs.find(
      'img',
      { 'class': 'showcase-product__big-img' }
    )['src']
  except AttributeError as err:
    print(f"[IMAGE ERROR] Error: {err}")
    return None
  return image

def getMarketplaceCreditCard(bs):
  try:
    general_credit_card = {}

    ul = bs.find('ul',{ 'class': 'method-payment__values--left'})
    children = ul.findChildren('li', recursive=False)

    for child in children:
      info = child.li.p.get_text().split()

      if 'R$' in info[0]:
        general_credit_card['1x sem juros'] = ''.join(info[0:2])
      else:
        if 'sem' in info:
          general_credit_card[f"{info[0]} sem juros"] = ''.join(info[1:3])
        else:
          general_credit_card[f"{info[0]} com juros"] = ''.join(info[1:3])

    return general_credit_card
  except AttributeError as err:
    print(f"[MARKETPLACE CREDIT CARD ERROR] Error: {err}")
    return None

def getGeneralCreditCard(bs):
  try:
    general_credit_card = {}

    ul = bs.find('ul',{ 'class': 'method-payment__values--general-cards'})
    children = ul.findChildren('li', recursive=False)

    for child in children:
      info = child.li.p.get_text().split()

      if 'R$' in info[0]:
        general_credit_card['1x sem juros'] = ''.join(info[0:2])
      else:
        if 'sem' in info:
          general_credit_card[f"{info[0]} sem juros"] = ''.join(info[1:3])
        else:
          general_credit_card[f"{info[0]} com juros"] = ''.join(info[1:3])

    return general_credit_card
  except AttributeError as err:
    print(f"[CREDIT CARD ERROR] Error: {err}")
    return None

def getSeller(bs):
  try:
    seller = bs.find('button', { 'class': 'seller-info-button' }).get_text().strip()
  except AttributeError:
    seller = 'Magazine Luiza'
  return seller

def getDiscount(bs):
  try:
    disc = bs.find('span', { 'class': 'price-template__discount-text'}).get_text()

    percentage = disc.split()[0].replace('(', '')
    criterion = 'Boleto bancário ou 1x no cartão de crédito.'

    return percentage, criterion
  except:
    return None, None

def parse(url, marketplace):
  try:
    html = requests.get(url)
    html.raise_for_status()

    # with open('tmp.html', 'w') as file:
    #   file.write(html.text)

    bs = BeautifulSoup(html.text, 'html.parser')
  
    description_product = getDescriptionProduct(bs)
    if description_product is None:
      description_product_error = {
        'error': 'Description Product could not be a found.'
      }
      return json.dumps(description_product_error, indent = 2)
    
    price = getPrice(bs)
    if price is None:
      price_error = {
        'error': 'Price could not be a found.'
      }
      return json.dumps(price_error, indent = 2)

    seller = getSeller(bs)
    if seller is None:
      seller_error = {
        'error': 'Seller could not be a found.'
      }
      return json.dumps(seller_error, indent = 2)

    picture_url = getImage(bs)
    if picture_url is None:
      picture_error = {
        'error': 'Picture URL could not be a found.'
      }
      return json.dumps(picture_error, indent = 2)

    general_credit_card = getGeneralCreditCard(bs)
    if general_credit_card is None:
      general_credit_card_error = {
        'error': 'General Credit Card could not be a found.'
      }
      return json.dumps(general_credit_card_error, indent = 2)

    marketplace_credit_card = getMarketplaceCreditCard(bs)
    if marketplace_credit_card is None:
      marketplace_credit_card_error = {
        'error': 'Marketplace Credit Card could not be a found.'
      }
      return json.dumps(marketplace_credit_card_error, indent = 2)

    discount_percentage, discount_criterion = getDiscount(bs)
    if discount_percentage is None or discount_criterion is None:
      discount_percentage, discount_criterion = '', ''

    result = {
      "description_product": description_product,
      "price": price,
      "picture_url": picture_url,
      "seller": seller,
      "discount_percentage": discount_percentage,
      "discount_criterion": discount_criterion,
      "general_credit_card": general_credit_card,
      "marketplace_credit_card": marketplace_credit_card,
      "marketplace": marketplace,
    }

    return json.dumps(result, indent = 2)

  except requests.exceptions.HTTPError as err:
    raise SystemExit(err)

  except Exception as err:
    print(f"[PRODUCT MAIN ERROR] Error: {err}")

