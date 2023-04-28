from django.contrib.auth.models import User
from movie_app.models import Movie, MovieCollection
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
        }


class MovieCollectionSerializer(serializers.ModelSerializer):
    movies = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), write_only=True)

    class Meta:
        model = MovieCollection
        exclude = ('user',)

    def create(self, validated_data):
        movies_data = validated_data.pop('movies')
        movie_collection = MovieCollection.objects.create(**validated_data)
        for movie_data in movies_data:
            movie, created = Movie.objects.get_or_create(**movie_data)
            movie_collection.movies.add(movie)
        return movie_collection

    def update(self, instance, validated_data):
        movies = validated_data.pop('movies', [])
        db_movies = instance.movies.all()

        for movie in movies:
            movie_instance = db_movies.filter(id=movie.get('id')).first()

            if movie_instance:
                movie_serializer = MovieSerializer(movie_instance, data=movie)
            else:
                movie_serializer = MovieSerializer(data=movie)

            movie_serializer.is_valid(raise_exception=True)
            movie_serializer.save()

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password')

    def save(self):
        username = self.validated_data['username']
        password = self.validated_data['password']

        queryset = User.objects.filter(username=username)
        if queryset.exists():
            raise ValidationError('Username already exists')

        new_user = User(username=username)
        new_user.set_password(password)
        new_user.save()
        return new_user
