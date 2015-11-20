(function () {
  'use strict';

  angular
    .module('Merchant')
    .controller('MerchantHomeController', MerchantHomeController)
    .controller('MerchantNavController', MerchantNavController);

  MerchantNavController.$inject = ['$scope', '$state', 'ngToast', 'AuthService'];

  function MerchantNavController ($scope, $state, ngToast, AuthService) {
    $scope.logout = function () {
      AuthService.logout().then(
        function () {
          $state.go('auth');
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

  MerchantHomeController.$inject = ['$scope', '$window', '$state', 'StoreService', 'ngToast'];

  function MerchantHomeController ($scope, $window, $state, StoreService, ngToast) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }

    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;

    $scope.getMerchantStores = function () {
      StoreService.getMerchantStores($scope.userId).then(
        function (response) {
          $scope.stores = response.data;
        },
        function (response) {
          ngToast.danger({
            content: "Error occurred while loading stores, try again",
            dismissButton: true
          });
        }
      );
    };

    $scope.getMerchantStores();
  }
})();
