angular.module('goLive.controllers')
    .controller('HomeController', ['$scope', '$location', 'LiveService', function($scope, $location, LiveService){

        $scope.album = {
            'title': '',
            'upc': '',
            'artist': '',
            'distributor': 'spotify'
        };

        $scope.required = {
            'upc': true,
            'artist': false,
            'title': false
        };

        $scope.checkRequiredValues = function(distributor) {
            if(distributor === 'amazon'){
                $scope.required['artist'] = true;
                $scope.required['title'] = true;
                $scope.required['upc'] = false;
            } else {
                $scope.required['artist'] = false;
                $scope.required['title'] = false;
                $scope.required['upc'] = true;
            }
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
