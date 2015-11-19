(function () {
  'use strict';

  angular.module('Auth')

  .controller('AuthController', AuthController);

  AuthController.$inject = ['$scope', '$state', 'AuthService', 'ngToast'];

  function AuthController ($scope, $state, AuthService, ngToast) {

    $scope.register = function () {
      var username = $scope.registerUsername;
      var password = $scope.registerPassword;
      var checkpassword = $scope.registerCheckPassword;

      if (username && password && checkpassword) {
        if (password != checkpassword) {
          ngToast.danger({
            content: 'Passwords do not match',
            dismissButton: true
          });
          return;
        }
        AuthService.register(username, password).then(
          function () {
            $state.go('index.home');
          },
          function (error) {
            ngToast.danger({
              content: error,
              dismissButton: true
            });
          }
        );
      } else {
        ngToast.danger({
          content: 'Username and password required',
          dismissButton: true
        });
      }
    };

    $scope.login = function () {
      var username = $scope.loginUsername;
      var password = $scope.loginPassword;

      if (username && password) {
        AuthService.login(username, password).then(
          function () {
            $state.go('index.home');
          },
          function (error) {
            ngToast.danger({
              content: error,
              dismissButton: true
            });
          }
        );
      } else {
        ngToast.danger({
          content: 'Username and password required',
          dismissButton: true
        });
      }
    };
  }
})();
