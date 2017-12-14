var controllers = angular.module('app.controllers.Register', []);

controllers.controller('Register', function ($scope, $http, $location) {

    $scope.submitRegister = function () {
        var data = {
            username: $scope.user.username,
            password: $scope.user.password,
            invite_code: $scope.user.invite_code
        }

        $http.post('/api/register', data)
            .success(function(data) {
                $location.path('/login');
            })
            .error(function(err, status) {
                $scope.error = {message: err.error, status: status};
            });
    };
});
