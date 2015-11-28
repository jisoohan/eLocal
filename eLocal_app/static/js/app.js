(function () {
  'use strict';

  angular.module('Auth', []);
  angular.module('Store', []);
  angular.module('Product', []);
  angular.module('Index', []);

  angular.module('udekApp', [
    'ui.router',
    'ui.bootstrap',
    'ngCookies',
    'ngSanitize',
    'dc.endlessScroll',
    'ngToast',
    'formly',
    'formlyBootstrap',
    'ngMap',
    'ngCart',
    'smart-table',
    'ngFileUpload',
    'Auth',
    'Store',
    'Product',
    'Index'
  ])

  .config(['$stateProvider', '$urlRouterProvider', '$httpProvider', 'ngToastProvider', function ($stateProvider, $urlRouterProvider, $httpProvider, ngToast) {

    $httpProvider.interceptors.push('AuthInterceptor');

    $urlRouterProvider.otherwise('/login');

    $stateProvider
      .state('auth', {
        url: '/login',
        templateUrl: '/static/js/auth/views/auth.html',
        controller: 'AuthController'
      })
      .state('index', {
        abstract: true,
        url: '/',
        templateUrl: '/static/js/index/views/index.html',
        controller: 'NavController'
      })
      .state('index.merchant', {
        url: 'merchant',
        templateUrl: '/static/js/index/views/index.merchant.html',
        controller: 'MerchantController'
      })
      .state('index.merchantStore', {
        url: 'merchant/store/:storeId',
        templateUrl: '/static/js/index/views/index.merchantStore.html',
        controller: 'MerchantStoreController'
      })
      .state('index.stores', {
        url: 'stores',
        templateUrl: '/static/js/index/views/index.stores.html',
        controller: 'StoresController'
      })
      .state('index.products', {
        url: 'products',
        templateUrl: '/static/js/index/views/index.products.html',
        controller: 'ProductsController'
      })
      .state('index.store', {
        url: 'store/:storeId',
        templateUrl: '/static/js/index/views/index.store.html',
        controller: 'StoreController'
      })
      .state('index.cart', {
        url: 'cart',
        templateUrl: '/static/js/index/views/index.cart.html',
        controller: 'IndexCartController'
      });

      ngToast.configure({
        maxNumber: 3
      });

  }])

  .constant('API_SERVER', 'https://elocalshops.herokuapp.com/')

  .run(['$http', function ($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }]);

})();
