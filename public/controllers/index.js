var controllers = angular.module('app.controllers.Index', ['ngFileUpload']);

controllers.controller('Index', function ($scope, Upload) {

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
});
