angular.module('goLive.services')
    .service('LiveService', ['$http', '$q', function($http, $q){
        var albumResults = null;

        return {
            checkStatus: function(opts) {
                var distro = opts.distributor;
                delete opts.distributor;
                var deferred = $q.defer();
                albumResults = null;
                $http.get('/api/' + distro, {params: opts})
                    .success(function(response){
                        albumResults = response;
                        return deferred.resolve(response);
                    })
                    .error(function(err){
                        return deferred.reject(err)
                    });
                    return deferred.promise;
            },

            getStatus: function() {
                return albumResults;
            },
        }

    }]);