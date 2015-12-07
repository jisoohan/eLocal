(function () {
  'use strict';

  angular.module('Auth')

  .controller('AuthController', AuthController);

  AuthController.$inject = ['$scope', '$window', '$state', 'AuthService', 'ngToast'];

  function AuthController ($scope, $window, $state, AuthService, ngToast) {

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
      },
      {
        key: 'is_staff',
        type: 'checkbox',
        templateOptions: {
          label: 'Merchant'
        }
      }
    ];

    $scope.loginModel = {};
    $scope.loginFields = [
      {
        "className": "row",
        "fieldGroup": [
          {
            "className": "col-xs-6",
            key: 'username',
            type: 'input',
            templateOptions: {
              type: 'text',
              placeholder: 'Username',
              required: true
            }
          },
          {
            "className": "col-xs-6",
            key: 'password',
            type: 'input',
            templateOptions: {
              type: 'password',
              placeholder: 'Password',
              required: true
            }
          }
        ]
      }
    ];

    $scope.register = function () {
      if ($scope.registerModel.is_staff == null) {
        $scope.registerModel.is_staff = false;
      }
      if ($scope.registerModel.password != $scope.registerModel.checkpw) {
        ngToast.danger({
          content: 'Passwords do not match',
          dismissButton: true
        });
      } else {
        AuthService.register($scope.registerModel).then(
          function (response) {
            $state.go('index.location');
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
      AuthService.login($scope.loginModel).then(
        function () {
          $state.go('index.location');
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
