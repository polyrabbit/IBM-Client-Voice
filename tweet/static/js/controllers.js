'use strict';
angular.module('IBMClientVoice', ['ngRoute', 'ionic'])
    .config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
        $routeProvider
            .when('/tweets', {
                templateUrl: 'templates/tweet-list',
                controller: 'ListCtrl'
            })
            .when('/users/:id', {
                templateUrl: 'templates/user-detail',
                controller: 'UserDetailCtrl'
            })
            .otherwise({redirectTo: '/tweets'});

        //$locationProvider.html5Mode(true);
        //$locationProvider.hashPrefix('!');
    }])
    .controller("ListCtrl", ['$http', "$scope", function ($http, $scope) {
        $scope.query = {};
        $scope.query.hashtags = [];

        $scope.update_tweet = function () {
            $http.get('/api/tweets/', {
                params: $scope.query,
            }).success(function (data) {
                $scope.tweets = data.results;
            }).error(function () {
                alert("Error fetching tweet list");
            });
        };

        $scope.add_hashtag = function (tag) {
            if ($scope.query.hashtags.indexOf(tag) == -1) {
                $scope.query.hashtags.push(tag);
                $scope.update_tweet();
            }
        };

        $scope.remove_hashtag = function (tag) {
            if ($scope.query.hashtags.indexOf(tag) != -1) {
                $scope.query.hashtags.splice($scope.query.hashtags.indexOf(tag), 1);
                $scope.update_tweet();
            }
        };
    }])
    .controller('UserDetailCtrl', ['$http', '$scope', '$routeParams', function($http, $scope, $routeParams) {
        $http.get('/api/users/' + $routeParams.id + '/')
            .success(function (data) {
                $scope.user = data;
            }).error(function () {
                alert("Error fetching user" + $routeParams.id);
            });
    }]);