(function () {
  'use strict';

  angular.module('Index')

  .controller('NavController', NavController)
  .controller('LocationController', LocationController)
  .controller('MerchantController', MerchantController)
  .controller('MerchantStoreController', MerchantStoreController)
  .controller('MerchantEditProductController', MerchantEditProductController)
  .controller('StoresController', StoresController)
  .controller('ProductsController', ProductsController)
  .controller('StoreController', StoreController)
  .controller('IndexCartController', IndexCartController)
  .controller('EditProductController', EditProductController);

  NavController.$inject = ['$scope', '$rootScope', '$window', '$state', 'AuthService', 'ngToast'];

  function NavController ($scope, $rootScope, $window, $state, AuthService, ngToast) {
    $scope.username = $window.localStorage.username;
    $scope.zipcode = $window.localStorage.zipcode;
    $scope.radius = $window.localStorage.radius;
    if ($window.localStorage.is_staff == 'true') {
      $scope.is_staff = true;
    } else {
      $scope.is_staff = false;
    }
    $rootScope.$on('location.changed', function (event, data) {
      $scope.zipcode = $window.localStorage.zipcode;
      $scope.radius = $window.localStorage.radius;
    });
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

  LocationController.$inject = ['$scope', '$rootScope', '$window', '$state', 'ngToast', 'GeoCoder'];

  function LocationController ($scope, $rootScope, $window, $state, ngToast, GeoCoder) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }

    $scope.locationModel = {
      'radius': 5
    };
    $scope.locationFields = [
      {
        key: 'zipcode',
        type: 'input',
        templateOptions: {
          type: 'text',
          placeholder: 'Zipcode',
          required: true
        }
      },
      {
        key: 'radius',
        type: 'select',
        templateOptions: {
          label: 'Radius',
          options: [
            {
              name: "5 miles",
              value: 5
            },
            {
              name: "10 miles",
              value: 10
            },
            {
              name: "15 miles",
              value: 15
            },
            {
              name: "20 miles",
              value: 20
            },
            {
              name: "25 miles",
              value: 25
            },
            {
              name: "30 miles",
              value: 30
            }
          ]
        }
      }
    ];

    $scope.enterLocation = function () {
      if ($scope.locationModel.zipcode.length == 5 && $scope.locationModel.zipcode.match(/^[0-9]+$/) != null) {
        GeoCoder.geocode({address: $scope.locationModel.zipcode}).then(
          function (response) {
            var lat = response[0].geometry.location.lat();
            var lng = response[0].geometry.location.lng();
            $window.localStorage.zipcode = $scope.locationModel.zipcode;
            $window.localStorage.lat = lat;
            $window.localStorage.lng = lng;
            $window.localStorage.radius = $scope.locationModel.radius;
            $rootScope.$emit('location.changed', '');
            $state.go('index.stores');
          },
          function (response) {
            $scope.locationFormOptions.resetModel();
            ngToast.danger({
              content: 'Enter a valid zipcode',
              dismissButton: true
            });
          }
        );
      } else {
        $scope.locationFormOptions.resetModel();
        ngToast.danger({
          content: 'Enter a valid zipcode',
          dismissButton: true
        });
      }
    }

  }

  MerchantController.$inject = ['$scope', '$window', '$state', 'StoreService', 'ngToast'];

  function MerchantController ($scope, $window, $state, StoreService, ngToast) {
    if ($window.localStorage.is_staff == 'false') {
      $state.go('index.stores');
      return;
    }
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }

    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;
    $scope.storeForm = {};

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
      if ($scope.storeForm.store_name && $scope.storeForm.st_number && $scope.storeForm.st_name && $scope.storeForm.city && $scope.storeForm.state && $scope.storeForm.country && $scope.storeForm.zipcode && $scope.storeForm.lat && $scope.storeForm.lng) {
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
      } else {
        ngToast.warning({
          content: "Fill out all form fields",
          dismissButton: true
        });
      }
    };

    getMerchantStores();
  }

  MerchantStoreController.$inject = ['$scope', '$window', '$state', '$uibModal', '$stateParams', 'StoreService', 'ngToast', 'ProductService'];

  function MerchantStoreController ($scope, $window, $state, $uibModal, $stateParams, StoreService, ngToast, ProductService) {
    if ($window.localStorage.is_staff == 'false') {
      $state.go('index.stores');
      return;
    }
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }
    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;
    $scope.productForm = {};

    $scope.addProduct = function () {
      if ($scope.productForm.product_name && $scope.productForm.description && $scope.productForm.price) {
        ProductService.addProduct($stateParams.storeId, $scope.productForm).then(
          function (response) {
            response.data.price = Number(response.data.price)
            $scope.products.push(response.data);
            $scope.productForm = {};
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
      } else {
        ngToast.warning({
          content: 'Fill out all form fields',
          dismissButton: true
        });
      }
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
          ProductService.editProduct(product.id, productEditModel).then(
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
          $state.go('index.merchant');
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
        ProductService.deleteProduct(product.id).then(
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
      StoreService.getMerchantStore($stateParams.storeId).then(
        function (response) {
          $scope.store = response.data;
          ProductService.getStoreProducts($stateParams.storeId).then(
            function (response) {
              $scope.products = response.data;
              for (var i = 0; i < $scope.products.length; i++) {
                $scope.products[i].price = Number($scope.products[i].price)
              }
              $scope.displayedProducts = [].concat($scope.products);
            },
            function (response) {
              $state.go('index.merchant');
              ngToast.danger({
                content: "Error while loading products",
                dismissButton: true
              });
            }
          );
        },
        function (response) {
          $state.go('index.merchant');
          ngToast.danger({
            content: "Error while loading store",
            dismissButton: true
          });
        }
      );
    }

    getStore();

  }

  StoresController.$inject = ['$scope', '$window', '$state', 'ngToast', 'StoreService', '$uibModal'];

  function StoresController ($scope, $window, $state, ngToast, StoreService, $uibModal) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }
    if (!$window.localStorage.zipcode) {
      $state.go('index.location');
      ngToast.warning({
        content: "Enter a location",
        dismissButton: true
      });
      return;
    }
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;
    var radius = $window.localStorage.radius;

    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;

    function getZipcodeStores () {
      StoreService.getZipcodeStores({'lat': lat, 'lng': lng, 'radius': radius}).then(
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

  ProductsController.$inject = ['$scope', '$window', '$state', '$uibModal', 'ngToast', 'ProductService'];

  function ProductsController ($scope, $window, $state, $uibModal, ngToast, ProductService) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }
    if (!$window.localStorage.zipcode) {
      $state.go('index.location');
      ngToast.warning({
        content: "Enter a location",
        dismissButton: true
      });
      return;
    }
    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;
    var radius = $window.localStorage.radius;

    $scope.editProduct = function (product) {
      var index = $scope.products.indexOf(product);
      if (index !== -1) {
        var editProductModal = $uibModal.open({
          animation: true,
          templateUrl: '/static/js/modals/views/editProduct.html',
          controller: 'EditProductController',
          size: 'sm',
          resolve: {
            price: function () {
              return product.price;
            }
          }
        });
        editProductModal.result.then(function (productEditModel) {
          ProductService.editProduct(product.id, productEditModel).then(
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
      ProductService.getZipcodeProducts({'lat': lat, 'lng': lng, 'radius': radius}).then(
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

  StoreController.$inject = ['$scope', '$window', '$stateParams', '$uibModal', 'StoreService', 'ngToast', 'ProductService'];

  function StoreController ($scope, $window, $stateParams, $uibModal, StoreService, ngToast, ProductService) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }

    var zipcode = $window.localStorage.zipcode;
    var lat = $window.localStorage.lat;
    var lng = $window.localStorage.lng;

    $scope.username = $window.localStorage.username;
    $scope.userId = $window.localStorage.userId;

    $scope.editProduct = function (product) {
      var index = $scope.products.indexOf(product);
      if (index !== -1) {
        var editProductModal = $uibModal.open({
          animation: true,
          templateUrl: '/static/js/modals/views/editProduct.html',
          controller: 'EditProductController',
          size: 'sm',
          resolve: {
            price: function () {
              return product.price;
            }
          }
        });
        editProductModal.result.then(function (productEditModel) {
          ProductService.editProduct(product.id, productEditModel).then(
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
          ProductService.getStoreProducts($stateParams.storeId).then(
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

  IndexCartController.$inject = ['$scope', '$window', 'ngToast', 'ngCart', 'NgMap'];

  function IndexCartController ($scope, $window, ngToast, ngCart, NgMap) {
    if (!$window.localStorage.token) {
      $state.go('auth');
      return;
    }

    $scope.lat = $window.localStorage.lat;
    $scope.lng = $window.localStorage.lng;

    $scope.routePath = function () {
      $scope.wayPoints = [];
      var seenStores = [];
      var products = ngCart.getItems();
      for (var i = 0; i < products.length; i++) {
        var wayPoint = {
          location: {
            lat: products[i].getData().address.lat,
            lng: products[i].getData().address.lng
          },
          stopover: true
        };
        var index = seenStores.indexOf(products[i].getData().id);
        if (index == -1) {
          seenStores.push(products[i].getData().id);
          $scope.wayPoints.push(wayPoint);
        }
      }
    };
  }

  EditProductController.$inject = ['$scope', '$uibModalInstance', 'price'];

  function EditProductController ($scope, $uibModalInstance, price) {

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
