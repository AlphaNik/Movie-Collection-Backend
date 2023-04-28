from movie_app.api.permissions import AdminOnly, UserOnly
from movie_app.api.serializers import (MovieCollectionSerializer,
                                       RegistrationSerializer)
from movie_app.helpers import (get_tokens_for_user, third_party_movie_list,
                               top_generes)
from movie_app.models import Movie, MovieCollection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


@api_view(['POST'])
def register_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user_obj = serializer.save()

            tokens = get_tokens_for_user(user_obj)

            # data['tokens'] = {'refresh_token': str(tokens['refresh']),
            #                   'access_token ': str(tokens['access'])}
            # (sending only access token)

            data['access_token'] = str(tokens['access'])
        else:
            data = serializer.errors

        return Response(data, status=status.HTTP_201_CREATED)


@api_view()
@permission_classes([IsAuthenticated])
def movie_list(request):
    response = third_party_movie_list()
    return Response(response, status=status.HTTP_200_OK)


class RequestCountView(APIView):
    '''only admin has access to this view'''

    permission_classes = [IsAuthenticated, AdminOnly]

    def get(self, request):
        count = request.session.get('request_count', 0)
        return Response({'requests': count})


class ResetRequestCountView(APIView):
    '''only admin has access to this view'''

    permission_classes = [IsAuthenticated, AdminOnly]

    def post(self, request):
        request.session['request_count'] = 0
        return Response({'message': 'Request count reset successfully'})


class MovieCollectionAV(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        collections = MovieCollection.objects.filter(user=request.user)
        top_three_generes = top_generes(collections)
        serializer = MovieCollectionSerializer(collections, many=True)
        return Response({'is_success': 'True', 'data': {'collection': serializer.data, 'favourite_genres': top_three_generes}})

    def post(self, request):
        serializer = MovieCollectionSerializer(data=request.data)
        if serializer.is_valid():
            instance = self.perform_create(serializer)
            return Response({'collection_uuid': serializer.data['id']}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        user = self.request.user
        instance = serializer.save(user=user)
        return instance


class MovieCollectionDetailAV(APIView):
    '''only user himself can see his own movie collection 
    and is able to alter the movie collection records speicific to him'''

    permission_classes = [IsAuthenticated, UserOnly]

    def get_object(self):
        try:
            obj = MovieCollection.objects.get(pk=self.kwargs['id'])
        except MovieCollection.DoesNotExist:
            return Response({'Error': f'Movie Collection with id {id} not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request=self.request, obj=obj)
        return obj

    def get(self, request, id):
        movie_collection = self.get_object()
        serializer = MovieCollectionSerializer(movie_collection)
        return Response(serializer.data)

    def put(self, request, id):
        movie_collection = self.get_object()
        serializer = MovieCollectionSerializer(
            movie_collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movie_collection = self.get_object()
        movie_collection.delete()
        return Response({'Success': f'Movie Collection with id {id} has been deleted'}, status=status.HTTP_204_NO_CONTENT)
