/**
 * main controller
 */
(function () {
  'use strict';

  angular
    .module('app')
    .controller('MainController', MainController);

  /* @ngInject */
  function MainController(AnalysService) {
    var mainVm = this;
    mainVm.submit = submit;

    // moked API
    // mainVm.elements = {
    //     "_status": 200,
    //     'h2': 0,
    //     'h3': 0,
    //     "h1": 0,
    //     "h6": 0,
    //     "h4": 0,
    //     "h5": 0,
    //     "external_links": 0,
    //     "inaccessible_links": 0,
    //     "title": "Google",
    //     "version": "HTML5",
    //     "login-form": false,
    //     "internal_links": 0
    //   }

    function submit(){
      AnalysService.getData(mainVm.url).then(function (response) {
        console.log(response);
        mainVm.elements = response.items[0];
      });
    }
  }
})();
