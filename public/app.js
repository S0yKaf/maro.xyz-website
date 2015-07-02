var app = angular.module('myblt', ['ngRoute', 'ngFileUpload', 'app.controllers.Index', 'app.controllers.Admin', 'app.controllers.Login'])

app.config(['$routeProvider', '$httpProvider', function($routeProvider) {
    $routeProvider
        .when('/', {templateUrl: 'partials/index.html', controller: 'Index',})
        .when('/blocked', {templateUrl: 'partials/blocked.html', controller: 'Blocked',})
        .when('/admin', {templateUrl: 'partials/admin.html', controller: 'Admin',})
        .when('/login', {templateUrl: 'partials/login.html', controller: 'Login',});
    $routeProvider.otherwise({redirectTo: '/'});
}]);
