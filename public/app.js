var app = angular.module('myblt', [
    'ngRoute',
    'ngFileUpload',
    'ngCookies',
    'ngSanitize',
    'app.controllers.Index',
    'app.controllers.Admin',
    'app.controllers.Login',
    'app.controllers.Register',
    'app.controllers.Invites',
])

app.config(['$routeProvider', '$httpProvider', function($routeProvider) {
    $routeProvider
        .when('/', {templateUrl: 'partials/index.html', controller: 'Index',})
        .when('/blocked', {templateUrl: 'partials/blocked.html', controller: 'Blocked',})
        .when('/admin', {templateUrl: 'partials/admin.html', controller: 'Admin',})
        .when('/login', {templateUrl: 'partials/login.html', controller: 'Login',})
        .when('/register', {templateUrl: 'partials/register.html', controller: 'Register',})
        .when('/invites', {templateUrl: 'partials/invites.html', controller: 'Invites',});
    $routeProvider.otherwise({redirectTo: '/'});
}]);

app.filter('reverse', function() {
  return function(items) {
    return items.slice().reverse();
  };
});
