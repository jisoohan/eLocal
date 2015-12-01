(function () {
  'use strict';

  angular
    .module('Product')
    .factory('ProductService', ProductService);

  ProductService.$inject = ['$http', 'API_SERVER', 'Upload'];

  function ProductService ($http, API_SERVER, Upload) {
    var service = {};

    service.getZipcodeProducts = function (data) {
      return $http.post(API_SERVER + 'api/products/products_in_zipcode/', data);
    };

    service.editProduct = function (productId, data) {
      return $http.post(API_SERVER + 'api/products/' + productId + '/edit/', data);
    };

    service.addProduct = function (store_id, data) {
      return Upload.upload({
        url: API_SERVER + 'api/products/' + store_id + '/add/',
        data: data
      });
    };

    service.getStoreProducts = function (store_id) {
      return $http.get(API_SERVER + 'api/products/' + store_id + '/store_products/');
    };

    service.deleteProduct = function (productId) {
      return $http.post(API_SERVER + 'api/products/' + productId + '/delete_product/');
    };

    return service;
  }
})();
