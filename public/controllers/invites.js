var controllers = angular.module('app.controllers.Invites', []);

controllers.controller('Invites', function ($scope, $http, $window) {
    $http.get('/api/InviteCodes')
        .success(function(codes) {
            $scope.codes = codes.codes;
        })
        .error(function(err, status) {
            $window.location.href = '/#/login'
        });

    $scope.generate_invite = function () {
      $http.get('/api/CreateInviteCode')
          .success(function(code) {
              $scope.codes.unshift({
                code : code.invite_code,
                redeemed : false
              });
          })
          .error(function(err, status) {
              $window.location.href = '/#/login'
          });
    };

});
