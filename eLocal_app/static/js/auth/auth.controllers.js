(function () {
  'use strict';

  angular.module('Auth')

  .controller('AuthController', AuthController);

  AuthController.$inject = ['$scope', '$window', '$state', 'AuthService', 'ngToast', 'GeoCoder'];

  function AuthController ($scope, $window, $state, AuthService, ngToast, GeoCoder) {

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

    $scope.loginModel = {
      'radius': 5
    };
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
      },
      {
        key: 'zipcode',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Zipcode',
          required: true
        }
      },
      {
        key: 'radius',
        type: 'select',
        templateOptions: {
          label: 'Radius',
          options: [
            {
              name: "5 miles",
              value: 5
            },
            {
              name: "10 miles",
              value: 10
            },
            {
              name: "15 miles",
              value: 15
            },
            {
              name: "20 miles",
              value: 20
            },
            {
              name: "25 miles",
              value: 25
            },
            {
              name: "30 miles",
              value: 30
            }
          ]
        }
      }
    ];

    function enterZipcode () {
      if ($scope.loginModel.zipcode.length == 5 && $scope.loginModel.zipcode.match(/^[0-9]+$/) != null) {
        GeoCoder.geocode({address: $scope.loginModel.zipcode}).then(
          function (response) {
            var lat = response[0].geometry.location.lat();
            var lng = response[0].geometry.location.lng();
            $window.localStorage.zipcode = $scope.loginModel.zipcode;
            $window.localStorage.lat = lat;
            $window.localStorage.lng = lng;
            $window.localStorage.radius = $scope.loginModel.radius;
            $state.go('index.stores');
          },
          function (response) {
            $scope.loginFormOptions.resetModel();
            ngToast.danger({
              content: 'Enter a valid zipcode',
              dismissButton: true
            });
          }
        );
      } else {
        $scope.loginFormOptions.resetModel();
        ngToast.danger({
          content: 'Enter a valid zipcode',
          dismissButton: true
        });
      }
    }

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
          function () {
            $state.go('index.stores');
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
          enterZipcode();
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
