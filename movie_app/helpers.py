import os
import requests
import retrying
from dotenv import load_dotenv
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import RefreshToken

load_dotenv()


class ThirdPartyAPIException(APIException):
    status_code = 400
    default_detail = 'An error occurred during the request.'


def raise_for_status(self):
    if self.status_code != 200:
        raise ThirdPartyAPIException()


@retrying.retry(wait_fixed=1000, stop_max_attempt_number=3)
def third_party_movie_list():
    '''
    this function will retry 3 times untill it gets 200 status response
    otherwise it will raise exception
    '''
    url = os.environ.get('MOVIE_API_URL')
    response = requests.get(url, auth=(os.environ.get(
        'MOVIE_API_USERNAME'), os.environ.get('MOVIE_API_PASSWORD')))
    raise_for_status(response)
    return response.json()


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def top_generes(collections):
    genere_count = {}
    user_generes = []
    for collection in collections:
        for movie in collection.movies.all():
            user_generes.append(movie.genere)
    for genere in user_generes:
        if genere in genere_count:
            genere_count[genere] += 1
        else:
            genere_count[genere] = 1

    top_3_genere = sorted(
        genere_count, key=lambda x: genere_count[x], reverse=True)[:3]
    return top_3_genere
