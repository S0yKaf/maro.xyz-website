var controllers = angular.module('app.controllers.Index', ['ngFileUpload']);

controllers.controller('Index', function($scope, Upload) {

    $scope.upload = function(file) {
        Upload.upload({
            url: 'http://myb.lt/api/upload',
            file: file
        }).progress(function (evt) {
            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
            console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
        }).success(function (data, status, headers, config) {
            console.log('file ' + file[0].name + ' uploaded');
        });
    }
});
