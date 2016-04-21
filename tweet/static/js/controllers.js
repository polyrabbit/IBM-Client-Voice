angular.module('IBMClientVoice', ['ngRoute', 'ionic'])
    .controller("ListCtrl", ['$http', "$scope", function ($http, $scope) {
        $scope.query = {};
        $scope.query.hashtags = [];

        $scope.update_tweet = function() {
            $http.get('/api/tweets/', {
                params: $scope.query,
            }).success(function (data) {
                $scope.tweets = data.results;
            }).error(function () {
                alert("Error fetching tweet list");
            });
        }

        $scope.add_hashtag = function (tag) {
            if($scope.query.hashtags.indexOf(tag) == -1) {
                $scope.query.hashtags.push(tag);
                $scope.update_tweet();
            }
        }

        $scope.remove_hashtag = function (tag) {
            if($scope.query.hashtags.indexOf(tag) != -1) {
                $scope.query.hashtags.splice($scope.query.hashtags.indexOf(tag), 1);
                $scope.update_tweet();
            }
        }
    }])