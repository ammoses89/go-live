angular.module('goLive.controllers', []);
angular.module('goLive.services', []);

var app = angular.module('goLive', [
    'goLive.controllers',
    'goLive.services',
    'ngRoute',
    ]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    'use strict';
    $routeProvider
        .when('/', {
            templateUrl: '/static/templates/home.html',
            controller: 'HomeController'
        })
        .when('/notify', {
            templateUrl: '/static/templates/notify.html',
            controller: 'NotifyController'
        })
        .when('/api', {
            templateUrl: '/static/templates/api.html',
            controller: 'ApiController'
        })
        .when('/status', {
            templateUrl: '/static/templates/status.html',
            controller: 'StatusController'
        })
        .otherwise({redirectTo: '/'})
}]);

