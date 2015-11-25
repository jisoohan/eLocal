(function () {
  'use strict';

  angular
    .module('Store')
    .factory('StoreService', StoreService);

  StoreService.$inject = ['$http', 'API_SERVER', 'Upload'];

  function StoreService ($http, API_SERVER, Upload) {
    var service = {};

    service.getMerchantStores = function (merchant_id) {
      return $http.get(API_SERVER + 'api/stores/' + merchant_id + '/merchant_stores/');
    };

    service.getMerchantStore = function (store_id) {
      return $http.get(API_SERVER + 'api/stores/' + store_id + '/merchant_store/');
    };

    service.getZipcodeStores = function (data) {
      return $http.post(API_SERVER + 'api/stores/stores_in_zipcode/', data);
    };

    service.createStore = function (merchant_id, data) {
      return Upload.upload({
        url: API_SERVER + 'api/stores/' + merchant_id + '/create_store/',
        data: data
      });
    };

    service.getStore = function (store_id) {
      return $http.get(API_SERVER + 'api/stores/' + store_id + '/store/');
    };

    service.deleteStore = function (store_id) {
      return $http.post(API_SERVER + 'api/stores/' + store_id + '/delete_store/');
    };

    return service;
  }
})();
