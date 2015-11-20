(function () {
  'use strict';

  angular
    .module('Store')
    .factory('StoreService', StoreService);

  StoreService.$inject = ['$http', 'API_SERVER'];

  function StoreService ($http, API_SERVER) {
    var service = {};

    service.getMerchantStores = function (merchant_id) {
      return $http.get(API_SERVER + 'api/users/' + merchant_id + '/stores/');
    };

    service.createStore = function (merchant_id, data) {
      return $http.post(API_SERVER + 'api/users/' + merchant_id + '/create_store/', data);
    };

    service.getStore = function (store_id) {
      return $http.get(API_SERVER + 'api/stores/' + store_id + '/store_info/');
    };

    service.deleteStore = function (store_id) {
      return $http.post(API_SERVER + 'api/users/' + store_id + '/delete_store/');
    };

    service.addProduct = function (store_id, data) {
      return $http.post(API_SERVER + 'api/stores/' + store_id + '/add_product/', data);
    };

    service.deleteStoreProduct = function (productId) {
      return $http.post(API_SERVER + 'api/stores/' + productId + '/delete_product/');
    };

    service.editStoreProduct = function (productId, data) {
      return $http.post(API_SERVER + 'api/stores/' + productId + '/edit_product/', data);
    };

    service.getStoreProducts = function (store_id) {
      return $http.get(API_SERVER + 'api/stores/' + store_id + '/products/');
    };

    return service;
  }
})();
