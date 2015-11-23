(function () {
  'use strict';

  angular.module('Index')

  .controller('IndexNavController', IndexNavController)
  .controller('IndexStoreController', IndexStoreController)
  .controller('IndexProductController', IndexProductController)
  .controller('IndexSingleStoreController', IndexSingleStoreController)
  .controller('IndexCartController', IndexCartController)
  .controller('IndexEditProductController', IndexEditProductController);

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

  IndexProductController.$inject = ['$scope', '$window', '$state', '$uibModal', 'ngToast', 'StoreService'];

  function IndexProductController ($scope, $window, $state, $uibModal, ngToast, StoreService) {
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;

    $scope.editProduct = function (product) {
      var index = $scope.products.indexOf(product);
      if (index !== -1) {
        var editProductModal = $uibModal.open({
          animation: true,
          templateUrl: '/static/js/modals/views/editProduct.html',
          controller: 'IndexEditProductController',
          size: 'sm',
          resolve: {
            price: function () {
              return product.price;
            }
          }
        });
        editProductModal.result.then(function (productEditModel) {
          StoreService.editStoreProduct(product.id, productEditModel).then(
            function (response) {
              $scope.products[index].price = Number(response.data.price);
              ngToast.success({
                content: "Price updated",
                dismissButton: true
              });
            },
            function (response) {
              ngToast.danger({
                content: "Error while updating price",
                dismissButton: true
              });
            }
          );
        });
      } else {
        ngToast.danger({
          content: "Error while updating price",
          dismissButton: true
        });
      }
    };

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

  IndexSingleStoreController.$inject = ['$scope', '$stateParams', '$uibModal', 'StoreService', 'ngToast'];

  function IndexSingleStoreController ($scope, $stateParams, $uibModal, StoreService, ngToast) {

    $scope.editProduct = function (product) {
      var index = $scope.products.indexOf(product);
      if (index !== -1) {
        var editProductModal = $uibModal.open({
          animation: true,
          templateUrl: '/static/js/modals/views/editProduct.html',
          controller: 'IndexEditProductController',
          size: 'sm',
          resolve: {
            price: function () {
              return product.price;
            }
          }
        });
        editProductModal.result.then(function (productEditModel) {
          StoreService.editStoreProduct(product.id, productEditModel).then(
            function (response) {
              $scope.products[index].price = Number(response.data.price);
              ngToast.success({
                content: "Price updated",
                dismissButton: true
              });
            },
            function (response) {
              ngToast.danger({
                content: "Error while updating price",
                dismissButton: true
              });
            }
          );
        });
      } else {
        ngToast.danger({
          content: "Error while updating price",
          dismissButton: true
        });
      }
    };

    function getStore() {
      StoreService.getStore($stateParams.storeId).then(
        function (response) {
          $scope.store = response.data;
          StoreService.getStoreProducts($stateParams.storeId).then(
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
        },
        function (response) {
          ngToast.danger({
            content: "Error while loading store",
            dismissButton: true
          });
        }
      );
    }
    getStore();
  }

  IndexCartController.$inject = ['$scope', 'ngToast', 'ngCart'];

  function IndexCartController ($scope, ngToast, ngCart) {

  }

  IndexEditProductController.$inject = ['$scope', '$uibModalInstance', 'price'];

  function IndexEditProductController ($scope, $uibModalInstance, price) {

    $scope.productEditModel = {
      'price': price
    };
    $scope.productEditFields = [
      {
        key: 'price',
        type: 'input',
        templateOptions: {
          type: 'number',
          placeholder: 'Price',
          required: true
        }
      }
    ];

    $scope.editProduct = function () {
      $uibModalInstance.close($scope.productEditModel);
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  }

})();
