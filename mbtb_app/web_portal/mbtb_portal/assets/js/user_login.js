var app = angular.module("login_app",[]);
app.controller('login_controller',["$scope", function($scope)
{
  $scope.user={'user_email':'','user_password':''};
}]);
