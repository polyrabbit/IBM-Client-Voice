'use strict';
angular.module('IBMClientVoice', ['ionic'])
    .config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
        $stateProvider
            .state('tweet-list', {
                url: '/tweets',
                templateUrl: 'templates/tweet-list',
                controller: 'ListCtrl'
            })
            .state('user-detail', {
                url: '/users/:id',
                templateUrl: 'templates/user-detail',
                controller: 'UserDetailCtrl'
            })

        $urlRouterProvider.otherwise('tweets');
    }])
    .controller("ListCtrl", ['$http', '$scope', function ($http, $scope) {
        $scope.query = {
            text: '',
            hashtags: []
        };

        $scope.update_tweet = function () {
            $http.get('/api/tweets/', {
                params: $scope.query
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
    .controller('UserDetailCtrl', ['$http', '$scope', '$state', '$stateParams', function($http, $scope, $state, $stateParams) {
        $http.get('/api/users/' + $stateParams.id + '/')
            .success(function (data) {
                $scope.user = data;
            }).error(function () {
                alert("Error fetching user" + $stateParams.id);
            });
    }]);