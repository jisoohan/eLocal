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

    $scope.createStore = function () {
      StoreService.createStore($scope.userId, $scope.storeForm).then(
        function (response) {
          $scope.stores.push(response.data);
        },
        function (response) {
          ngToast.danger({
            content: "Error while creating store",
            dismissButton: true
          });
        }
      );
    };

    $scope.getMerchantStores();
  }
})();
