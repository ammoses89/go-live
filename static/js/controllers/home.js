angular.module('goLive.controllers')
    .controller('HomeController', ['$scope', '$location', 'LiveService', function($scope, $location, LiveService){

        $scope.album = {
            'title': 'VF',
            'upc': '884502232769',
            'artist': 'Vintage Fresh',
            'distributor': 'itunes'
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
