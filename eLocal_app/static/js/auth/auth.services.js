(function () {
  'use strict';

  angular
    .module('Auth')
    .factory('AuthService', AuthService)
    .factory('AuthInterceptor', AuthInterceptor);

  AuthService.$inject = ['$http', '$q', '$window', 'API_SERVER'];

  function AuthService ($http, $q, $window, API_SERVER) {
    var service = {};

    service.register = function (data) {
      var deferred = $q.defer();
      var url = API_SERVER + 'auth/register/';
      $http.post(url, 'username=' + data.username + '&password=' + data.password + '&is_staff=' + data.is_staff,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
        function (response) {
          var token = response.data.token;
          var userId = response.data.userId;
          var username = response.data.username;
          var is_staff = response.data.is_staff;
          if (token && userId && username) {
            $window.localStorage.token = token;
            $window.localStorage.userId = userId;
            $window.localStorage.username = username;
            $window.localStorage.is_staff = is_staff;
            deferred.resolve(true);
          } else {
            deferred.reject('Not valid credentials');
          }
        },
        function (response) {
          deferred.reject(response.data.error);
        }
      );
      return deferred.promise;
    };

    service.login = function (data) {
      var deferred = $q.defer();
      var url = API_SERVER + 'auth/login/';
      $http.post(url, 'username=' + data.username + '&password=' + data.password,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
        function (response) {
          var token = response.data.token;
          var userId = response.data.userId;
          var username = response.data.username;
          var is_staff = response.data.is_staff;
          if (token && userId && username) {
            $window.localStorage.token = token;
            $window.localStorage.userId = userId;
            $window.localStorage.username = username;
            $window.localStorage.is_staff = is_staff;
            deferred.resolve(true);
          } else {
            deferred.reject('Not valid credentials');
          }
        },
        function (response) {
          deferred.reject(response.data.error);
        }
      );
      return deferred.promise;
      return authenticate(username, password, 'auth/login/');
    };

    service.logout = function () {
      var deferred = $q.defer();
      var url = API_SERVER + 'auth/logout/';

      $http.post(url).then(
        function () {
          $window.localStorage.removeItem('token');
          $window.localStorage.removeItem('username');
          $window.localStorage.removeItem('userId');
          $window.localStorage.removeItem('is_staff');
          $window.localStorage.removeItem('zipcode');
          $window.localStorage.removeItem('lat');
          $window.localStorage.removeItem('lng');
          $window.localStorage.removeItem('radius');
          deferred.resolve();
        },
        function (error) {
          deferred.reject(error.data.error);
        }
      );
      return deferred.promise;
    };

    return service;
  }

  AuthInterceptor.$inject = ['$rootScope', '$q', '$window', '$location'];
  // Change location to state later
  function AuthInterceptor ($rootScope, $q, $window, $location) {
    var service = {};

    service.request = function (config) {
      config.headers = config.headers || {};
      if ($window.localStorage.token) {
        config.headers.Authorization = 'Token ' + $window.localStorage.token;
      }
      return config;
    };

    service.responseError = function (response) {
      if (response.status == 401) {
        $window.localStorage.removeItem('token');
        $window.localStorage.removeItem('username');
        $window.localStorage.removeItem('userId');
        $window.localStorage.removeItem('is_staff');
        $location.path('/');
        return;
      }
      return $q.reject(response);
    };

    return service;
  }
})();
