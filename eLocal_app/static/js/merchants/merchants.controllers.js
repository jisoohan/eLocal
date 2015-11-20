(function () {
  'use strict';

  angular
    .module('Merchant')
    .controller('MerchantHomeController', MerchantHomeController)
    .controller('MerchantNavController', MerchantNavController)
    .controller('MerchantStoreController', MerchantStoreController);

  MerchantNavController.$inject = ['$scope', '$window', '$state', 'ngToast', 'AuthService'];

  function MerchantNavController ($scope, $window, $state, ngToast, AuthService) {
    $scope.username = $window.localStorage.username;
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

    $scope.placeChanged = function() {
       $scope.storeModel = this.getPlace();
       $scope.storeForm = {};
       $scope.storeForm.store_name = $scope.storeModel.name;
       $scope.storeForm.has_card = false;
       for (var i = 0; i < $scope.storeModel.address_components.length; i++) {
        if ($scope.storeModel.address_components[i].types.indexOf('street_number') != -1) {
          $scope.storeForm.st_number = $scope.storeModel.address_components[i].long_name;
        }
        if ($scope.storeModel.address_components[i].types.indexOf('route') != -1) {
          $scope.storeForm.st_name = $scope.storeModel.address_components[i].long_name;
        }
        if ($scope.storeModel.address_components[i].types.indexOf('locality') != -1) {
          $scope.storeForm.city = $scope.storeModel.address_components[i].long_name;
        }
        if ($scope.storeModel.address_components[i].types.indexOf('administrative_area_level_1') != -1) {
          $scope.storeForm.state = $scope.storeModel.address_components[i].short_name;
        }
        if ($scope.storeModel.address_components[i].types.indexOf('country') != -1) {
          $scope.storeForm.country = $scope.storeModel.address_components[i].short_name;
        }
        if ($scope.storeModel.address_components[i].types.indexOf('postal_code') != -1) {
          $scope.storeForm.zipcode = $scope.storeModel.address_components[i].short_name;
        }
       }
       $scope.storeForm.lat = $scope.storeModel.geometry.location.lat();
       $scope.storeForm.lng = $scope.storeModel.geometry.location.lng();
    };

    function getMerchantStores () {
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
    }

    $scope.createStore = function () {
      StoreService.createStore($scope.userId, $scope.storeForm).then(
        function (response) {
          $scope.stores.push(response.data);
          $scope.storeForm = {};
          $scope.address = null;
          ngToast.success({
            content: "Created store",
            dismissButton: true
          });
        },
        function (response) {
          ngToast.danger({
            content: "Error while creating store",
            dismissButton: true
          });
        }
      );
    };

    getMerchantStores();
  }

  MerchantStoreController.$inject = ['$scope', '$window', '$state', '$stateParams', 'StoreService', 'ngToast'];

  function MerchantStoreController ($scope, $window, $state, $stateParams, StoreService, ngToast) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }
    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;

    $scope.deleteStore = function () {
      StoreService.deleteStore($stateParams.storeId).then(
        function (response) {
          $state.go('merchant.home');
          ngToast.success({
            content: "Deleted store",
            dismissButton: true
          });
        },
        function (response) {
          ngToast.danger({
            content: "Error while deleting store",
            dismissButton: true
          });
        }
      );
    };

    function getStore() {
      StoreService.getStore($stateParams.storeId).then(
        function (response) {
          $scope.store = response.data;
        },
        function (response) {
          $state.go('merchant.home');
          ngToast.danger({
            content: "Error while loading store",
            dismissButton: true
          });
        }
      );
    }

    getStore();

  }


})();
