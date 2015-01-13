angular.module('goLive.controllers')
    .controller('HomeController', ['$scope', '$location', 'LiveService', function($scope, $location, LiveService){

        $scope.album = {
            'title': '',
            'upc': '',
            'artist': '',
            'distributor': 'spotify'
        };

        $scope.checkStatus = function(album) {
            LiveService.checkStatus(album)
                .then(function(respone){
                    $location.path('/status');
                }, function(err) {
                   console.error(err);
                });
        };
    }])
