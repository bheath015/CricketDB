

var app = angular.module('angularjsNodejsTutorial', []).config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('[{').endSymbol('}]');
    });;


app.service('restServices', function($http, $q) {

    var addFavPlayer = function(playerid) {

        console.log("$$$$$$$$$$$$");

        var deferred = $q.defer();
        var url = "/addFavPlayer?playerid=" + playerid;

        $.ajax({
            url: url,
            type: 'get',
            data: {},
            success: function(data) {
                console.info(data);
                deferred.resolve(data);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Status: " + textStatus);
                alert("Error: " + errorThrown);
                deferred.reject();
            }
        });
        return deferred.promise;
    };

    var getFavPlayer = function() {


        var deferred = $q.defer();
        var url = "/getFavPlayer";

        $.ajax({
            url: url,
            type: 'get',
            data: {},
            success: function(data) {
                console.info(data);
                deferred.resolve(data);
            },
            error: function(XMLHttpRequest, textStatus, errorThrown) {
                alert("Status: " + textStatus);
                alert("Error: " + errorThrown);
                deferred.reject();
            }
        });
        return deferred.promise;
    };

    

    return {
        addFavPlayer: addFavPlayer,
        getFavPlayer: getFavPlayer
    };

});

app.controller('profilePageController', function($scope, restServices, $http) {

    console.log("hello world");
    $scope.playerid = undefined;

    var favPlayer = restServices.getFavPlayer();
    favPlayer.then(function(response) {
        $scope.playerid = response.playerid;
    });

    $scope.addFavPlayer = function(pid) {
        console.log(pid);
        var re = restServices.addFavPlayer(pid);
        re.then(function(response) {
            $scope.playerid = pid;
            
        }, function(reason) {
            console.log(reason);
        });
    };

});
