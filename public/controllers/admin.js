var controllers = angular.module('app.controllers.Admin', []);

controllers.controller('Admin', function ($scope, $http) {
    $http.get('/api/uploads')
        .success(function(uploads) {
            $scope.uploads = uploads.uploads;
        })
        .error(function(err, status) {
            $scope.error = {message: err, status: status};
        });
});
