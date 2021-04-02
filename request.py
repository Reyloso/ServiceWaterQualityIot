# -*- coding: utf-8 -*
import requests
from requests.exceptions import HTTPError


def get_data(url, *args, **kwargs):
   """ method to get data from a route """
   try:
      headers = kwargs.get('headers')
      if headers:
        response = requests.get(
            url,
            headers=headers,
            body=body,
        )
      else:
         response = requests.get(url, body)

      response.raise_for_status()
   except HTTPError as http_err:
      print(f'HTTP error occurred: {http_err}')
   except Exception as err:
      print(f'Other error occurred: {err}')
   else:
      return response.json()


def post_data(url, *args, **kwargs):
    try:
        headers = kwargs.get('headers')
        body = kwargs.get('body')
        if headers:
            response = requests.post(
                url,
                headers=headers,
                data=body,
            )
        else:
            response = requests.post(url, data=body)

        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        return response.json()