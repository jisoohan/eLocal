(function () {
  'use strict';

  angular.module('Auth')

  .controller('AuthController', AuthController);

  AuthController.$inject = ['$scope', '$state', 'AuthService', 'ngToast'];

  function AuthController ($scope, $state, AuthService, ngToast) {

    $scope.registerModel = {};
    $scope.registerFields = [
      {
        key: 'username',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Username',
          required: true
        }
      },
      {
        key: 'password',
        type: 'input',
        templateOptions: {
          type: 'password',
          placeholder: 'Password',
          required: true
        }
      },
      {
        key: 'checkpw',
        type: 'input',
        templateOptions: {
          type: 'password',
          placeholder: 'Enter password again',
          required: true
        }
      }
    ];

    $scope.loginModel = {};
    $scope.loginFields = [
      {
        key: 'username',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Username',
          required: true
        }
      },
      {
        key: 'password',
        type: 'input',
        templateOptions: {
          type: 'password',
          placeholder: 'Password',
          required: true
        }
      }
    ];

    $scope.register = function () {
      if ($scope.registerModel.password != $scope.registerModel.checkpw) {
        ngToast.danger({
          content: 'Passwords do not match',
          dismissButton: true
        });
      } else {
        AuthService.register($scope.registerModel.username, $scope.registerModel.password).then(
          function () {
            $state.go('merchant.home');
          },
          function (error) {
            ngToast.danger({
              content: error,
              dismissButton: true
            });
          }
        );
      }
    };

    $scope.login = function () {
      AuthService.login($scope.loginModel.username, $scope.loginModel.password).then(
        function () {
          $state.go('merchant.home');
        },
        function (error) {
          ngToast.danger({
            content: error,
            dismissButton: true
          });
        }
      );
    };

  }
})();
