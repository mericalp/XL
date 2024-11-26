from django.urls import path
from .dataAccess import NeoModel


class BusinessBase:
    def __init__(self, route, model_class):
        self.urlpatterns = []
        self.route = route
        self.model_class = model_class

    def register_url(self, route, fnc, name):
        self.urlpatterns.append(path(route, fnc, name=name))



