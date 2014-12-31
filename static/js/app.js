var app = angular.module('goLive', [
    'goLive.controllers',
    'ngRoute',
    ]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    'use strict';
    $routeProvider
        .when('/', {
            templateUrl: '/static/templates/home.html',
            controller: 'HomeController'
        })
        .otherwise({redirectTo: '/'})
}]);

