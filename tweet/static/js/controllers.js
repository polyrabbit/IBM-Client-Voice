angular.module('IBMClientVoice', ['ionic'])
    .controller("ListCtrl", ['$http', "$scope", function ($http, $scope) {
        $scope.query = {};

        $scope.update_tweet = function() {
            $http.get('/api/tweets/', {
                params: $scope.query,
            }).success(function (data) {
                $scope.tweets = data.results;
            }).error(function () {
                alert("Error fetching tweet list");
            });
        }
    }])