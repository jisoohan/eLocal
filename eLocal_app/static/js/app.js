(function () {
  'use strict';

  angular.module('Auth', []);

  angular.module('udekApp', [
    'ui.router',
    'ui.bootstrap',
    'ngCookies',
    'ngSanitize',
    'dc.endlessScroll',
    'ngToast',
    'Auth'
  ])

  .config(['$stateProvider', '$urlRouterProvider', '$httpProvider', 'ngToastProvider', function ($stateProvider, $urlRouterProvider, $httpProvider, ngToast) {

    $httpProvider.interceptors.push('AuthInterceptor');

    $urlRouterProvider.otherwise('/login');

    $stateProvider
      .state('auth', {
        url: '/login',
        templateUrl: '/static/js/auth/views/auth.html',
        controller: 'AuthController'
      });

      ngToast.configure({
        maxNumber: 3
      });

  }])

  .constant('API_SERVER', 'http://127.0.0.1:8000/')

  .run(['$http', function ($http) {
    $http.defaults.xsrfHeaderName = 'X-CSRFToken';
    $http.defaults.xsrfCookieName = 'csrftoken';
  }])

  .controller('IndexController', IndexController);

  IndexController.$inject = ['$scope', '$window', '$state', 'ngToast', 'AuthService'];

  function IndexController ($scope, $window, $state, ngToast, AuthService) {
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

})();
