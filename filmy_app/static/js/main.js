function _C(a) {console.log(a)}
    
var filmyApp = angular.module('filmy', ['ngResource', 'ngRoute', 'ngCookies', 'ui.bootstrap']);

filmyApp.run(function ($http, $cookies) {
   $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];
});

filmyApp.directive('ngEnter', function () {
    return function (scope, element, attrs) {
        element.bind("keydown keypress", function (event) {
            if (event.which === 13) {
                scope.$apply(function (){
                    scope.$eval(attrs.ngEnter);
                });

                event.preventDefault();
            }
        });
    };
});

filmyApp.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});

filmyApp.config(function($routeProvider, $interpolateProvider) {
    $routeProvider
        .when('/', {
            controller:'MainCtrl',
            templateUrl:'static/html/main.html'
        })
        .when('/video/:id', {
            controller:'VideoCtrl',
            templateUrl:'static/html/main.html'
        })
        .when('/category/:id', {
            controller:'MainCtrl',
            templateUrl:'static/html/main.html',
        })
        .when('/video_category/:id', {
            controller:'VideoCatCtrl',
            templateUrl:'static/html/main.html',
        })
        .otherwise({
            redirectTo:'/'
        });
    /* Para solucionar conflicto entre plantillas de django y angularjs */
    $interpolateProvider.startSymbol('<%').endSymbol('%>');
})

filmyApp.factory('videoFactory', ['$resource', function($resource) {
    return $resource('/api/video/:id', {'id':'@id'}, {
    });
}]);

filmyApp.factory('categoryFactory', ['$resource', function($resource) {
    return $resource('/api/category/:id', {'id':'@id'}, {
    });
}]);

filmyApp.factory('personFactory', ['$resource', function($resource) {
    return $resource('/api/person/:id', {'id':'@id'}, {
    });
}]);

filmyApp.factory('actorFactory', ['$resource', function($resource) {
    return $resource('/api/person?is_actor=True', {}, {
    });
}]);

filmyApp.factory('directorFactory', ['$resource', function($resource) {
    return $resource('/api/person?is_director=True', {}, {
    });
}]);
    
function filter_text_multiple_html(label,field,filter_values,filter_shows,max_filters) {
    html = "<label for=\"filter_" + field + "_X\">" + label + "</label>";
    /*html += "<div ng-repeat=\"n in [] | range:max_" + field + "_filters\">";
    html += "<div ng-show=\"showInputFilter(filter_" + field + ", filter_" + field + "_show, n)\">";
    html += "<input type=\"text\" class=\"form-control\" id=\"filterform_" + field +"_<%n%>\" ng-model=\"filtermodel_" + field + "\" ng-blur=\"updateValue(filter_" + field + ",n,filtermodel_" + field + "); filtermodel_" + field + "=''\">";
    html += "<div class=\"btn glyphicon glyphicon-minus-sign pull-right icon-mag\" ng-show=\"n!=0 && !filtermodel_" + field +"\" ng-click=\"removeValue(filter_" + field + ",filter_" + field + "_show,n); filtermodel_" + field + "=''\"></div>";
    html += "</div>";
    html += "<div ng-show=\"showReadOnlyFilter(filter_" + field + ", filter_" + field + "_show, n)\">";
    html += "<span><% filter_" + field + "[n] %></span>";
    html += "<div class=\"btn glyphicon glyphicon-remove pull-right icon-mag remove\" ng-click=\"filtermodel_" + field + "=''; removeFilter(filter_" + field + ", filter_" + field + "_show, n)\"></div>";
    html += "</div>";
    html += "</div>";
    html += "<div ng-show=\"showButtonAdd(filter_" + field + ", filter_" + field + "_show)\" class=\"btn glyphicon glyphicon-plus-sign pull-right icon-mag\" ng-click=\"addFilter(filter_" + field + ", filter_" + field + "_show)\"></div>";
*/
    /*for (var i=0; i<max_filters; i++) {
        html += "<div ng-show=\"showInputFilter("+ filter_values + "," + filter_shows + "," + i + ")\">";
        html += "<input type=\"text\" class=\"form-control\" id=\"filterform_" + field + "_" + i + "\" ng-model=\"filtermodel_" + field + "\" ng-blur=\"updateValue(" + filter_values + "," + i + "," + "filtermodel_" + field + "); filtermodel_" + field + "=''\">";
        html += "<div class=\"btn glyphicon glyphicon-minus-sign pull-right icon-mag\" ng-show=\"" + i + "!=0 && !filtermodel_" + field +"\" ng-click=\"removeValue(" + filter_values + "," + filter_shows + "," + i + "); filtermodel_" + field + "=''\"></div>";
        html += "</div>";
    }

    if (max_filters != 0) {
	html += "<div ng-show=\"showButtonAdd(" + filter_values + "," + filter_shows +")\" class=\"btn glyphicon glyphicon-plus-sign pull-right icon-mag\" ng-click=\"addFilter(" + filter_values + "," + filter_shows + ")\"></div>"; 
    }*/

    return html;
};


filmyApp.controller('MainCtrl', ['$scope', '$sce', '$routeParams', 'videoFactory', 'categoryFactory', 'actorFactory', 'directorFactory',  
                         function($scope, $sce, $routeParams, videoFactory, categoryFactory, actorFactory, directorFactory) {
    $scope.videos = videoFactory.query();
    $scope.categories = categoryFactory.query();
    $scope.actors = actorFactory.query();
    $scope.directors = directorFactory.query();

    $scope.filter_title = '';

    $scope.filter_director = '';

    $scope.filter_nationality = '';

    $scope.max_cast_filters = 3;
    $scope.filter_cast = [];
    $scope.filter_cast_show = [1];

    /*$scope.filter_cast_html = function() {
        return $sce.trustAsHtml(filter_text_multiple_html("Cast","cast",$scope.filter_cast,$scope.filter_cast_show,$scope.max_cast_filters));
    }*/

    $scope.showReadOnlyFilter = function(values,shows,pos) {
        for (var i=0; i<=pos;i++) {
            if (i==pos && values[i] && shows[i]) return 1
            else if (values[i] && shows[i]) continue
            else return 0
        }
        return 0
    };
    
    $scope.showInputFilter = function(values,shows,pos) {
        for (var i=0; i<=pos;i++) {
            if (values[i] && shows[i]) continue
            else if (i==pos && !values[i] && shows[i]) return 1
            else return 0
        }
        return 0
    };
    
    $scope.showButtonAdd = function(values,shows) {
        num_showed_filters = 0;
	for (var i=0; i<shows.length;i++)
            if (shows[i] == 1) num_showed_filters++
        if ($scope.max_cast_filters == num_showed_filters) return 0
        for (var pos=0; pos<$scope.max_cast_filters;pos++)
            if (shows[pos] && !values[pos]) return 0
        return 1
    };
    
    $scope.addFilter = function(values,shows) {
        for (var pos=0; pos<$scope.max_cast_filters;pos++) {
            if (!shows[pos]) {
	        shows[pos] = 1;
                values[pos] = '';
                break;
            }
        }
    };
    
    $scope.removeFilter = function(values,shows,pos) {
        var i = $scope.max_cast_filters;
        for (i=pos; i<$scope.max_cast_filters-1;i++) {
	    shows[i] = shows[i+1];
            values[i] = values[i+1];
        }
        shows[i] = 0;
        values[i] = '';
        shows[0] = 1;
    };
    
    $scope.updateValue = function(values,pos,value) {
	values[pos]=value;
    };

    $scope.removeValue = function(values,shows,pos) {
	shows[pos]=0; 
        values[pos]='';
    }; 

}]);

filmyApp.controller('VideoCtrl', ['$scope', '$routeParams', 'videoFactory', 'categoryFactory', function($scope, $routeParams, videoFactory, categoryFactory) {
    $scope.videos = videoFactory.query();
    $scope.categories = categoryFactory.query();
}]);

filmyApp.controller('VideoCatCtrl', ['$scope', '$routeParams', '$location', 'videoFactory', 'categoryFactory', function($scope, $routeParams, $location, videoFactory, categoryFactory) {
    $scope.videos = videoFactory.query({category:$routeParams.id});
    console.log($scope.videos);
    $scope.categories = categoryFactory.query();

    $scope.getCategoryClass = function(category_id) {
        var path_divided = $location.path().split("/"); 
        if (path_divided[2] == category_id) {
      	    return "activef"
    	} else {
            return ""
        }
    }
}]);
