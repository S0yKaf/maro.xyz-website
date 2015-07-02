var controllers = angular.module('app.controllers.Index', ['ngFileUpload', 'ngCookies']);

controllers.controller('Index', function ($scope, $http, $cookies, $location, Upload) {

    $scope.upload = function (file) {
        delete $scope.uploadSuccess;

        Upload.upload({
            url: 'http://myb.lt/api/upload',
            file: file
        }).progress(function (evt) {
            $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
        }).success(function (data, status, headers, config) {
            $scope.uploadSuccess = {filename: file[0].name, short_url: data.short_url};
            delete $scope.file;
            delete $scope.progress;
        });
    }

    function isAppPrivate(cb) {
        $http.get('/api/private')
            .success(function(data) {
                cb(data.private);
            })
            .error(function(err, status) {
                $scope.error = {message: err, status: status};
            });
    }

    function verify() {
        isAppPrivate(function (isPrivate) {
            if (isPrivate && !$cookies.token) {
                $location.path('/login');
            }
        });
    }

    verify();
});
