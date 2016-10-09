var controllers = angular.module('app.controllers.Index', ['ngFileUpload', 'ngCookies']);

controllers.controller('Index', function ($scope, $http, $cookies, $location, $sce, Upload) {

    $scope.alerts = [];
    $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
    };

    $scope.upload = function (file) {
        delete $scope.uploadSuccess;

        Upload.upload({
            url: 'https://maro.xyz/api/upload',
            file: file
        }).progress(function (evt) {
            $scope.progress = parseInt(100.0 * evt.loaded / evt.total);
        }).success(function (data, status, headers, config) {
            $scope.uploadSuccess = {filename: file[0].name, short_url: data.short_url};
            var url = data.short_url;
            var msg = file[0].name + ' uploaded to <a style="color: #314F00" href="' + data.short_url + '">'+data.short_url+'</a>';
            var trusted =  $scope.thisCanBeusedInsideNgBindHtml = $sce.trustAsHtml(msg);
            var alert = {
                url: url,
                msg: trusted,
                type: 'success'};
                console.log(alert);
            $scope.alerts.push(alert);

            delete $scope.file;
            delete $scope.progress;
        }).error(function (data, status, headers, config) {
            console.log(status);
            if (status == 413) {
                $scope.alerts.push({msg: 'Your file is too big !', type: 'danger'});
            } else {
                $scope.alerts.push({msg: data.error, type: 'danger'});
            }
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
