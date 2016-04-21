//(function () {
//    'use strict';
//
//    angular
//        .module('IBMClientVoice')
//        .config(['$routeProvider', '$locationProvider', function config($routeProvider, $locationProvider) {
//            $locationProvider.html5Mode(true);
//            $locationProvider.hashPrefix('!');
//
//            $routeProvider.when('/register', {
//                controller: 'ListCtrl',
//                templateUrl: '/tweet-list.html'
//            }).otherwise('/');
//        }]);
//})();