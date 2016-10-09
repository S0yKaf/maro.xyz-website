var controllers = angular.module('app.controllers.Admin', []);

controllers.controller('Admin', function ($scope, $http) {
    $http.get('/api/uploads')
        .success(function(uploads) {
            $scope.uploads = uploads.uploads;
        })
        .error(function(err, status) {
            $scope.error = {message: err, status: status};
        });

        $scope.block = function (upload) {
            $http.get('/api/block/' + upload.short_url)
                .success(function (res) {
                    upload.blocked = !upload.blocked
                })
                .error(function(err, status) {
                    $scope.error = {message: err, status: status};
                })
        }
});
