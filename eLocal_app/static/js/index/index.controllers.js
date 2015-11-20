(function () {
  'use strict';

  angular.module('Index')

  .controller('IndexNavController', IndexNavController);

  IndexNavController.$inject = ['$scope', '$window', '$state', 'ngToast'];

  function IndexNavController ($scope, $window, $state, ngToast) {
    $scope.zipcode = $window.localStorage.zipcode;

    $scope.enterZipcode = function () {
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
    };

  }
})();
