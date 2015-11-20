(function () {
  'use strict';

  angular.module('Index')

  .controller('IndexNavController', IndexNavController)
  .controller('IndexStoreController', IndexStoreController)
  .controller('IndexAddProductController', IndexAddProductController)
  .controller('IndexEditProductController', IndexEditProductController);

  IndexNavController.$inject = ['$scope', '$window', '$state', 'ngToast'];

  function IndexNavController ($scope, $window, $state, ngToast) {
    $scope.zipcode = $window.localStorage.zipcode;

  }

  IndexStoreController.$inject = ['$scope', '$window', '$state', 'ngToast', 'StoreService', '$uibModal'];

  function IndexStoreController ($scope, $window, $state, ngToast, StoreService, $uibModal) {
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;

    $scope.addProduct = function (index, storeId) {
      var addProductModal = $uibModal.open({
        animation: true,
        templateUrl: '/static/js/modals/views/addProduct.html',
        controller: 'IndexAddProductController',
        size: 'md'
      });
      addProductModal.result.then(function (productAddModel) {
        StoreService.addProduct(storeId, productAddModel).then(
          function (response) {
            $scope.stores[index].products.push(response.data);
            ngToast.success({
              content: "Product Added",
              dismissButton: true
            });
          },
          function (response) {
            ngToast.danger({
              content: "Error while adding product",
              dismissButton: true
            });
          }
        );
      });
    };

    $scope.editProduct = function (store_index, product_index, product_id, product_name, description, price) {
      var editProductModal = $uibModal.open({
        animation: true,
        templateUrl: '/static/js/modals/views/editProduct.html',
        controller: 'IndexEditProductController',
        size: 'md',
        resolve: {
          product_name: function () {
            return product_name;
          },
          description: function () {
            return description;
          },
          price: function () {
            return price;
          }
        }
      });
      editProductModal.result.then(function (productEditModel) {
        StoreService.editStoreProduct(product_id, productEditModel).then(
          function (response) {
            $scope.stores[store_index].products[product_index].name = response.data.name;
            $scope.stores[store_index].products[product_index].description = response.data.description;
            $scope.stores[store_index].products[product_index].price = response.data.price;
            ngToast.success({
              content: "Product updated",
              dismissButton: true
            });
          },
          function (response) {
            ngToast.danger({
              content: "Error while updating product",
              dismissButton: true
            });
          }
        );
      });
    };

    $scope.deleteProduct = function (store_index, product_index, product_id) {
      StoreService.deleteStoreProduct(product_id).then(
        function (response) {
          $scope.stores[store_index].products.splice(product_index, 1);
          ngToast.success({
            content: "Deleted product",
            dismissButton: true
          });
        },
        function (response) {
          ngToast.danger({
            content: "Error while deleting product",
            dismissButton: true
          });
        }
      );
    };

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

  IndexAddProductController.$inject = ['$scope', '$uibModalInstance'];

  function IndexAddProductController ($scope, $uibModalInstance) {
    $scope.productAddModel = {};
    $scope.productAddFields = [
      {
        key: 'product_name',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Product name',
          required: true
        }
      },
      {
        key: 'description',
        type: 'textarea',
        templateOptions: {
          placeholder: 'Description',
          required: true
        }
      },
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

    $scope.addProduct = function () {
      $uibModalInstance.close($scope.productAddModel);
    };

    $scope.cancel = function () {
      $uibModalInstance.dismiss('cancel');
    };
  }

  IndexEditProductController.$inject = ['$scope', '$uibModalInstance', 'product_name', 'description', 'price'];

  function IndexEditProductController ($scope, $uibModalInstance, product_name, description, price) {

    $scope.productEditModel = {
      'product_name': product_name,
      'description': description,
      'price': Number(price)
    };
    $scope.productEditFields = [
      {
        key: 'product_name',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Product name',
          required: true
        }
      },
      {
        key: 'description',
        type: 'textarea',
        templateOptions: {
          placeholder: 'Description',
          required: true
        }
      },
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
