# Movie-Collection-Backend

#this project consists of following features


1)Integration of a third party API which serves a list of movies
    Integration with 3rd party API which serves a list of movies and their genres
    Username and Password are abstracted and stored in .env
    
2)Implementation of a request counter middleware
    a monitoring system of counting the number of requests done to this server. Written a 
    1.custom middleware for counting all requests coming to the server.
    2.an API to return the number of requests which have been served by the server till now. 
    3.API to reset the counter.


3)Implementation of retrying mechanism
    since 3rd party API is flaky, and often fails and/or time outs,
    implmented built-in retry mechanisms in the project to fectch data provided by this api.
    
4)Implementation of JWT authentication
     users can register using a username and password, which should return a JWT token which should be used for authentication.

4)other
    Users are able to see the list of movies and add any movie which they like into their collections.
    Each user can create multiple collections and multiple movies into the collections.
