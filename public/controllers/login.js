var controllers = angular.module('app.controllers.Login', []);

controllers.controller('Login', function ($scope, $http, $location) {

    $scope.submitLogin = function () {
        var data = {
            username: $scope.user.username,
            password: $scope.user.password
        }

        $http.post('/api/login', data)
            .success(function(data) {
                $location.path('/');
            })
            .error(function(err, status) {
                $scope.error = {message: err.error, status: status};
            });
    };
});
