var app = angular.module("app",[]);
app.controller('mycontroller',function($scope)
{
    $scope.user={'username':'','password':''};
    $scope.showError=false;
    $scope.showSuccess=false;

});