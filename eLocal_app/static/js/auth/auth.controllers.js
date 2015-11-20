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

    $scope.zipcodeModel = {};
    $scope.zipcodeFields = [
      {
        key: 'zipcode',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Zipcode',
          required: true
        }
      }
    ];

    $scope.enterZipcode = function () {
      if ($scope.zipcodeModel.zipcode.length == 5 && $scope.zipcodeModel.zipcode.match(/^[0-9]+$/) != null) {
        GeoCoder.geocode({address: $scope.zipcodeModel.zipcode}).then(
          function (response) {
            var lat = response[0].geometry.location.lat();
            var lng = response[0].geometry.location.lng();
            $window.localStorage.zipcode = $scope.zipcodeModel.zipcode;
            $window.localStorage.lat = lat;
            $window.localStorage.lng = lng;
            $state.go('index.stores');
          },
          function (response) {
            $scope.zipcodeFormOptions.resetModel();
            ngToast.danger({
              content: 'Enter a valid zipcode',
              dismissButton: true
            });
          }
        );
      } else {
        $scope.zipcodeFormOptions.resetModel();
        ngToast.danger({
          content: 'Enter a valid zipcode',
          dismissButton: true
        });
      }
    };

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
