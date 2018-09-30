/**
 * Get Analyed data
 * @description
 * retrieve a list of elements in webpage
 */

(function () {
  'use strict';

  angular
    .module('app')
    .factory('AnalysService', AnalysService);

  /* @ngInject */
  function AnalysService($http, API_URL, $log) {
    return {
      getData: getData
    };

    function getData(url) {
      var url = API_URL + '/crawl.json?url=' + url + '&spider_name=analyzer';
      return $http.get(url)
        .then(GetAnalyserServiceSuccess)
        .catch(GetAnalyserServiceFailed);
    }

    function GetAnalyserServiceSuccess(response) {
      return response.data;
    }

    function GetAnalyserServiceFailed(error) {
      $log.log('error', error);
    }
  }
})();
