(function () {
  'use strict';

  angular.module('Index')

  .controller('IndexNavController', IndexNavController)
  .controller('IndexStoreController', IndexStoreController);

  IndexNavController.$inject = ['$scope', '$window', '$state', 'ngToast'];

  function IndexNavController ($scope, $window, $state, ngToast) {
    $scope.zipcode = $window.localStorage.zipcode;

  }

  IndexStoreController.$inject = ['$scope', '$window', '$state', 'ngToast', 'StoreService'];

  function IndexStoreController ($scope, $window, $state, ngToast, StoreService) {
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;

    function getZipcodeStores () {
      StoreService.getZipcodeStores({'lat': lat, 'lng': lng}).then(
        function (response) {
          $scope.stores = response.data;
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

})();
