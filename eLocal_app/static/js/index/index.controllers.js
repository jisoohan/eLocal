(function () {
  'use strict';

  angular.module('Index')

  .controller('IndexNavController', IndexNavController)
  .controller('IndexStoreController', IndexStoreController)
  .controller('IndexProductController', IndexProductController);

  IndexNavController.$inject = ['$scope', '$window', '$state'];

  function IndexNavController ($scope, $window, $state) {
    $scope.zipcode = $window.localStorage.zipcode;
  }

  IndexStoreController.$inject = ['$scope', '$window', '$state', 'ngToast', 'StoreService', '$uibModal'];

  function IndexStoreController ($scope, $window, $state, ngToast, StoreService, $uibModal) {
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;

    function getZipcodeStores () {
      StoreService.getZipcodeStores({'lat': lat, 'lng': lng}).then(
        function (response) {
          $scope.stores = response.data;
          $scope.displayedStores = [].concat($scope.stores);
        },
        function (response) {
          ngToast.danger({
            content: "Error while loading stores",
            dismissButton: true
          });
        }
      );
    }
    getZipcodeStores();
  }

  IndexProductController.$inject = ['$scope', '$window', '$state', 'ngToast', 'StoreService'];

  function IndexProductController ($scope, $window, $state, ngToast, StoreService) {
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;

    function getZipcodeProducts() {
      StoreService.getZipcodeProducts({'lat': lat, 'lng': lng}).then(
        function (response) {
          $scope.products = response.data;
          for (var i = 0; i < $scope.products.length; i++) {
            $scope.products[i].price = Number($scope.products[i].price)
          }
          $scope.displayedProducts = [].concat($scope.products);
        },
        function (response) {
          ngToast.danger({
            content: "Error while loading products",
            dismissButton: true
          });
        }
      );
    }
    getZipcodeProducts();
  }

})();
