(function () {
  'use strict';

  angular
    .module('Merchant')
    .controller('MerchantHomeController', MerchantHomeController)
    .controller('MerchantNavController', MerchantNavController)
    .controller('MerchantStoreController', MerchantStoreController)
    .controller('MerchantEditProductController', MerchantEditProductController);

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
          $scope.displayedStores = [].concat($scope.stores);
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
          $scope.storeForm = null;
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

  MerchantStoreController.$inject = ['$scope', '$window', '$state', '$uibModal', '$stateParams', 'StoreService', 'ngToast'];

  function MerchantStoreController ($scope, $window, $state, $uibModal, $stateParams, StoreService, ngToast) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }
    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;

    $scope.productModel = {};
    $scope.productFields = [
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
      StoreService.addProduct($stateParams.storeId, $scope.productModel).then(
        function (response) {
          response.data.price = Number(response.data.price)
          $scope.products.push(response.data);
          $scope.options.resetModel();
          ngToast.success({
            content: 'Product added',
            dismissButton: true
          });
        },
        function (response) {
          ngToast.danger({
            content: 'Error while adding product',
            dismissButton: true
          });
        }
      );
    };

    $scope.editProduct = function (product) {
      var index = $scope.products.indexOf(product);
      if (index !== -1) {
        var editProductModal = $uibModal.open({
          animation: true,
          templateUrl: '/static/js/modals/views/editProduct.html',
          controller: 'MerchantEditProductController',
          size: 'md',
          resolve: {
            product: function () {
              return product;
            }
          }
        });
        editProductModal.result.then(function (productEditModel) {
          StoreService.editStoreProduct(product.id, productEditModel).then(
            function (response) {
              $scope.products[index].name = response.data.name;
              $scope.products[index].description = response.data.description;
              $scope.products[index].price = Number(response.data.price);
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
      } else {
        ngToast.danger({
          content: "Error while updating product",
          dismissButton: true
        });
      }
    };

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

    $scope.deleteProduct = function (product) {
      var index = $scope.products.indexOf(product);
      if (index !== -1) {
        StoreService.deleteStoreProduct(product.id).then(
          function (response) {
            $scope.products.splice(index, 1);
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
      } else {
        ngToast.danger({
          content: "Error while deleting product",
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
              $state.go('merchant.home');
              ngToast.danger({
                content: "Error while loading products",
                dismissButton: true
              });
            }
          );
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

  MerchantEditProductController.$inject = ['$scope', '$uibModalInstance', 'product'];

  function MerchantEditProductController ($scope, $uibModalInstance, product) {

    $scope.productEditModel = {
      'product_name': product.name,
      'description': product.description,
      'price': product.price
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
