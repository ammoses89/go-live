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
            if(distributor === 'amazon'){
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
            var distro = album.distributor;
            var params = {
                'upc': album.upc,
                'artist': album.artist,
                'album_title': album.album_title,
            };

            LiveService.checkStatus(album)
                .then(function(response){
                    $location.path('/status');
                }, function(err) {
                   console.error(err);
                });
        };
    }])
