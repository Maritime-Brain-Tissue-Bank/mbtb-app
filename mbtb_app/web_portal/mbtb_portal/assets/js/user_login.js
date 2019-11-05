var user_login = angular.module('login_app',[]);

user_login.controller('login_controller',['$scope', function($scope)
{
  $scope.user={
    'user_email': '',
    'user_password':''
  };
}]);
