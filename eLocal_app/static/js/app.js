(function () {
  'use strict';

  angular.module('Auth', []);
  angular.module('Merchant', []);
  angular.module('Store', []);
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
    'Auth',
    'Merchant',
    'Store',
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
      .state('merchant', {
        abstract: true,
        url: '/merchant',
        templateUrl: '/static/js/merchants/views/merchant.html',
        controller: 'MerchantNavController'
      })
      .state('merchant.home', {
        url: '',
        templateUrl: '/static/js/merchants/views/merchant.home.html',
        controller: 'MerchantHomeController'
      })
      .state('merchant.store', {
        url: '/store/:storeId',
        templateUrl: '/static/js/merchants/views/merchant.store.html',
        controller: 'MerchantStoreController'
      })
      .state('index', {
        abstract: true,
        url: '/',
        templateUrl: '/static/js/index/views/index.html',
        controller: 'IndexNavController'
      })
      .state('index.stores', {
        url: 'stores',
        templateUrl: '/static/js/index/views/index.stores.html',
        controller: 'IndexStoreController'
      });

      ngToast.configure({
        maxNumber: 3
      });

  }])

  .constant('API_SERVER', 'http://127.0.0.1:8000/')

  .run(['$http', function ($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }]);

})();
