angular.module('goLive.controllers')
    .controller('StatusController', ['$scope', 'LiveService', function($scope, LiveService){
        $scope.results = {
            'color': 'red',
            'status': 'Noop',
            'message': 'Nothing here',
            'albumLink': ''
        }

        $scope.getStatus = function() {
            var results = LiveService.getStatus()
            if(results && typeof results === 'object'){
                $scope.results = results;
            }
        };

        $scope.getStatus();

    }]);