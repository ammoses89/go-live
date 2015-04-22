angular.module('goLive.controllers')
    .controller('HomeController', ['$scope', '$location', 'LiveService',
        function($scope, $location, LiveService){

        $scope.album = {
            'album_title': '',
            'upc': '',
            'artist': '',
            'distributor': 'spotify'
        };

        $scope.required = {
            'upc': true,
            'artist': false,
            'album_title': false
        };

        $scope.checkRequiredValues = function(distributor) {
            if(['amazon', 'deezer', 'google'].indexOf(distributor) >= 0){
                $scope.required['artist'] = true;
                $scope.required['album_title'] = true;
                $scope.required['upc'] = false;
            } else {
                $scope.required['artist'] = false;
                $scope.required['album_title'] = false;
                $scope.required['upc'] = true;
            }
        };

        $scope.checkStatus = function(album) {
            LiveService.checkStatus(album)
                .then(function(response){
                    $location.path('/status');
                }, function(err) {
                   console.error(err);
                });
        };
    }])
