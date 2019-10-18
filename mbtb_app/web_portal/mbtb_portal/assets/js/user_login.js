var app = angular.module("login_app",[]);
app.controller('login_controller',function($scope)
{
  $scope.user={'user_email':'','user_password':''};
  $scope.showError=false;
  $scope.showSuccess=false;

});
