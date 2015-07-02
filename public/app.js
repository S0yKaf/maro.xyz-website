
var app = angular.module('myblt', ['ngRoute','ngFileUpload','app.controllers.Index'])


app.controller('Admin', function ($scope, $http) {
  $http.get('/api/uploads')
    .success(function(uploads) {
      $scope.uploads = uploads.uploads;
    })
    .error(function(err, status) {
      $scope.error = {message: err, status: status};
    });
});

app.config(['$routeProvider', '$httpProvider', function($routeProvider) {
    $routeProvider
    .when('/', {templateUrl: 'partials/index.html', controller: 'Index',})
    .when('/blocked', {templateUrl: 'partials/blocked.html', controller: 'Blocked',})
    .when('/admin', {templateUrl: 'partials/admin.html', controller: 'Admin',});
    $routeProvider.otherwise({redirectTo: '/'});
}]);
