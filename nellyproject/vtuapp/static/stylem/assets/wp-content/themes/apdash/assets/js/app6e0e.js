/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/app.js":
/*!***********************!*\
  !*** ./src/js/app.js ***!
  \***********************/
/*! no static exports found */
/***/ (function(module, exports) {

var THEMETAGS = THEMETAGS || {};

(function ($) {
  /*!----------------------------------------------
      # This beautiful code written with heart
      # by Mominul Islam <hello@mominul.me>
      # In Dhaka, BD at the ThemeTags workstation.
      ---------------------------------------------*/
  // USE STRICT
  "use strict";

  window.TT = {
    init: function init() {
      // Header
      this.header = $('.site-header');
      this.body = $('body');
      this.wpadminbar = $('#wpadminbar');
      this.headerFixed = {
        initialOffset: parseInt(this.header.attr('data-fixed-initial-offset')) || 100,
        enabled: $('[data-header-fixed]').length,
        value: false,
        mobileEnabled: $('[data-mobile-header-fixed]').length,
        mobileValue: false
      }; // Logos

      this.siteBranding = this.header.find('.site-branding');
      this.siteTitle = this.header.find('.site-title');
      this.logo = this.header.find('.main-logo');
      this.fixedLogo = this.header.find('.logo-sticky');
      this.mobileLogo = this.header.find('.mobile-logo');
      this.fixedMobileLogo = this.header.find('.fixed-mobile-logo');
      this.logoForOnepage = this.header.find('.for-onepage');
      this.logoForOnepageDark = this.logoForOnepage.find('.dark');
      this.logoForOnepageLight = this.logoForOnepage.find('.light'); // Menus

      this.megaMenu = this.header.find('#mega-menu-wrap');
      this.mobileMenu = $('[data-mobile-menu-resolution]').data('mobile-menu-resolution');
      this.resize();
    },
    resize: function resize() {
      this.isDesktop = $(window).width() >= 991;
      this.isMobile = $(window).width() <= 991;
      this.isPad = $(window).width() <= 1024;
      this.isMobileMenu = $(window).width() <= TT.mobileMenu;
    }
  };
  THEMETAGS.initialize = {
    init: function init() {
      THEMETAGS.initialize.general();
      THEMETAGS.initialize.domainSearch();
      THEMETAGS.initialize.swiperSlider();
      THEMETAGS.initialize.sidebarMenu();
      THEMETAGS.initialize.countUp();
      THEMETAGS.initialize.countDown();
      THEMETAGS.initialize.sectionSwitch();
      THEMETAGS.initialize.googleMap();
      THEMETAGS.initialize.contactFrom();
      THEMETAGS.initialize.handleMobileHeader();
    },

    /*========================================================*/

    /*=           Collection of snippet and tweaks           =*/

    /*========================================================*/
    general: function general() {
      if ($('body').hasClass("admin-bar")) {
        $('body').addClass('header-position');
      } // Init Wow Js


      var wow = new WOW({
        boxClass: 'wow',
        animateClass: 'animated',
        offset: 0,
        mobile: false,
        live: true,
        scrollContainer: null
      });
      wow.init(); // Pricing Switcher

      $('#js-contcheckbox').change(function () {
        if (this.checked) {
          $('.monthly-price').css('display', 'none');
          $('.yearly-price').css('display', 'block');
          $('.pricing-switch-wrap').addClass('yearly');
          $('.pricing-switch-wrap').removeClass('monthly');
          $('.afterinput').addClass('active');
          $('.beforeinput').removeClass('active');
        } else {
          $('.monthly-price').css('display', 'block');
          $('.yearly-price').css('display', 'none');
          $('.pricing-switch-wrap').removeClass('yearly');
          $('.pricing-switch-wrap').addClass('monthly');
          $('.afterinput').removeClass('active');
          $('.beforeinput').addClass('active');
        }
      });

      if ($("#wpadminbar").length && $(window).width() < 768) {
        $("#wpadminbar").css({
          position: "fixed",
          top: "0"
        });
      }

      var blogContainer = $(".blog-masonry");
      blogContainer.masonry({
        itemSelector: '.post-item',
        percentPosition: true
      });
      /* Magnefic Popup */

      $('.popup-video').each(function () {
        $('.popup-video').magnificPopup({
          type: 'iframe'
        });
      });
    },

    /*====================================*/

    /*=           Sidebar Menu          =*/

    /*===================================*/
    sidebarMenu: function sidebarMenu() {
      var $popup = $('.canvas-menu-wrapper');
      $("#page-open-main-menu").on('click', function (e) {
        e.preventDefault();
        var mask = '<div class="mask-overlay">';
        $(mask).hide().appendTo('body').fadeIn('fast');
        $popup.addClass('open');
        $(".tt-hamburger").addClass('active');
        $("html").addClass("no-scroll sidebar-open").height(window.innerHeight + "px");
      });
      $("#page-close-main-menu, .main-nav-container li a").on('click', function (e) {
        $('.mask-overlay').remove();
        $popup.removeClass('open');
        $(".tt-hamburger").removeClass('active');
        $("html").removeClass("no-scroll sidebar-open").height("auto");
      });
    },

    /*===========================================*/

    /*=           handle Mobile Header          =*/

    /*===========================================*/
    handleMobileHeader: function handleMobileHeader() {
      if (TT.header && TT.header.length) {
        if (TT.isMobileMenu) {
          TT.header.addClass('mobile-header');
          TT.body.addClass('is-mobile-menu');
          setTimeout(function () {
            $('.main-nav').addClass('unhidden');
          }, 300);
        } else {
          TT.header.removeClass('mobile-header');
          TT.body.removeClass('is-mobile-menu');
          $('.main-nav').addClass('visible');
        }
      }
    },

    /*==========================================*/

    /*=           handle Fixed Header          =*/

    /*==========================================*/
    handleFixedHeader: function handleFixedHeader() {
      // TT.init();
      var fixed = TT.headerFixed;

      if ($(document).scrollTop() > fixed.initialOffset) {
        if (!TT.isMobileMenu && fixed.enabled && !fixed.value || TT.isMobileMenu && fixed.mobileEnabled && !fixed.mobileValue) {
          if (TT.isMobileMenu) {
            fixed.mobileValue = true;
          } else {
            fixed.value = true;
          }

          TT.header.addClass('header-fixed no-transition');
        }
      } else if (fixed.value || fixed.mobileValue) {
        fixed.value = false;
        fixed.mobileValue = false;
        TT.header.removeClass('header-fixed');
      } // Effect appearance


      if ($(document).scrollTop() > fixed.initialOffset + 50) {
        TT.header.removeClass('no-transition').addClass('showed');
      } else {
        TT.header.removeClass('showed').addClass('no-transition');
      }
    },

    /*===========================*/

    /*=           Blog          =*/

    /*===========================*/
    domainSearch: function domainSearch() {
      /* Domain Check */
      var DomainCheck = {
        submit: function submit(e) {
          e.preventDefault();
          var obj = e.data,
              el = obj.wap.find("#tt-domain-results"),
              domainDefault = "themetags.com",
              basename = obj.input.val() !== "" ? obj.input.val() : domainDefault,
              ext = obj.select.val() !== "" ? obj.select.val() : '',
              whmcs_url = obj.whmcs_url.val() !== "" ? obj.whmcs_url.val() : '',
              transferUrl = obj.transferUrl.val() !== "" ? obj.transferUrl.val() : '',
              domainSearchOption = obj.domainSearchOption.val() !== "" ? obj.domainSearchOption.val() : '',
              extension = DomainCheck.dotExt(obj.input.val());
          var domainName = "";

          if (basename.indexOf('.') > -1) {
            domainName = basename;
          } else if (basename.indexOf('.') == -1) {
            domainName = basename + (ext ? '.' + ext : '.com');
          }

          obj.security = obj.form.find("input[name=security]").val();
          obj.el = el;
          var domainData = {},
              domainResultTable = $('<div id="tt_result_item" class="tt-result-domain-box" role="alert"> </div></div>'),
              domainResult = $('<div class="inner-block-result-item">' + '<div class="spinner tt-loading-results text-center">' + '<i class="fas fa-spinner fa-spin fa-lg fa-fw"></i>' + '<span> Seaching...</span>' + '<span class="sr-only">...</span>' + "</div>");
          $.extend(domainData, obj);
          domainData.domain = domainName;
          domainData.extension = extension;
          domainData.whmcs_url = whmcs_url;
          domainData.transferUrl = transferUrl;
          domainData.el = domainResult;
          domainData.domainSearchOption = domainSearchOption;
          domainResult.data("domain", domainData.domain);

          if (obj.el.find("#tt_result_item").length == 0) {
            obj.el.append(domainResultTable);
            obj.el.find("#tt_result_item").append(domainResult);
          } else {
            obj.el.find("#tt_result_item").remove();
            obj.el.append(domainResultTable);
            obj.el.find("#tt_result_item").append(domainResult);
          }

          DomainCheck.checkAjax(domainData);
        },
        name: function name(domain) {
          return domain.replace(/^.*\/|\.[^.]*$/g, "");
        },
        dotExt: function dotExt(ext) {
          var fExt,
              tExt = ext.split(".", 3);

          if (tExt[1] === undefined) {
            fExt = "com";
          } else if (tExt[0] === "www") {
            fExt = tExt[2];
          } else {
            fExt = tExt[1];
          }

          return fExt;
        },
        checkAjax: function checkAjax(obj) {
          var data = {
            domain: obj.domain,
            whmcs_url: obj.whmcs_url,
            transferUrl: obj.transferUrl,
            domain_search_option: obj.domainSearchOption,
            action: "tt_ajax_search_domain",
            security: obj.security
          };
          $.ajax({
            url: tt_ajax_url,
            type: "POST",
            dataType: "json",
            data: data,
            success: function success(data) {
              obj.el.find(".spinner").remove();
              obj.el.append(data.results_html);
            },
            error: function error(xhr, ajaxOptions, thrownError) {
              console.log(xhr);
              console.log(thrownError);
            }
          });
        }
      };
      $("#tt-domain-search").is(function () {
        var id = $(this),
            submitEl = id.find("#tt-search"),
            inputEl = id.find("#tt-domain"),
            selectEl = id.find("#domainext"),
            formEl = id.find("#tt-domain-form"),
            acEl = id.find('input[name="whmcs_url"]'),
            transferUrl = id.find('input[name="whmcs_transfer_url"]'),
            domainSearchOption = id.find('input[name="domain_search_option"]'),
            data;
        data = {
          submit: submitEl,
          input: inputEl,
          select: selectEl,
          whmcs_url: acEl,
          transferUrl: transferUrl,
          form: formEl,
          div: id,
          wap: id,
          domainSearchOption: domainSearchOption
        };
        submitEl.attr("disabled", true);
        inputEl.keyup(function () {
          if ($(this).val().length != 0) submitEl.attr("disabled", false);else submitEl.attr("disabled", true);
        });
        submitEl.on("click", data, DomainCheck.submit);
      }); // Loading Screen

      var loadingClass = $(".loading"),
          removeFLow = $("html,body").css("overflow", "auto");

      if (loadingClass.length === 1) {
        $(window).on("load", function () {
          loadingClass.fadeOut();
          removeFLow;
        });
      }
    },

    /*====================================*/

    /*=           Swiper Slider          =*/

    /*====================================*/
    swiperSlider: function swiperSlider() {
      $('#portfolio-testimonial').each(function () {
        var swiper = new Swiper('#portfolio-testimonial', {
          slidesPerView: 1,
          spaceBetween: 30,
          loop: true,
          speed: 800,
          autoplay: {
            delay: 5000
          },
          navigation: {
            nextEl: '.testi-button-next',
            prevEl: '.testi-button-prev'
          }
        });
      });
      $('.related-product').each(function () {
        var swiper = new Swiper('.related-product', {
          slidesPerView: 3,
          spaceBetween: 30,
          loop: true,
          speed: 800,
          autoplay: {
            delay: 2000
          },
          navigation: {
            nextEl: '.product-button-next',
            prevEl: '.product-button-prev'
          }
        });
      });
    },

    /*=====================================*/

    /*=           Section Switch          =*/

    /*=====================================*/
    sectionSwitch: function sectionSwitch() {
      $('.page-scroll, .site-header .menu li a').on('click', function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
          var target = $(this.hash);

          if (target.length > 0) {
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            $('html,body').animate({
              scrollTop: target.offset().top - 130
            }, 1000);
            return false;
          }
        }
      });
    },

    /*==============================*/

    /*=           Countup          =*/

    /*==============================*/
    countUp: function countUp() {
      var options = {
        useEasing: true,
        useGrouping: true,
        separator: ',',
        decimal: '.',
        prefix: '',
        suffix: ''
      };
      var counteEl = $('[data-counter]');

      if (counteEl) {
        counteEl.each(function () {
          var val = $(this).data('counter');
          var countup = new CountUp(this, 0, val, 0, 2.5, options);
          $(this).appear(function () {
            countup.start();
          }, {
            accX: 0,
            accY: 0
          });
        });
      }
    },

    /*=================================*/

    /*=           Countdown          =*/

    /*=================================*/
    countDown: function countDown() {
      if ($('.countdown').length > 0) {
        $('.countdown').each(function (index, value) {
          var count_year = $(this).data("count-year");
          var count_month = $(this).data("count-month");
          var count_day = $(this).data("count-day");
          var count_date = count_year + '/' + count_month + '/' + count_day;
          $(this).countdown(count_date, function (event) {
            $(this).html(event.strftime('<div class="counting"><span class="CountdownContent">%D<span class="CountdownLabel">Days</span></span></div><div class="counting"><span class="CountdownContent">%H <span class="CountdownLabel">Hours</span></span></div><div class="counting"><span class="CountdownContent">%M <span class="CountdownLabel">Minutes</span></span></div><div class="counting"><span class="CountdownContent">%S <span class="CountdownLabel">Seconds</span></span></div>'));
          });
        });
      }
    },

    /*=================================*/

    /*=           Google Map          =*/

    /*=================================*/
    googleMap: function googleMap() {
      $('.gmap3-area').each(function () {
        var $this = $(this),
            key = $this.data('key'),
            lat = $this.data('lat'),
            lng = $this.data('lng'),
            mrkr = $this.data('mrkr'),
            zoom = $this.data('zoom'),
            scrollwheel = $this.data('scrollwheel') || false;
        $this.gmap3({
          center: [lat, lng],
          zoom: zoom,
          scrollwheel: scrollwheel,
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          styles: [{
            "featureType": "administrative.country",
            "elementType": "geometry.fill",
            "stylers": [{
              "visibility": "on"
            }]
          }]
        }).marker(function (map) {
          return {
            position: map.getCenter(),
            icon: mrkr
          };
        });
      });
    },

    /*===========================*/

    /*=           Form          =*/

    /*===========================*/
    contactFrom: function contactFrom() {
      $('[data-apdash-form]').each(function () {
        var $this = $(this);
        $('.form-result', $this).css('display', 'none');
        $this.submit(function () {
          $('button[type="submit"]', $this).addClass('clicked'); // Create a object and assign all fields name and value.

          var values = {};
          $('[name]', $this).each(function () {
            var $this = $(this),
                $name = $this.attr('name'),
                $value = $this.val();
            values[$name] = $value;
          }); // Make Request

          $.ajax({
            url: $this.attr('action'),
            type: 'POST',
            data: values,
            success: function success(data) {
              if (data.error == true) {
                $('.form-result', $this).addClass('alert-warning').removeClass('alert-success alert-danger').css('display', 'block');
              } else {
                $('.form-result', $this).addClass('alert-success').removeClass('alert-warning alert-danger').css('display', 'block');
              }

              $('.form-result > .content', $this).html(data.message);
              $('button[type="submit"]', $this).removeClass('clicked');
              console.log("Success");
            },
            error: function error() {
              $('.form-result', $this).addClass('alert-danger').removeClass('alert-warning alert-success').css('display', 'block');
              $('.form-result > .content', $this).html('Sorry, an error occurred.');
              $('button[type="submit"]', $this).removeClass('clicked');
              console.log("Error");
            }
          });
          return false;
        });
      });
    }
  };
  THEMETAGS.documentOnReady = {
    init: function init() {
      THEMETAGS.initialize.init();
    }
  };
  THEMETAGS.documentOnLoad = {
    init: function init() {
      THEMETAGS.initialize.handleMobileHeader();
      $("#preloader").fadeOut("slow");
    }
  };
  THEMETAGS.documentOnResize = {
    init: function init() {
      if ($("#wpadminbar").length && $(window).width() < 768) {
        $("#wpadminbar").css({
          position: "fixed",
          top: "0"
        });
      }

      TT.resize();
      THEMETAGS.initialize.handleMobileHeader();
      THEMETAGS.initialize.handleFixedHeader();
    }
  };
  THEMETAGS.documentOnScroll = {
    init: function init() {
      THEMETAGS.initialize.handleFixedHeader();
    }
  };
  TT.init(); // Initialize Functions

  $(document).ready(THEMETAGS.documentOnReady.init);
  $(window).on('load', THEMETAGS.documentOnLoad.init);
  $(window).on('resize', THEMETAGS.documentOnResize.init);
  $(window).on('scroll', THEMETAGS.documentOnScroll.init);
})(jQuery);

/***/ }),

/***/ 0:
/*!*****************************!*\
  !*** multi ./src/js/app.js ***!
  \*****************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /Volumes/Development/Sites/apdash/wp-content/themes/apdash/src/js/app.js */"./src/js/app.js");


/***/ })

/******/ });
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vd2VicGFjay9ib290c3RyYXAiLCJ3ZWJwYWNrOi8vLy4vc3JjL2pzL2FwcC5qcyJdLCJuYW1lcyI6WyJUSEVNRVRBR1MiLCIkIiwid2luZG93IiwiVFQiLCJpbml0IiwiaGVhZGVyIiwiYm9keSIsIndwYWRtaW5iYXIiLCJoZWFkZXJGaXhlZCIsImluaXRpYWxPZmZzZXQiLCJwYXJzZUludCIsImF0dHIiLCJlbmFibGVkIiwibGVuZ3RoIiwidmFsdWUiLCJtb2JpbGVFbmFibGVkIiwibW9iaWxlVmFsdWUiLCJzaXRlQnJhbmRpbmciLCJmaW5kIiwic2l0ZVRpdGxlIiwibG9nbyIsImZpeGVkTG9nbyIsIm1vYmlsZUxvZ28iLCJmaXhlZE1vYmlsZUxvZ28iLCJsb2dvRm9yT25lcGFnZSIsImxvZ29Gb3JPbmVwYWdlRGFyayIsImxvZ29Gb3JPbmVwYWdlTGlnaHQiLCJtZWdhTWVudSIsIm1vYmlsZU1lbnUiLCJkYXRhIiwicmVzaXplIiwiaXNEZXNrdG9wIiwid2lkdGgiLCJpc01vYmlsZSIsImlzUGFkIiwiaXNNb2JpbGVNZW51IiwiaW5pdGlhbGl6ZSIsImdlbmVyYWwiLCJkb21haW5TZWFyY2giLCJzd2lwZXJTbGlkZXIiLCJzaWRlYmFyTWVudSIsImNvdW50VXAiLCJjb3VudERvd24iLCJzZWN0aW9uU3dpdGNoIiwiZ29vZ2xlTWFwIiwiY29udGFjdEZyb20iLCJoYW5kbGVNb2JpbGVIZWFkZXIiLCJoYXNDbGFzcyIsImFkZENsYXNzIiwid293IiwiV09XIiwiYm94Q2xhc3MiLCJhbmltYXRlQ2xhc3MiLCJvZmZzZXQiLCJtb2JpbGUiLCJsaXZlIiwic2Nyb2xsQ29udGFpbmVyIiwiY2hhbmdlIiwiY2hlY2tlZCIsImNzcyIsInJlbW92ZUNsYXNzIiwicG9zaXRpb24iLCJ0b3AiLCJibG9nQ29udGFpbmVyIiwibWFzb25yeSIsIml0ZW1TZWxlY3RvciIsInBlcmNlbnRQb3NpdGlvbiIsImVhY2giLCJtYWduaWZpY1BvcHVwIiwidHlwZSIsIiRwb3B1cCIsIm9uIiwiZSIsInByZXZlbnREZWZhdWx0IiwibWFzayIsImhpZGUiLCJhcHBlbmRUbyIsImZhZGVJbiIsImhlaWdodCIsImlubmVySGVpZ2h0IiwicmVtb3ZlIiwic2V0VGltZW91dCIsImhhbmRsZUZpeGVkSGVhZGVyIiwiZml4ZWQiLCJkb2N1bWVudCIsInNjcm9sbFRvcCIsIkRvbWFpbkNoZWNrIiwic3VibWl0Iiwib2JqIiwiZWwiLCJ3YXAiLCJkb21haW5EZWZhdWx0IiwiYmFzZW5hbWUiLCJpbnB1dCIsInZhbCIsImV4dCIsInNlbGVjdCIsIndobWNzX3VybCIsInRyYW5zZmVyVXJsIiwiZG9tYWluU2VhcmNoT3B0aW9uIiwiZXh0ZW5zaW9uIiwiZG90RXh0IiwiZG9tYWluTmFtZSIsImluZGV4T2YiLCJzZWN1cml0eSIsImZvcm0iLCJkb21haW5EYXRhIiwiZG9tYWluUmVzdWx0VGFibGUiLCJkb21haW5SZXN1bHQiLCJleHRlbmQiLCJkb21haW4iLCJhcHBlbmQiLCJjaGVja0FqYXgiLCJuYW1lIiwicmVwbGFjZSIsImZFeHQiLCJ0RXh0Iiwic3BsaXQiLCJ1bmRlZmluZWQiLCJkb21haW5fc2VhcmNoX29wdGlvbiIsImFjdGlvbiIsImFqYXgiLCJ1cmwiLCJ0dF9hamF4X3VybCIsImRhdGFUeXBlIiwic3VjY2VzcyIsInJlc3VsdHNfaHRtbCIsImVycm9yIiwieGhyIiwiYWpheE9wdGlvbnMiLCJ0aHJvd25FcnJvciIsImNvbnNvbGUiLCJsb2ciLCJpcyIsImlkIiwic3VibWl0RWwiLCJpbnB1dEVsIiwic2VsZWN0RWwiLCJmb3JtRWwiLCJhY0VsIiwiZGl2Iiwia2V5dXAiLCJsb2FkaW5nQ2xhc3MiLCJyZW1vdmVGTG93IiwiZmFkZU91dCIsInN3aXBlciIsIlN3aXBlciIsInNsaWRlc1BlclZpZXciLCJzcGFjZUJldHdlZW4iLCJsb29wIiwic3BlZWQiLCJhdXRvcGxheSIsImRlbGF5IiwibmF2aWdhdGlvbiIsIm5leHRFbCIsInByZXZFbCIsImxvY2F0aW9uIiwicGF0aG5hbWUiLCJob3N0bmFtZSIsInRhcmdldCIsImhhc2giLCJzbGljZSIsImFuaW1hdGUiLCJvcHRpb25zIiwidXNlRWFzaW5nIiwidXNlR3JvdXBpbmciLCJzZXBhcmF0b3IiLCJkZWNpbWFsIiwicHJlZml4Iiwic3VmZml4IiwiY291bnRlRWwiLCJjb3VudHVwIiwiQ291bnRVcCIsImFwcGVhciIsInN0YXJ0IiwiYWNjWCIsImFjY1kiLCJpbmRleCIsImNvdW50X3llYXIiLCJjb3VudF9tb250aCIsImNvdW50X2RheSIsImNvdW50X2RhdGUiLCJjb3VudGRvd24iLCJldmVudCIsImh0bWwiLCJzdHJmdGltZSIsIiR0aGlzIiwia2V5IiwibGF0IiwibG5nIiwibXJrciIsInpvb20iLCJzY3JvbGx3aGVlbCIsImdtYXAzIiwiY2VudGVyIiwibWFwVHlwZUlkIiwiZ29vZ2xlIiwibWFwcyIsIk1hcFR5cGVJZCIsIlJPQURNQVAiLCJzdHlsZXMiLCJtYXJrZXIiLCJtYXAiLCJnZXRDZW50ZXIiLCJpY29uIiwidmFsdWVzIiwiJG5hbWUiLCIkdmFsdWUiLCJtZXNzYWdlIiwiZG9jdW1lbnRPblJlYWR5IiwiZG9jdW1lbnRPbkxvYWQiLCJkb2N1bWVudE9uUmVzaXplIiwiZG9jdW1lbnRPblNjcm9sbCIsInJlYWR5IiwialF1ZXJ5Il0sIm1hcHBpbmdzIjoiO1FBQUE7UUFDQTs7UUFFQTtRQUNBOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBOztRQUVBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7OztRQUdBO1FBQ0E7O1FBRUE7UUFDQTs7UUFFQTtRQUNBO1FBQ0E7UUFDQSwwQ0FBMEMsZ0NBQWdDO1FBQzFFO1FBQ0E7O1FBRUE7UUFDQTtRQUNBO1FBQ0Esd0RBQXdELGtCQUFrQjtRQUMxRTtRQUNBLGlEQUFpRCxjQUFjO1FBQy9EOztRQUVBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQTtRQUNBO1FBQ0E7UUFDQSx5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LENBQXFCVSxrQkFBckI7QUFDQTlDLGVBQVMsQ0FBQ29DLFVBQVYsQ0FBcUI4QyxpQkFBckI7QUFDSDtBQVh3QixHQUE3QjtBQWNBbEYsV0FBUyxDQUFDb04sZ0JBQVYsR0FBNkI7QUFDekJoTixRQUFJLEVBQUUsZ0JBQVk7QUFDZEosZUFBUyxDQUFDb0MsVUFBVixDQUFxQjhDLGlCQUFyQjtBQUNIO0FBSHdCLEdBQTdCO0FBS0EvRSxJQUFFLENBQUNDLElBQUgsR0E1bEJVLENBNmxCVjs7QUFDQUgsR0FBQyxDQUFDbUYsUUFBRCxDQUFELENBQVlpSSxLQUFaLENBQWtCck4sU0FBUyxDQUFDaU4sZUFBVixDQUEwQjdNLElBQTVDO0FBQ0FILEdBQUMsQ0FBQ0MsTUFBRCxDQUFELENBQVVxRSxFQUFWLENBQWEsTUFBYixFQUFxQnZFLFNBQVMsQ0FBQ2tOLGNBQVYsQ0FBeUI5TSxJQUE5QztBQUNBSCxHQUFDLENBQUNDLE1BQUQsQ0FBRCxDQUFVcUUsRUFBVixDQUFhLFFBQWIsRUFBdUJ2RSxTQUFTLENBQUNtTixnQkFBVixDQUEyQi9NLElBQWxEO0FBQ0FILEdBQUMsQ0FBQ0MsTUFBRCxDQUFELENBQVVxRSxFQUFWLENBQWEsUUFBYixFQUF1QnZFLFNBQVMsQ0FBQ29OLGdCQUFWLENBQTJCaE4sSUFBbEQ7QUFFSCxDQW5tQkQsRUFtbUJHa04sTUFubUJILEUiLCJmaWxlIjoiYXBwLmpzIiwic291cmNlc0NvbnRlbnQiOlsiIFx0Ly8gVGhlIG1vZHVsZSBjYWNoZVxuIFx0dmFyIGluc3RhbGxlZE1vZHVsZXMgPSB7fTtcblxuIFx0Ly8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbiBcdGZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblxuIFx0XHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcbiBcdFx0aWYoaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0pIHtcbiBcdFx0XHRyZXR1cm4gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0uZXhwb3J0cztcbiBcdFx0fVxuIFx0XHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuIFx0XHR2YXIgbW9kdWxlID0gaW5zdGFsbGVkTW9kdWxlc1ttb2R1bGVJZF0gPSB7XG4gXHRcdFx0aTogbW9kdWxlSWQsXG4gXHRcdFx0bDogZmFsc2UsXG4gXHRcdFx0ZXhwb3J0czoge31cbiBcdFx0fTtcblxuIFx0XHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cbiBcdFx0bW9kdWxlc1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cbiBcdFx0Ly8gRmxhZyB0aGUgbW9kdWxlIGFzIGxvYWRlZFxuIFx0XHRtb2R1bGUubCA9IHRydWU7XG5cbiBcdFx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcbiBcdFx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xuIFx0fVxuXG5cbiBcdC8vIGV4cG9zZSB0aGUgbW9kdWxlcyBvYmplY3QgKF9fd2VicGFja19tb2R1bGVzX18pXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLm0gPSBtb2R1bGVzO1xuXG4gXHQvLyBleHBvc2UgdGhlIG1vZHVsZSBjYWNoZVxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5jID0gaW5zdGFsbGVkTW9kdWxlcztcblxuIFx0Ly8gZGVmaW5lIGdldHRlciBmdW5jdGlvbiBmb3IgaGFybW9ueSBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLmQgPSBmdW5jdGlvbihleHBvcnRzLCBuYW1lLCBnZXR0ZXIpIHtcbiBcdFx0aWYoIV9fd2VicGFja19yZXF1aXJlX18ubyhleHBvcnRzLCBuYW1lKSkge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBuYW1lLCB7IGVudW1lcmFibGU6IHRydWUsIGdldDogZ2V0dGVyIH0pO1xuIFx0XHR9XG4gXHR9O1xuXG4gXHQvLyBkZWZpbmUgX19lc01vZHVsZSBvbiBleHBvcnRzXG4gXHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIgPSBmdW5jdGlvbihleHBvcnRzKSB7XG4gXHRcdGlmKHR5cGVvZiBTeW1ib2wgIT09ICd1bmRlZmluZWQnICYmIFN5bWJvbC50b1N0cmluZ1RhZykge1xuIFx0XHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCBTeW1ib2wudG9TdHJpbmdUYWcsIHsgdmFsdWU6ICdNb2R1bGUnIH0pO1xuIFx0XHR9XG4gXHRcdE9iamVjdC5kZWZpbmVQcm9wZXJ0eShleHBvcnRzLCAnX19lc01vZHVsZScsIHsgdmFsdWU6IHRydWUgfSk7XG4gXHR9O1xuXG4gXHQvLyBjcmVhdGUgYSBmYWtlIG5hbWVzcGFjZSBvYmplY3RcbiBcdC8vIG1vZGUgJiAxOiB2YWx1ZSBpcyBhIG1vZHVsZSBpZCwgcmVxdWlyZSBpdFxuIFx0Ly8gbW9kZSAmIDI6IG1lcmdlIGFsbCBwcm9wZXJ0aWVzIG9mIHZhbHVlIGludG8gdGhlIG5zXG4gXHQvLyBtb2RlICYgNDogcmV0dXJuIHZhbHVlIHdoZW4gYWxyZWFkeSBucyBvYmplY3RcbiBcdC8vIG1vZGUgJiA4fDE6IGJlaGF2ZSBsaWtlIHJlcXVpcmVcbiBcdF9fd2VicGFja19yZXF1aXJlX18udCA9IGZ1bmN0aW9uKHZhbHVlLCBtb2RlKSB7XG4gXHRcdGlmKG1vZGUgJiAxKSB2YWx1ZSA9IF9fd2VicGFja19yZXF1aXJlX18odmFsdWUpO1xuIFx0XHRpZihtb2RlICYgOCkgcmV0dXJuIHZhbHVlO1xuIFx0XHRpZigobW9kZSAmIDQpICYmIHR5cGVvZiB2YWx1ZSA9PT0gJ29iamVjdCcgJiYgdmFsdWUgJiYgdmFsdWUuX19lc01vZHVsZSkgcmV0dXJuIHZhbHVlO1xuIFx0XHR2YXIgbnMgPSBPYmplY3QuY3JlYXRlKG51bGwpO1xuIFx0XHRfX3dlYnBhY2tfcmVxdWlyZV9fLnIobnMpO1xuIFx0XHRPYmplY3QuZGVmaW5lUHJvcGVydHkobnMsICdkZWZhdWx0JywgeyBlbnVtZXJhYmxlOiB0cnVlLCB2YWx1ZTogdmFsdWUgfSk7XG4gXHRcdGlmKG1vZGUgJiAyICYmIHR5cGVvZiB2YWx1ZSAhPSAnc3RyaW5nJykgZm9yKHZhciBrZXkgaW4gdmFsdWUpIF9fd2VicGFja19yZXF1aXJlX18uZChucywga2V5LCBmdW5jdGlvbihrZXkpIHsgcmV0dXJuIHZhbHVlW2tleV07IH0uYmluZChudWxsLCBrZXkpKTtcbiBcdFx0cmV0dXJuIG5zO1xuIFx0fTtcblxuIFx0Ly8gZ2V0RGVmYXVsdEV4cG9ydCBmdW5jdGlvbiBmb3IgY29tcGF0aWJpbGl0eSB3aXRoIG5vbi1oYXJtb255IG1vZHVsZXNcbiBcdF9fd2VicGFja19yZXF1aXJlX18ubiA9IGZ1bmN0aW9uKG1vZHVsZSkge1xuIFx0XHR2YXIgZ2V0dGVyID0gbW9kdWxlICYmIG1vZHVsZS5fX2VzTW9kdWxlID9cbiBcdFx0XHRmdW5jdGlvbiBnZXREZWZhdWx0KCkgeyByZXR1cm4gbW9kdWxlWydkZWZhdWx0J107IH0gOlxuIFx0XHRcdGZ1bmN0aW9uIGdldE1vZHVsZUV4cG9ydHMoKSB7IHJldHVybiBtb2R1bGU7IH07XG4gXHRcdF9fd2VicGFja19yZXF1aXJlX18uZChnZXR0ZXIsICdhJywgZ2V0dGVyKTtcbiBcdFx0cmV0dXJuIGdldHRlcjtcbiBcdH07XG5cbiBcdC8vIE9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbFxuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5vID0gZnVuY3Rpb24ob2JqZWN0LCBwcm9wZXJ0eSkgeyByZXR1cm4gT2JqZWN0LnByb3RvdHlwZS5oYXNPd25Qcm9wZXJ0eS5jYWxsKG9iamVjdCwgcHJvcGVydHkpOyB9O1xuXG4gXHQvLyBfX3dlYnBhY2tfcHVibGljX3BhdGhfX1xuIFx0X193ZWJwYWNrX3JlcXVpcmVfXy5wID0gXCJcIjtcblxuXG4gXHQvLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbiBcdHJldHVybiBfX3dlYnBhY2tfcmVxdWlyZV9fKF9fd2VicGFja19yZXF1aXJlX18ucyA9IDApO1xuIiwidmFyIFRIRU1FVEFHUyA9IFRIRU1FVEFHUyB8fCB7fTtcclxuXHJcbihmdW5jdGlvbiAoJCkge1xyXG5cclxuICAgIC8qIS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS1cclxuICAgICAgICAjIFRoaXMgYmVhdXRpZnVsIGNvZGUgd3JpdHRlbiB3aXRoIGhlYXJ0XHJcbiAgICAgICAgIyBieSBNb21pbnVsIElzbGFtIDxoZWxsb0Btb21pbnVsLm1lPlxyXG4gICAgICAgICMgSW4gRGhha2EsIEJEIGF0IHRoZSBUaGVtZVRhZ3Mgd29ya3N0YXRpb24uXHJcbiAgICAgICAgLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tKi9cclxuXHJcbiAgICAvLyBVU0UgU1RSSUNUXHJcbiAgICBcInVzZSBzdHJpY3RcIjtcclxuXHJcbiAgICB3aW5kb3cuVFQgPSB7XHJcbiAgICAgICAgaW5pdDogZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICAvLyBIZWFkZXJcclxuICAgICAgICAgICAgdGhpcy5oZWFkZXIgPSAkKCcuc2l0ZS1oZWFkZXInKTtcclxuICAgICAgICAgICAgdGhpcy5ib2R5ID0gJCgnYm9keScpO1xyXG4gICAgICAgICAgICB0aGlzLndwYWRtaW5iYXIgPSAkKCcjd3BhZG1pbmJhcicpO1xyXG5cclxuICAgICAgICAgICAgdGhpcy5oZWFkZXJGaXhlZCA9IHtcclxuICAgICAgICAgICAgICAgIGluaXRpYWxPZmZzZXQ6IHBhcnNlSW50KHRoaXMuaGVhZGVyLmF0dHIoJ2RhdGEtZml4ZWQtaW5pdGlhbC1vZmZzZXQnKSkgfHwgMTAwLFxyXG5cclxuICAgICAgICAgICAgICAgIGVuYWJsZWQ6ICQoJ1tkYXRhLWhlYWRlci1maXhlZF0nKS5sZW5ndGgsXHJcbiAgICAgICAgICAgICAgICB2YWx1ZTogZmFsc2UsXHJcblxyXG4gICAgICAgICAgICAgICAgbW9iaWxlRW5hYmxlZDogJCgnW2RhdGEtbW9iaWxlLWhlYWRlci1maXhlZF0nKS5sZW5ndGgsXHJcbiAgICAgICAgICAgICAgICBtb2JpbGVWYWx1ZTogZmFsc2VcclxuICAgICAgICAgICAgfTtcclxuXHJcblxyXG4gICAgICAgICAgICAvLyBMb2dvc1xyXG4gICAgICAgICAgICB0aGlzLnNpdGVCcmFuZGluZyA9IHRoaXMuaGVhZGVyLmZpbmQoJy5zaXRlLWJyYW5kaW5nJyk7XHJcbiAgICAgICAgICAgIHRoaXMuc2l0ZVRpdGxlID0gdGhpcy5oZWFkZXIuZmluZCgnLnNpdGUtdGl0bGUnKTtcclxuICAgICAgICAgICAgdGhpcy5sb2dvID0gdGhpcy5oZWFkZXIuZmluZCgnLm1haW4tbG9nbycpO1xyXG4gICAgICAgICAgICB0aGlzLmZpeGVkTG9nbyA9IHRoaXMuaGVhZGVyLmZpbmQoJy5sb2dvLXN0aWNreScpO1xyXG4gICAgICAgICAgICB0aGlzLm1vYmlsZUxvZ28gPSB0aGlzLmhlYWRlci5maW5kKCcubW9iaWxlLWxvZ28nKTtcclxuICAgICAgICAgICAgdGhpcy5maXhlZE1vYmlsZUxvZ28gPSB0aGlzLmhlYWRlci5maW5kKCcuZml4ZWQtbW9iaWxlLWxvZ28nKTtcclxuXHJcbiAgICAgICAgICAgIHRoaXMubG9nb0Zvck9uZXBhZ2UgPSB0aGlzLmhlYWRlci5maW5kKCcuZm9yLW9uZXBhZ2UnKTtcclxuICAgICAgICAgICAgdGhpcy5sb2dvRm9yT25lcGFnZURhcmsgPSB0aGlzLmxvZ29Gb3JPbmVwYWdlLmZpbmQoJy5kYXJrJyk7XHJcbiAgICAgICAgICAgIHRoaXMubG9nb0Zvck9uZXBhZ2VMaWdodCA9IHRoaXMubG9nb0Zvck9uZXBhZ2UuZmluZCgnLmxpZ2h0Jyk7XHJcblxyXG4gICAgICAgICAgICAvLyBNZW51c1xyXG4gICAgICAgICAgICB0aGlzLm1lZ2FNZW51ID0gdGhpcy5oZWFkZXIuZmluZCgnI21lZ2EtbWVudS13cmFwJyk7XHJcbiAgICAgICAgICAgIHRoaXMubW9iaWxlTWVudSA9ICQoJ1tkYXRhLW1vYmlsZS1tZW51LXJlc29sdXRpb25dJykuZGF0YSgnbW9iaWxlLW1lbnUtcmVzb2x1dGlvbicpO1xyXG5cclxuXHJcbiAgICAgICAgICAgIHRoaXMucmVzaXplKCk7XHJcbiAgICAgICAgfSxcclxuXHJcbiAgICAgICAgcmVzaXplOiBmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgIHRoaXMuaXNEZXNrdG9wID0gJCh3aW5kb3cpLndpZHRoKCkgPj0gOTkxO1xyXG4gICAgICAgICAgICB0aGlzLmlzTW9iaWxlID0gJCh3aW5kb3cpLndpZHRoKCkgPD0gOTkxO1xyXG4gICAgICAgICAgICB0aGlzLmlzUGFkID0gJCh3aW5kb3cpLndpZHRoKCkgPD0gMTAyNDtcclxuICAgICAgICAgICAgdGhpcy5pc01vYmlsZU1lbnUgPSAkKHdpbmRvdykud2lkdGgoKSA8PSBUVC5tb2JpbGVNZW51XHJcbiAgICAgICAgfVxyXG4gICAgfTtcclxuXHJcbiAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZSA9IHtcclxuICAgICAgICBpbml0OiBmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgIFRIRU1FVEFHUy5pbml0aWFsaXplLmdlbmVyYWwoKTtcclxuICAgICAgICAgICAgVEhFTUVUQUdTLmluaXRpYWxpemUuZG9tYWluU2VhcmNoKCk7XHJcbiAgICAgICAgICAgIFRIRU1FVEFHUy5pbml0aWFsaXplLnN3aXBlclNsaWRlcigpO1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5zaWRlYmFyTWVudSgpO1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5jb3VudFVwKCk7XHJcbiAgICAgICAgICAgIFRIRU1FVEFHUy5pbml0aWFsaXplLmNvdW50RG93bigpO1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5zZWN0aW9uU3dpdGNoKCk7XHJcbiAgICAgICAgICAgIFRIRU1FVEFHUy5pbml0aWFsaXplLmdvb2dsZU1hcCgpO1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5jb250YWN0RnJvbSgpO1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5oYW5kbGVNb2JpbGVIZWFkZXIoKTtcclxuICAgICAgICB9LFxyXG5cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIENvbGxlY3Rpb24gb2Ygc25pcHBldCBhbmQgdHdlYWtzICAgICAgICAgICA9Ki9cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuXHJcbiAgICAgICAgZ2VuZXJhbDogZnVuY3Rpb24gKCkge1xyXG5cclxuICAgICAgICAgICAgaWYgKCQoJ2JvZHknKS5oYXNDbGFzcyhcImFkbWluLWJhclwiKSkge1xyXG4gICAgICAgICAgICAgICAgJCgnYm9keScpLmFkZENsYXNzKCdoZWFkZXItcG9zaXRpb24nKTtcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAvLyBJbml0IFdvdyBKc1xyXG4gICAgICAgICAgICB2YXIgd293ID0gbmV3IFdPVyh7XHJcbiAgICAgICAgICAgICAgICBib3hDbGFzczogJ3dvdycsXHJcbiAgICAgICAgICAgICAgICBhbmltYXRlQ2xhc3M6ICdhbmltYXRlZCcsXHJcbiAgICAgICAgICAgICAgICBvZmZzZXQ6IDAsXHJcbiAgICAgICAgICAgICAgICBtb2JpbGU6IGZhbHNlLFxyXG4gICAgICAgICAgICAgICAgbGl2ZTogdHJ1ZSxcclxuICAgICAgICAgICAgICAgIHNjcm9sbENvbnRhaW5lcjogbnVsbFxyXG4gICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgd293LmluaXQoKTtcclxuXHJcblxyXG4gICAgICAgICAgICAvLyBQcmljaW5nIFN3aXRjaGVyXHJcbiAgICAgICAgICAgICQoJyNqcy1jb250Y2hlY2tib3gnKS5jaGFuZ2UoZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICAgICAgaWYgKHRoaXMuY2hlY2tlZCkge1xyXG5cdFx0XHRcdCAgICAkKCcubW9udGhseS1wcmljZScpLmNzcygnZGlzcGxheScsICdub25lJyk7XHJcblx0XHRcdFx0ICAgICQoJy55ZWFybHktcHJpY2UnKS5jc3MoJ2Rpc3BsYXknLCAnYmxvY2snKTtcclxuICAgICAgICAgICAgICAgICAgICAkKCcucHJpY2luZy1zd2l0Y2gtd3JhcCcpLmFkZENsYXNzKCd5ZWFybHknKTtcdFxyXG4gICAgICAgICAgICAgICAgICAgICQoJy5wcmljaW5nLXN3aXRjaC13cmFwJykucmVtb3ZlQ2xhc3MoJ21vbnRobHknKTtcdFx0XHJcbiAgICAgICAgICAgICAgICAgICAgJCgnLmFmdGVyaW5wdXQnKS5hZGRDbGFzcygnYWN0aXZlJyk7XHRcclxuICAgICAgICAgICAgICAgICAgICAkKCcuYmVmb3JlaW5wdXQnKS5yZW1vdmVDbGFzcygnYWN0aXZlJyk7XHJcblx0XHRcdFx0fSBlbHNlIHtcclxuXHRcdFx0XHQgICAgJCgnLm1vbnRobHktcHJpY2UnKS5jc3MoJ2Rpc3BsYXknLCAnYmxvY2snKTtcclxuXHRcdFx0XHQgICAgJCgnLnllYXJseS1wcmljZScpLmNzcygnZGlzcGxheScsICdub25lJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgJCgnLnByaWNpbmctc3dpdGNoLXdyYXAnKS5yZW1vdmVDbGFzcygneWVhcmx5Jyk7XHJcbiAgICAgICAgICAgICAgICAgICAgJCgnLnByaWNpbmctc3dpdGNoLXdyYXAnKS5hZGRDbGFzcygnbW9udGhseScpO1x0XHJcbiAgICAgICAgICAgICAgICAgICAgJCgnLmFmdGVyaW5wdXQnKS5yZW1vdmVDbGFzcygnYWN0aXZlJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgJCgnLmJlZm9yZWlucHV0JykuYWRkQ2xhc3MoJ2FjdGl2ZScpO1x0XHRcdFx0XHJcblx0XHRcdFx0fVxyXG4gICAgICAgICAgICB9KTtcclxuXHJcblxyXG4gICAgICAgICAgICBpZiAoJChcIiN3cGFkbWluYmFyXCIpLmxlbmd0aCAmJiAkKHdpbmRvdykud2lkdGgoKSA8IDc2OCkge1xyXG4gICAgICAgICAgICAgICAgJChcIiN3cGFkbWluYmFyXCIpLmNzcyh7XHJcbiAgICAgICAgICAgICAgICAgICAgcG9zaXRpb246IFwiZml4ZWRcIixcclxuICAgICAgICAgICAgICAgICAgICB0b3A6IFwiMFwiXHJcbiAgICAgICAgICAgICAgICB9KVxyXG4gICAgICAgICAgICB9XHJcblxyXG4gICAgICAgICAgICB2YXIgYmxvZ0NvbnRhaW5lciA9ICQoXCIuYmxvZy1tYXNvbnJ5XCIpO1xyXG5cclxuICAgICAgICAgICAgYmxvZ0NvbnRhaW5lci5tYXNvbnJ5KHtcclxuICAgICAgICAgICAgICAgIGl0ZW1TZWxlY3RvcjogJy5wb3N0LWl0ZW0nLFxyXG4gICAgICAgICAgICAgICAgcGVyY2VudFBvc2l0aW9uOiB0cnVlXHJcbiAgICAgICAgICAgIH0pO1xyXG5cclxuICAgICAgICAgICAgLyogTWFnbmVmaWMgUG9wdXAgKi9cclxuICAgICAgICAgICAgJCgnLnBvcHVwLXZpZGVvJykuZWFjaChmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgICAgICAkKCcucG9wdXAtdmlkZW8nKS5tYWduaWZpY1BvcHVwKHtcclxuICAgICAgICAgICAgICAgICAgICB0eXBlOiAnaWZyYW1lJ1xyXG4gICAgICAgICAgICAgICAgfSk7XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0sXHJcblxyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIFNpZGViYXIgTWVudSAgICAgICAgICA9Ki9cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICBzaWRlYmFyTWVudTogZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICB2YXIgJHBvcHVwID0gJCgnLmNhbnZhcy1tZW51LXdyYXBwZXInKTtcclxuXHJcbiAgICAgICAgICAgICQoXCIjcGFnZS1vcGVuLW1haW4tbWVudVwiKS5vbignY2xpY2snLCBmdW5jdGlvbiAoZSkge1xyXG4gICAgICAgICAgICAgICAgZS5wcmV2ZW50RGVmYXVsdCgpO1xyXG4gICAgICAgICAgICAgICAgdmFyIG1hc2sgPSAnPGRpdiBjbGFzcz1cIm1hc2stb3ZlcmxheVwiPic7XHJcbiAgICAgICAgICAgICAgICAkKG1hc2spLmhpZGUoKS5hcHBlbmRUbygnYm9keScpLmZhZGVJbignZmFzdCcpO1xyXG4gICAgICAgICAgICAgICAgJHBvcHVwLmFkZENsYXNzKCdvcGVuJyk7XHJcbiAgICAgICAgICAgICAgICAkKFwiLnR0LWhhbWJ1cmdlclwiKS5hZGRDbGFzcygnYWN0aXZlJyk7XHJcbiAgICAgICAgICAgICAgICAkKFwiaHRtbFwiKS5hZGRDbGFzcyhcIm5vLXNjcm9sbCBzaWRlYmFyLW9wZW5cIikuaGVpZ2h0KHdpbmRvdy5pbm5lckhlaWdodCArIFwicHhcIik7XHJcbiAgICAgICAgICAgIH0pO1xyXG5cclxuICAgICAgICAgICAgJChcIiNwYWdlLWNsb3NlLW1haW4tbWVudSwgLm1haW4tbmF2LWNvbnRhaW5lciBsaSBhXCIpLm9uKCdjbGljaycsIGZ1bmN0aW9uIChlKSB7XHJcbiAgICAgICAgICAgICAgICAkKCcubWFzay1vdmVybGF5JykucmVtb3ZlKCk7XHJcbiAgICAgICAgICAgICAgICAkcG9wdXAucmVtb3ZlQ2xhc3MoJ29wZW4nKTtcclxuICAgICAgICAgICAgICAgICQoXCIudHQtaGFtYnVyZ2VyXCIpLnJlbW92ZUNsYXNzKCdhY3RpdmUnKTtcclxuICAgICAgICAgICAgICAgICQoXCJodG1sXCIpLnJlbW92ZUNsYXNzKFwibm8tc2Nyb2xsIHNpZGViYXItb3BlblwiKS5oZWlnaHQoXCJhdXRvXCIpO1xyXG4gICAgICAgICAgICB9KTtcclxuXHJcbiAgICAgICAgfSxcclxuXHJcbiAgICAgICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIGhhbmRsZSBNb2JpbGUgSGVhZGVyICAgICAgICAgID0qL1xyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcblxyXG4gICAgICAgIGhhbmRsZU1vYmlsZUhlYWRlcjogZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICBpZiAoVFQuaGVhZGVyICYmIFRULmhlYWRlci5sZW5ndGgpIHtcclxuXHJcbiAgICAgICAgICAgICAgICBpZiAoVFQuaXNNb2JpbGVNZW51KSB7XHJcbiAgICAgICAgICAgICAgICAgICAgVFQuaGVhZGVyLmFkZENsYXNzKCdtb2JpbGUtaGVhZGVyJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgVFQuYm9keS5hZGRDbGFzcygnaXMtbW9iaWxlLW1lbnUnKTtcclxuICAgICAgICAgICAgICAgICAgICBzZXRUaW1lb3V0KGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgJCgnLm1haW4tbmF2JykuYWRkQ2xhc3MoJ3VuaGlkZGVuJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgfSwgMzAwKTtcclxuICAgICAgICAgICAgICAgIH0gZWxzZSB7XHJcbiAgICAgICAgICAgICAgICAgICAgVFQuaGVhZGVyLnJlbW92ZUNsYXNzKCdtb2JpbGUtaGVhZGVyJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgVFQuYm9keS5yZW1vdmVDbGFzcygnaXMtbW9iaWxlLW1lbnUnKTtcclxuICAgICAgICAgICAgICAgICAgICAkKCcubWFpbi1uYXYnKS5hZGRDbGFzcygndmlzaWJsZScpO1xyXG4gICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfSxcclxuXHJcbiAgICAgICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xyXG4gICAgICAgIC8qPSAgICAgICAgICAgaGFuZGxlIEZpeGVkIEhlYWRlciAgICAgICAgICA9Ki9cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcblxyXG4gICAgICAgIGhhbmRsZUZpeGVkSGVhZGVyOiBmdW5jdGlvbiAoKSB7XHJcblxyXG4gICAgICAgICAgICAvLyBUVC5pbml0KCk7XHJcbiAgICAgICAgICAgIHZhciBmaXhlZCA9IFRULmhlYWRlckZpeGVkO1xyXG5cclxuICAgICAgICAgICAgaWYgKCQoZG9jdW1lbnQpLnNjcm9sbFRvcCgpID4gZml4ZWQuaW5pdGlhbE9mZnNldCkge1xyXG5cclxuICAgICAgICAgICAgICAgIGlmICgoIVRULmlzTW9iaWxlTWVudSAmJiBmaXhlZC5lbmFibGVkICYmICFmaXhlZC52YWx1ZSkgfHxcclxuICAgICAgICAgICAgICAgICAgICAoVFQuaXNNb2JpbGVNZW51ICYmIGZpeGVkLm1vYmlsZUVuYWJsZWQgJiYgIWZpeGVkLm1vYmlsZVZhbHVlKSkge1xyXG5cclxuICAgICAgICAgICAgICAgICAgICBpZiAoVFQuaXNNb2JpbGVNZW51KSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGZpeGVkLm1vYmlsZVZhbHVlID0gdHJ1ZTtcclxuICAgICAgICAgICAgICAgICAgICB9IGVsc2Uge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBmaXhlZC52YWx1ZSA9IHRydWU7XHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG4gICAgICAgICAgICAgICAgICAgIFRULmhlYWRlci5hZGRDbGFzcygnaGVhZGVyLWZpeGVkIG5vLXRyYW5zaXRpb24nKTtcclxuICAgICAgICAgICAgICAgIH1cclxuXHJcbiAgICAgICAgICAgIH0gZWxzZSBpZiAoZml4ZWQudmFsdWUgfHwgZml4ZWQubW9iaWxlVmFsdWUpIHtcclxuICAgICAgICAgICAgICAgIGZpeGVkLnZhbHVlID0gZmFsc2U7XHJcbiAgICAgICAgICAgICAgICBmaXhlZC5tb2JpbGVWYWx1ZSA9IGZhbHNlO1xyXG4gICAgICAgICAgICAgICAgVFQuaGVhZGVyLnJlbW92ZUNsYXNzKCdoZWFkZXItZml4ZWQnKTtcclxuICAgICAgICAgICAgfVxyXG5cclxuICAgICAgICAgICAgLy8gRWZmZWN0IGFwcGVhcmFuY2VcclxuICAgICAgICAgICAgaWYgKCQoZG9jdW1lbnQpLnNjcm9sbFRvcCgpID4gZml4ZWQuaW5pdGlhbE9mZnNldCArIDUwKSB7XHJcbiAgICAgICAgICAgICAgICBUVC5oZWFkZXIucmVtb3ZlQ2xhc3MoJ25vLXRyYW5zaXRpb24nKS5hZGRDbGFzcygnc2hvd2VkJyk7XHJcbiAgICAgICAgICAgIH0gZWxzZSB7XHJcbiAgICAgICAgICAgICAgICBUVC5oZWFkZXIucmVtb3ZlQ2xhc3MoJ3Nob3dlZCcpLmFkZENsYXNzKCduby10cmFuc2l0aW9uJyk7XHJcbiAgICAgICAgICAgIH1cclxuICAgICAgICB9LFxyXG5cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcbiAgICAgICAgLyo9ICAgICAgICAgICBCbG9nICAgICAgICAgID0qL1xyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuXHJcbiAgICAgICAgZG9tYWluU2VhcmNoOiBmdW5jdGlvbiAoKSB7XHJcblxyXG4gICAgICAgICAgICAvKiBEb21haW4gQ2hlY2sgKi9cclxuICAgICAgICAgICAgdmFyIERvbWFpbkNoZWNrID0ge1xyXG4gICAgICAgICAgICAgICAgc3VibWl0OiBmdW5jdGlvbiAoZSkge1xyXG4gICAgICAgICAgICAgICAgICAgIGUucHJldmVudERlZmF1bHQoKTtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIG9iaiA9IGUuZGF0YSxcclxuICAgICAgICAgICAgICAgICAgICAgICAgZWwgPSBvYmoud2FwLmZpbmQoXCIjdHQtZG9tYWluLXJlc3VsdHNcIiksXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGRvbWFpbkRlZmF1bHQgPSBcInRoZW1ldGFncy5jb21cIixcclxuICAgICAgICAgICAgICAgICAgICAgICAgYmFzZW5hbWUgPSBvYmouaW5wdXQudmFsKCkgIT09IFwiXCIgPyBvYmouaW5wdXQudmFsKCkgOiBkb21haW5EZWZhdWx0LFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBleHQgPSBvYmouc2VsZWN0LnZhbCgpICE9PSBcIlwiID8gb2JqLnNlbGVjdC52YWwoKSA6ICcnLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICB3aG1jc191cmwgPSBvYmoud2htY3NfdXJsLnZhbCgpICE9PSBcIlwiID8gb2JqLndobWNzX3VybC52YWwoKSA6ICcnLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICB0cmFuc2ZlclVybCA9IG9iai50cmFuc2ZlclVybC52YWwoKSAhPT0gXCJcIiA/IG9iai50cmFuc2ZlclVybC52YWwoKSA6ICcnLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBkb21haW5TZWFyY2hPcHRpb24gPSBvYmouZG9tYWluU2VhcmNoT3B0aW9uLnZhbCgpICE9PSBcIlwiID8gb2JqLmRvbWFpblNlYXJjaE9wdGlvbi52YWwoKSA6ICcnLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBleHRlbnNpb24gPSBEb21haW5DaGVjay5kb3RFeHQob2JqLmlucHV0LnZhbCgpKTtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIGRvbWFpbk5hbWUgPSBcIlwiO1xyXG4gICAgICAgICAgICAgICAgICAgIGlmIChiYXNlbmFtZS5pbmRleE9mKCcuJykgPiAtMSkge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBkb21haW5OYW1lID0gYmFzZW5hbWU7XHJcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIGlmIChiYXNlbmFtZS5pbmRleE9mKCcuJykgPT0gLTEpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgZG9tYWluTmFtZSA9IGJhc2VuYW1lICsgKGV4dCA/ICcuJyArIGV4dCA6ICcuY29tJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG5cclxuICAgICAgICAgICAgICAgICAgICBvYmouc2VjdXJpdHkgPSBvYmouZm9ybS5maW5kKFwiaW5wdXRbbmFtZT1zZWN1cml0eV1cIikudmFsKCk7XHJcbiAgICAgICAgICAgICAgICAgICAgb2JqLmVsID0gZWw7XHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIGRvbWFpbkRhdGEgPSB7fSxcclxuICAgICAgICAgICAgICAgICAgICAgICAgZG9tYWluUmVzdWx0VGFibGUgPSAkKFxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgJzxkaXYgaWQ9XCJ0dF9yZXN1bHRfaXRlbVwiIGNsYXNzPVwidHQtcmVzdWx0LWRvbWFpbi1ib3hcIiByb2xlPVwiYWxlcnRcIj4gPC9kaXY+PC9kaXY+J1xyXG4gICAgICAgICAgICAgICAgICAgICAgICApLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBkb21haW5SZXN1bHQgPSAkKFxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgJzxkaXYgY2xhc3M9XCJpbm5lci1ibG9jay1yZXN1bHQtaXRlbVwiPicgK1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgJzxkaXYgY2xhc3M9XCJzcGlubmVyIHR0LWxvYWRpbmctcmVzdWx0cyB0ZXh0LWNlbnRlclwiPicgK1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgJzxpIGNsYXNzPVwiZmFzIGZhLXNwaW5uZXIgZmEtc3BpbiBmYS1sZyBmYS1md1wiPjwvaT4nICtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICc8c3Bhbj4gU2VhY2hpbmcuLi48L3NwYW4+JyArXHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAnPHNwYW4gY2xhc3M9XCJzci1vbmx5XCI+Li4uPC9zcGFuPicgK1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgXCI8L2Rpdj5cIlxyXG4gICAgICAgICAgICAgICAgICAgICAgICApO1xyXG5cclxuICAgICAgICAgICAgICAgICAgICAkLmV4dGVuZChkb21haW5EYXRhLCBvYmopO1xyXG4gICAgICAgICAgICAgICAgICAgIGRvbWFpbkRhdGEuZG9tYWluID0gZG9tYWluTmFtZTtcclxuICAgICAgICAgICAgICAgICAgICBkb21haW5EYXRhLmV4dGVuc2lvbiA9IGV4dGVuc2lvbjtcclxuICAgICAgICAgICAgICAgICAgICBkb21haW5EYXRhLndobWNzX3VybCA9IHdobWNzX3VybDtcclxuICAgICAgICAgICAgICAgICAgICBkb21haW5EYXRhLnRyYW5zZmVyVXJsID0gdHJhbnNmZXJVcmw7XHJcbiAgICAgICAgICAgICAgICAgICAgZG9tYWluRGF0YS5lbCA9IGRvbWFpblJlc3VsdDtcclxuICAgICAgICAgICAgICAgICAgICBkb21haW5EYXRhLmRvbWFpblNlYXJjaE9wdGlvbiA9IGRvbWFpblNlYXJjaE9wdGlvbjtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgZG9tYWluUmVzdWx0LmRhdGEoXCJkb21haW5cIiwgZG9tYWluRGF0YS5kb21haW4pO1xyXG5cclxuICAgICAgICAgICAgICAgICAgICBpZiAob2JqLmVsLmZpbmQoXCIjdHRfcmVzdWx0X2l0ZW1cIikubGVuZ3RoID09IDApIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgb2JqLmVsLmFwcGVuZChkb21haW5SZXN1bHRUYWJsZSk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIG9iai5lbC5maW5kKFwiI3R0X3Jlc3VsdF9pdGVtXCIpLmFwcGVuZChkb21haW5SZXN1bHQpO1xyXG4gICAgICAgICAgICAgICAgICAgIH0gZWxzZSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIG9iai5lbC5maW5kKFwiI3R0X3Jlc3VsdF9pdGVtXCIpLnJlbW92ZSgpO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBvYmouZWwuYXBwZW5kKGRvbWFpblJlc3VsdFRhYmxlKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgb2JqLmVsLmZpbmQoXCIjdHRfcmVzdWx0X2l0ZW1cIikuYXBwZW5kKGRvbWFpblJlc3VsdCk7XHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG5cclxuICAgICAgICAgICAgICAgICAgICBEb21haW5DaGVjay5jaGVja0FqYXgoZG9tYWluRGF0YSk7XHJcbiAgICAgICAgICAgICAgICB9LFxyXG5cclxuICAgICAgICAgICAgICAgIG5hbWU6IGZ1bmN0aW9uIChkb21haW4pIHtcclxuICAgICAgICAgICAgICAgICAgICByZXR1cm4gZG9tYWluLnJlcGxhY2UoL14uKlxcL3xcXC5bXi5dKiQvZywgXCJcIik7XHJcbiAgICAgICAgICAgICAgICB9LFxyXG5cclxuICAgICAgICAgICAgICAgIGRvdEV4dDogZnVuY3Rpb24gKGV4dCkge1xyXG4gICAgICAgICAgICAgICAgICAgIHZhciBmRXh0LFxyXG4gICAgICAgICAgICAgICAgICAgICAgICB0RXh0ID0gZXh0LnNwbGl0KFwiLlwiLCAzKTtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgaWYgKHRFeHRbMV0gPT09IHVuZGVmaW5lZCkge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBmRXh0ID0gXCJjb21cIjtcclxuICAgICAgICAgICAgICAgICAgICB9IGVsc2UgaWYgKHRFeHRbMF0gPT09IFwid3d3XCIpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgZkV4dCA9IHRFeHRbMl07XHJcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgZkV4dCA9IHRFeHRbMV07XHJcbiAgICAgICAgICAgICAgICAgICAgfVxyXG5cclxuICAgICAgICAgICAgICAgICAgICByZXR1cm4gZkV4dDtcclxuICAgICAgICAgICAgICAgIH0sXHJcblxyXG4gICAgICAgICAgICAgICAgY2hlY2tBamF4OiBmdW5jdGlvbiAob2JqKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIGRhdGEgPSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGRvbWFpbjogb2JqLmRvbWFpbixcclxuICAgICAgICAgICAgICAgICAgICAgICAgd2htY3NfdXJsOiBvYmoud2htY3NfdXJsLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICB0cmFuc2ZlclVybDogb2JqLnRyYW5zZmVyVXJsLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBkb21haW5fc2VhcmNoX29wdGlvbjogb2JqLmRvbWFpblNlYXJjaE9wdGlvbixcclxuICAgICAgICAgICAgICAgICAgICAgICAgYWN0aW9uOiBcInR0X2FqYXhfc2VhcmNoX2RvbWFpblwiLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBzZWN1cml0eTogb2JqLnNlY3VyaXR5LFxyXG4gICAgICAgICAgICAgICAgICAgIH07XHJcblxyXG5cclxuXHJcbiAgICAgICAgICAgICAgICAgICAgJC5hamF4KHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgdXJsOiB0dF9hamF4X3VybCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgdHlwZTogXCJQT1NUXCIsXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGRhdGFUeXBlOiBcImpzb25cIixcclxuICAgICAgICAgICAgICAgICAgICAgICAgZGF0YTogZGF0YSxcclxuICAgICAgICAgICAgICAgICAgICAgICAgc3VjY2VzczogZnVuY3Rpb24gKGRhdGEpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9iai5lbC5maW5kKFwiLnNwaW5uZXJcIikucmVtb3ZlKCk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBvYmouZWwuYXBwZW5kKGRhdGEucmVzdWx0c19odG1sKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3I6IGZ1bmN0aW9uICh4aHIsIGFqYXhPcHRpb25zLCB0aHJvd25FcnJvcikge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coeGhyKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbnNvbGUubG9nKHRocm93bkVycm9yKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgICAgIH0sXHJcbiAgICAgICAgICAgIH07XHJcblxyXG4gICAgICAgICAgICAkKFwiI3R0LWRvbWFpbi1zZWFyY2hcIikuaXMoZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICAgICAgdmFyIGlkID0gJCh0aGlzKSxcclxuICAgICAgICAgICAgICAgICAgICBzdWJtaXRFbCA9IGlkLmZpbmQoXCIjdHQtc2VhcmNoXCIpLFxyXG4gICAgICAgICAgICAgICAgICAgIGlucHV0RWwgPSBpZC5maW5kKFwiI3R0LWRvbWFpblwiKSxcclxuICAgICAgICAgICAgICAgICAgICBzZWxlY3RFbCA9IGlkLmZpbmQoXCIjZG9tYWluZXh0XCIpLFxyXG4gICAgICAgICAgICAgICAgICAgIGZvcm1FbCA9IGlkLmZpbmQoXCIjdHQtZG9tYWluLWZvcm1cIiksXHJcbiAgICAgICAgICAgICAgICAgICAgYWNFbCA9IGlkLmZpbmQoJ2lucHV0W25hbWU9XCJ3aG1jc191cmxcIl0nKSxcclxuICAgICAgICAgICAgICAgICAgICB0cmFuc2ZlclVybCA9IGlkLmZpbmQoJ2lucHV0W25hbWU9XCJ3aG1jc190cmFuc2Zlcl91cmxcIl0nKSxcclxuICAgICAgICAgICAgICAgICAgICBkb21haW5TZWFyY2hPcHRpb24gPSBpZC5maW5kKCdpbnB1dFtuYW1lPVwiZG9tYWluX3NlYXJjaF9vcHRpb25cIl0nKSxcclxuICAgICAgICAgICAgICAgICAgICBkYXRhO1xyXG5cclxuICAgICAgICAgICAgICAgIGRhdGEgPSB7XHJcbiAgICAgICAgICAgICAgICAgICAgc3VibWl0OiBzdWJtaXRFbCxcclxuICAgICAgICAgICAgICAgICAgICBpbnB1dDogaW5wdXRFbCxcclxuICAgICAgICAgICAgICAgICAgICBzZWxlY3Q6IHNlbGVjdEVsLFxyXG4gICAgICAgICAgICAgICAgICAgIHdobWNzX3VybDogYWNFbCxcclxuICAgICAgICAgICAgICAgICAgICB0cmFuc2ZlclVybDogdHJhbnNmZXJVcmwsXHJcbiAgICAgICAgICAgICAgICAgICAgZm9ybTogZm9ybUVsLFxyXG4gICAgICAgICAgICAgICAgICAgIGRpdjogaWQsXHJcbiAgICAgICAgICAgICAgICAgICAgd2FwOiBpZCxcclxuICAgICAgICAgICAgICAgICAgICBkb21haW5TZWFyY2hPcHRpb246IGRvbWFpblNlYXJjaE9wdGlvbixcclxuICAgICAgICAgICAgICAgIH07XHJcblxyXG5cclxuICAgICAgICAgICAgICAgIHN1Ym1pdEVsLmF0dHIoXCJkaXNhYmxlZFwiLCB0cnVlKTtcclxuICAgICAgICAgICAgICAgIGlucHV0RWwua2V5dXAoZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICAgICAgICAgIGlmICgkKHRoaXMpLnZhbCgpLmxlbmd0aCAhPSAwKSBzdWJtaXRFbC5hdHRyKFwiZGlzYWJsZWRcIiwgZmFsc2UpO1xyXG4gICAgICAgICAgICAgICAgICAgIGVsc2Ugc3VibWl0RWwuYXR0cihcImRpc2FibGVkXCIsIHRydWUpO1xyXG4gICAgICAgICAgICAgICAgfSk7XHJcblxyXG4gICAgICAgICAgICAgICAgc3VibWl0RWwub24oXCJjbGlja1wiLCBkYXRhLCBEb21haW5DaGVjay5zdWJtaXQpO1xyXG4gICAgICAgICAgICB9KTtcclxuXHJcbiAgICAgICAgICAgIC8vIExvYWRpbmcgU2NyZWVuXHJcbiAgICAgICAgICAgIGNvbnN0IGxvYWRpbmdDbGFzcyA9ICQoXCIubG9hZGluZ1wiKSxcclxuICAgICAgICAgICAgICAgIHJlbW92ZUZMb3cgPSAkKFwiaHRtbCxib2R5XCIpLmNzcyhcIm92ZXJmbG93XCIsIFwiYXV0b1wiKTtcclxuXHJcbiAgICAgICAgICAgIGlmIChsb2FkaW5nQ2xhc3MubGVuZ3RoID09PSAxKSB7XHJcbiAgICAgICAgICAgICAgICAkKHdpbmRvdykub24oXCJsb2FkXCIsIGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgICAgICBsb2FkaW5nQ2xhc3MuZmFkZU91dCgpO1xyXG4gICAgICAgICAgICAgICAgICAgIHJlbW92ZUZMb3c7XHJcbiAgICAgICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH0sXHJcblxyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIFN3aXBlciBTbGlkZXIgICAgICAgICAgPSovXHJcbiAgICAgICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xyXG5cclxuICAgICAgICBzd2lwZXJTbGlkZXI6IGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgJCgnI3BvcnRmb2xpby10ZXN0aW1vbmlhbCcpLmVhY2goZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICAgICAgdmFyIHN3aXBlciA9IG5ldyBTd2lwZXIoJyNwb3J0Zm9saW8tdGVzdGltb25pYWwnLCB7XHJcbiAgICAgICAgICAgICAgICAgICAgc2xpZGVzUGVyVmlldzogMSxcclxuICAgICAgICAgICAgICAgICAgICBzcGFjZUJldHdlZW46IDMwLFxyXG4gICAgICAgICAgICAgICAgICAgIGxvb3A6IHRydWUsXHJcbiAgICAgICAgICAgICAgICAgICAgc3BlZWQ6IDgwMCxcclxuICAgICAgICAgICAgICAgICAgICBhdXRvcGxheToge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBkZWxheTogNTAwMCxcclxuICAgICAgICAgICAgICAgICAgICB9LFxyXG4gICAgICAgICAgICAgICAgICAgIG5hdmlnYXRpb246IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgbmV4dEVsOiAnLnRlc3RpLWJ1dHRvbi1uZXh0JyxcclxuICAgICAgICAgICAgICAgICAgICAgICAgcHJldkVsOiAnLnRlc3RpLWJ1dHRvbi1wcmV2JyxcclxuICAgICAgICAgICAgICAgICAgICB9LFxyXG4gICAgICAgICAgICAgICAgfSk7XHJcbiAgICAgICAgICAgIH0pO1xyXG5cclxuICAgICAgICAgICAgJCgnLnJlbGF0ZWQtcHJvZHVjdCcpLmVhY2goZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICAgICAgdmFyIHN3aXBlciA9IG5ldyBTd2lwZXIoJy5yZWxhdGVkLXByb2R1Y3QnLCB7XHJcbiAgICAgICAgICAgICAgICAgICAgc2xpZGVzUGVyVmlldzogMyxcclxuICAgICAgICAgICAgICAgICAgICBzcGFjZUJldHdlZW46IDMwLFxyXG4gICAgICAgICAgICAgICAgICAgIGxvb3A6IHRydWUsXHJcbiAgICAgICAgICAgICAgICAgICAgc3BlZWQ6IDgwMCxcclxuICAgICAgICAgICAgICAgICAgICBhdXRvcGxheToge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBkZWxheTogMjAwMCxcclxuICAgICAgICAgICAgICAgICAgICB9LFxyXG4gICAgICAgICAgICAgICAgICAgIG5hdmlnYXRpb246IHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgbmV4dEVsOiAnLnByb2R1Y3QtYnV0dG9uLW5leHQnLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBwcmV2RWw6ICcucHJvZHVjdC1idXR0b24tcHJldicsXHJcbiAgICAgICAgICAgICAgICAgICAgfSxcclxuICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgICAgICB9KTtcclxuXHJcbiAgICAgICAgfSxcclxuXHJcbiAgICAgICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIFNlY3Rpb24gU3dpdGNoICAgICAgICAgID0qL1xyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcblxyXG4gICAgICAgIHNlY3Rpb25Td2l0Y2g6IGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgJCgnLnBhZ2Utc2Nyb2xsLCAuc2l0ZS1oZWFkZXIgLm1lbnUgbGkgYScpLm9uKCdjbGljaycsIGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgIGlmIChsb2NhdGlvbi5wYXRobmFtZS5yZXBsYWNlKC9eXFwvLywgJycpID09IHRoaXMucGF0aG5hbWUucmVwbGFjZSgvXlxcLy8sICcnKSAmJiBsb2NhdGlvbi5ob3N0bmFtZSA9PSB0aGlzLmhvc3RuYW1lKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIHRhcmdldCA9ICQodGhpcy5oYXNoKTtcclxuICAgICAgICAgICAgICAgICAgICBpZiAodGFyZ2V0Lmxlbmd0aCA+IDApIHtcclxuXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHRhcmdldCA9IHRhcmdldC5sZW5ndGggPyB0YXJnZXQgOiAkKCdbbmFtZT0nICsgdGhpcy5oYXNoLnNsaWNlKDEpICsgJ10nKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgJCgnaHRtbCxib2R5JykuYW5pbWF0ZSh7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBzY3JvbGxUb3A6IHRhcmdldC5vZmZzZXQoKS50b3AgLSAxMzBcclxuICAgICAgICAgICAgICAgICAgICAgICAgfSwgMTAwMCk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBmYWxzZTtcclxuICAgICAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH0sXHJcblxyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIENvdW50dXAgICAgICAgICAgPSovXHJcbiAgICAgICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xyXG5cclxuICAgICAgICBjb3VudFVwOiBmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgIHZhciBvcHRpb25zID0ge1xyXG4gICAgICAgICAgICAgICAgdXNlRWFzaW5nOiB0cnVlLFxyXG4gICAgICAgICAgICAgICAgdXNlR3JvdXBpbmc6IHRydWUsXHJcbiAgICAgICAgICAgICAgICBzZXBhcmF0b3I6ICcsJyxcclxuICAgICAgICAgICAgICAgIGRlY2ltYWw6ICcuJyxcclxuICAgICAgICAgICAgICAgIHByZWZpeDogJycsXHJcbiAgICAgICAgICAgICAgICBzdWZmaXg6ICcnXHJcbiAgICAgICAgICAgIH07XHJcblxyXG4gICAgICAgICAgICB2YXIgY291bnRlRWwgPSAkKCdbZGF0YS1jb3VudGVyXScpO1xyXG5cclxuICAgICAgICAgICAgaWYgKGNvdW50ZUVsKSB7XHJcbiAgICAgICAgICAgICAgICBjb3VudGVFbC5lYWNoKGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgICAgICB2YXIgdmFsID0gJCh0aGlzKS5kYXRhKCdjb3VudGVyJyk7XHJcblxyXG4gICAgICAgICAgICAgICAgICAgIHZhciBjb3VudHVwID0gbmV3IENvdW50VXAodGhpcywgMCwgdmFsLCAwLCAyLjUsIG9wdGlvbnMpO1xyXG4gICAgICAgICAgICAgICAgICAgICQodGhpcykuYXBwZWFyKGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgY291bnR1cC5zdGFydCgpO1xyXG4gICAgICAgICAgICAgICAgICAgIH0sIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgYWNjWDogMCxcclxuICAgICAgICAgICAgICAgICAgICAgICAgYWNjWTogMFxyXG4gICAgICAgICAgICAgICAgICAgIH0pXHJcbiAgICAgICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgfVxyXG4gICAgICAgIH0sXHJcblxyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuICAgICAgICAvKj0gICAgICAgICAgIENvdW50ZG93biAgICAgICAgICA9Ki9cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcbiAgICAgICAgY291bnREb3duOiBmdW5jdGlvbiAoKSB7XHJcblxyXG4gICAgICAgICAgICBpZiAoJCgnLmNvdW50ZG93bicpLmxlbmd0aCA+IDApIHtcclxuXHJcbiAgICAgICAgICAgICAgICAkKCcuY291bnRkb3duJykuZWFjaChmdW5jdGlvbiAoaW5kZXgsIHZhbHVlKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIGNvdW50X3llYXIgPSAkKHRoaXMpLmRhdGEoXCJjb3VudC15ZWFyXCIpO1xyXG4gICAgICAgICAgICAgICAgICAgIHZhciBjb3VudF9tb250aCA9ICQodGhpcykuZGF0YShcImNvdW50LW1vbnRoXCIpO1xyXG4gICAgICAgICAgICAgICAgICAgIHZhciBjb3VudF9kYXkgPSAkKHRoaXMpLmRhdGEoXCJjb3VudC1kYXlcIik7XHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIGNvdW50X2RhdGUgPSBjb3VudF95ZWFyICsgJy8nICsgY291bnRfbW9udGggKyAnLycgKyBjb3VudF9kYXk7XHJcbiAgICAgICAgICAgICAgICAgICAgJCh0aGlzKS5jb3VudGRvd24oY291bnRfZGF0ZSwgZnVuY3Rpb24gKGV2ZW50KSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICQodGhpcykuaHRtbChldmVudC5zdHJmdGltZSgnPGRpdiBjbGFzcz1cImNvdW50aW5nXCI+PHNwYW4gY2xhc3M9XCJDb3VudGRvd25Db250ZW50XCI+JUQ8c3BhbiBjbGFzcz1cIkNvdW50ZG93bkxhYmVsXCI+RGF5czwvc3Bhbj48L3NwYW4+PC9kaXY+PGRpdiBjbGFzcz1cImNvdW50aW5nXCI+PHNwYW4gY2xhc3M9XCJDb3VudGRvd25Db250ZW50XCI+JUggPHNwYW4gY2xhc3M9XCJDb3VudGRvd25MYWJlbFwiPkhvdXJzPC9zcGFuPjwvc3Bhbj48L2Rpdj48ZGl2IGNsYXNzPVwiY291bnRpbmdcIj48c3BhbiBjbGFzcz1cIkNvdW50ZG93bkNvbnRlbnRcIj4lTSA8c3BhbiBjbGFzcz1cIkNvdW50ZG93bkxhYmVsXCI+TWludXRlczwvc3Bhbj48L3NwYW4+PC9kaXY+PGRpdiBjbGFzcz1cImNvdW50aW5nXCI+PHNwYW4gY2xhc3M9XCJDb3VudGRvd25Db250ZW50XCI+JVMgPHNwYW4gY2xhc3M9XCJDb3VudGRvd25MYWJlbFwiPlNlY29uZHM8L3NwYW4+PC9zcGFuPjwvZGl2PicpKTtcclxuICAgICAgICAgICAgICAgICAgICB9KTtcclxuICAgICAgICAgICAgICAgIH0pO1xyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgfSxcclxuXHJcbiAgICAgICAgLyo9PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT0qL1xyXG4gICAgICAgIC8qPSAgICAgICAgICAgR29vZ2xlIE1hcCAgICAgICAgICA9Ki9cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcblxyXG4gICAgICAgIGdvb2dsZU1hcDogZnVuY3Rpb24gKCkge1xyXG5cclxuICAgICAgICAgICAgJCgnLmdtYXAzLWFyZWEnKS5lYWNoKGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgIHZhciAkdGhpcyA9ICQodGhpcyksXHJcbiAgICAgICAgICAgICAgICAgICAga2V5ID0gJHRoaXMuZGF0YSgna2V5JyksXHJcbiAgICAgICAgICAgICAgICAgICAgbGF0ID0gJHRoaXMuZGF0YSgnbGF0JyksXHJcbiAgICAgICAgICAgICAgICAgICAgbG5nID0gJHRoaXMuZGF0YSgnbG5nJyksXHJcbiAgICAgICAgICAgICAgICAgICAgbXJrciA9ICR0aGlzLmRhdGEoJ21ya3InKSxcclxuICAgICAgICAgICAgICAgICAgICB6b29tID0gJHRoaXMuZGF0YSgnem9vbScpLFxyXG4gICAgICAgICAgICAgICAgICAgIHNjcm9sbHdoZWVsID0gJHRoaXMuZGF0YSgnc2Nyb2xsd2hlZWwnKSB8fCBmYWxzZTtcclxuXHJcbiAgICAgICAgICAgICAgICAkdGhpcy5nbWFwMyh7XHJcbiAgICAgICAgICAgICAgICAgICAgY2VudGVyOiBbbGF0LCBsbmddLFxyXG4gICAgICAgICAgICAgICAgICAgIHpvb206IHpvb20sXHJcbiAgICAgICAgICAgICAgICAgICAgc2Nyb2xsd2hlZWw6IHNjcm9sbHdoZWVsLFxyXG4gICAgICAgICAgICAgICAgICAgIG1hcFR5cGVJZDogZ29vZ2xlLm1hcHMuTWFwVHlwZUlkLlJPQURNQVAsXHJcbiAgICAgICAgICAgICAgICAgICAgc3R5bGVzOiBbe1xyXG4gICAgICAgICAgICAgICAgICAgICAgICBcImZlYXR1cmVUeXBlXCI6IFwiYWRtaW5pc3RyYXRpdmUuY291bnRyeVwiLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBcImVsZW1lbnRUeXBlXCI6IFwiZ2VvbWV0cnkuZmlsbFwiLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBcInN0eWxlcnNcIjogW3tcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIFwidmlzaWJpbGl0eVwiOiBcIm9uXCJcclxuICAgICAgICAgICAgICAgICAgICAgICAgfV1cclxuICAgICAgICAgICAgICAgICAgICB9XVxyXG4gICAgICAgICAgICAgICAgfSlcclxuICAgICAgICAgICAgICAgICAgICAubWFya2VyKGZ1bmN0aW9uIChtYXApIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBvc2l0aW9uOiBtYXAuZ2V0Q2VudGVyKCksXHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpY29uOiBtcmtyXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIH07XHJcbiAgICAgICAgICAgICAgICAgICAgfSlcclxuXHJcbiAgICAgICAgICAgIH0pO1xyXG5cclxuICAgICAgICB9LFxyXG5cclxuICAgICAgICAvKj09PT09PT09PT09PT09PT09PT09PT09PT09PSovXHJcbiAgICAgICAgLyo9ICAgICAgICAgICBGb3JtICAgICAgICAgID0qL1xyXG4gICAgICAgIC8qPT09PT09PT09PT09PT09PT09PT09PT09PT09Ki9cclxuXHJcbiAgICAgICAgY29udGFjdEZyb206IGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgJCgnW2RhdGEtYXBkYXNoLWZvcm1dJykuZWFjaChmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgICAgICB2YXIgJHRoaXMgPSAkKHRoaXMpO1xyXG4gICAgICAgICAgICAgICAgJCgnLmZvcm0tcmVzdWx0JywgJHRoaXMpLmNzcygnZGlzcGxheScsICdub25lJyk7XHJcblxyXG4gICAgICAgICAgICAgICAgJHRoaXMuc3VibWl0KGZ1bmN0aW9uICgpIHtcclxuICAgICAgICAgICAgICAgICAgICAkKCdidXR0b25bdHlwZT1cInN1Ym1pdFwiXScsICR0aGlzKS5hZGRDbGFzcygnY2xpY2tlZCcpO1xyXG4gICAgICAgICAgICAgICAgICAgIC8vIENyZWF0ZSBhIG9iamVjdCBhbmQgYXNzaWduIGFsbCBmaWVsZHMgbmFtZSBhbmQgdmFsdWUuXHJcbiAgICAgICAgICAgICAgICAgICAgdmFyIHZhbHVlcyA9IHt9O1xyXG5cclxuICAgICAgICAgICAgICAgICAgICAkKCdbbmFtZV0nLCAkdGhpcykuZWFjaChmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhciAkdGhpcyA9ICQodGhpcyksXHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkbmFtZSA9ICR0aGlzLmF0dHIoJ25hbWUnKSxcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICR2YWx1ZSA9ICR0aGlzLnZhbCgpO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZXNbJG5hbWVdID0gJHZhbHVlO1xyXG4gICAgICAgICAgICAgICAgICAgIH0pO1xyXG5cclxuICAgICAgICAgICAgICAgICAgICAvLyBNYWtlIFJlcXVlc3RcclxuICAgICAgICAgICAgICAgICAgICAkLmFqYXgoe1xyXG4gICAgICAgICAgICAgICAgICAgICAgICB1cmw6ICR0aGlzLmF0dHIoJ2FjdGlvbicpLFxyXG4gICAgICAgICAgICAgICAgICAgICAgICB0eXBlOiAnUE9TVCcsXHJcbiAgICAgICAgICAgICAgICAgICAgICAgIGRhdGE6IHZhbHVlcyxcclxuICAgICAgICAgICAgICAgICAgICAgICAgc3VjY2VzczogZnVuY3Rpb24gc3VjY2VzcyhkYXRhKSB7XHJcblxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaWYgKGRhdGEuZXJyb3IgPT0gdHJ1ZSkge1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICQoJy5mb3JtLXJlc3VsdCcsICR0aGlzKS5hZGRDbGFzcygnYWxlcnQtd2FybmluZycpLnJlbW92ZUNsYXNzKCdhbGVydC1zdWNjZXNzIGFsZXJ0LWRhbmdlcicpLmNzcygnZGlzcGxheScsICdibG9jaycpO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKCcuZm9ybS1yZXN1bHQnLCAkdGhpcykuYWRkQ2xhc3MoJ2FsZXJ0LXN1Y2Nlc3MnKS5yZW1vdmVDbGFzcygnYWxlcnQtd2FybmluZyBhbGVydC1kYW5nZXInKS5jc3MoJ2Rpc3BsYXknLCAnYmxvY2snKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH1cclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICQoJy5mb3JtLXJlc3VsdCA+IC5jb250ZW50JywgJHRoaXMpLmh0bWwoZGF0YS5tZXNzYWdlKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICQoJ2J1dHRvblt0eXBlPVwic3VibWl0XCJdJywgJHRoaXMpLnJlbW92ZUNsYXNzKCdjbGlja2VkJyk7XHJcblxyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29uc29sZS5sb2coXCJTdWNjZXNzXCIpO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICB9LFxyXG4gICAgICAgICAgICAgICAgICAgICAgICBlcnJvcjogZnVuY3Rpb24gZXJyb3IoKSB7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAkKCcuZm9ybS1yZXN1bHQnLCAkdGhpcykuYWRkQ2xhc3MoJ2FsZXJ0LWRhbmdlcicpLnJlbW92ZUNsYXNzKCdhbGVydC13YXJuaW5nIGFsZXJ0LXN1Y2Nlc3MnKS5jc3MoJ2Rpc3BsYXknLCAnYmxvY2snKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICQoJy5mb3JtLXJlc3VsdCA+IC5jb250ZW50JywgJHRoaXMpLmh0bWwoJ1NvcnJ5LCBhbiBlcnJvciBvY2N1cnJlZC4nKTtcclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICQoJ2J1dHRvblt0eXBlPVwic3VibWl0XCJdJywgJHRoaXMpLnJlbW92ZUNsYXNzKCdjbGlja2VkJyk7XHJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb25zb2xlLmxvZyhcIkVycm9yXCIpO1xyXG4gICAgICAgICAgICAgICAgICAgICAgICB9XHJcbiAgICAgICAgICAgICAgICAgICAgfSk7XHJcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIGZhbHNlO1xyXG4gICAgICAgICAgICAgICAgfSk7XHJcbiAgICAgICAgICAgIH0pO1xyXG4gICAgICAgIH1cclxuICAgIH07XHJcblxyXG4gICAgVEhFTUVUQUdTLmRvY3VtZW50T25SZWFkeSA9IHtcclxuICAgICAgICBpbml0OiBmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgIFRIRU1FVEFHUy5pbml0aWFsaXplLmluaXQoKTtcclxuICAgICAgICB9LFxyXG4gICAgfTtcclxuXHJcbiAgICBUSEVNRVRBR1MuZG9jdW1lbnRPbkxvYWQgPSB7XHJcbiAgICAgICAgaW5pdDogZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5oYW5kbGVNb2JpbGVIZWFkZXIoKTtcclxuICAgICAgICAgICAgJChcIiNwcmVsb2FkZXJcIikuZmFkZU91dChcInNsb3dcIik7XHJcbiAgICAgICAgfSxcclxuICAgIH07XHJcblxyXG4gICAgVEhFTUVUQUdTLmRvY3VtZW50T25SZXNpemUgPSB7XHJcbiAgICAgICAgaW5pdDogZnVuY3Rpb24gKCkge1xyXG4gICAgICAgICAgICBpZiAoJChcIiN3cGFkbWluYmFyXCIpLmxlbmd0aCAmJiAkKHdpbmRvdykud2lkdGgoKSA8IDc2OCkge1xyXG4gICAgICAgICAgICAgICAgJChcIiN3cGFkbWluYmFyXCIpLmNzcyh7XHJcbiAgICAgICAgICAgICAgICAgICAgcG9zaXRpb246IFwiZml4ZWRcIixcclxuICAgICAgICAgICAgICAgICAgICB0b3A6IFwiMFwiXHJcbiAgICAgICAgICAgICAgICB9KVxyXG4gICAgICAgICAgICB9XHJcbiAgICAgICAgICAgIFRULnJlc2l6ZSgpO1xyXG4gICAgICAgICAgICBUSEVNRVRBR1MuaW5pdGlhbGl6ZS5oYW5kbGVNb2JpbGVIZWFkZXIoKTtcclxuICAgICAgICAgICAgVEhFTUVUQUdTLmluaXRpYWxpemUuaGFuZGxlRml4ZWRIZWFkZXIoKTtcclxuICAgICAgICB9LFxyXG4gICAgfTtcclxuXHJcbiAgICBUSEVNRVRBR1MuZG9jdW1lbnRPblNjcm9sbCA9IHtcclxuICAgICAgICBpbml0OiBmdW5jdGlvbiAoKSB7XHJcbiAgICAgICAgICAgIFRIRU1FVEFHUy5pbml0aWFsaXplLmhhbmRsZUZpeGVkSGVhZGVyKCk7XHJcbiAgICAgICAgfSxcclxuICAgIH07XHJcbiAgICBUVC5pbml0KCk7XHJcbiAgICAvLyBJbml0aWFsaXplIEZ1bmN0aW9uc1xyXG4gICAgJChkb2N1bWVudCkucmVhZHkoVEhFTUVUQUdTLmRvY3VtZW50T25SZWFkeS5pbml0KTtcclxuICAgICQod2luZG93KS5vbignbG9hZCcsIFRIRU1FVEFHUy5kb2N1bWVudE9uTG9hZC5pbml0KTtcclxuICAgICQod2luZG93KS5vbigncmVzaXplJywgVEhFTUVUQUdTLmRvY3VtZW50T25SZXNpemUuaW5pdCk7XHJcbiAgICAkKHdpbmRvdykub24oJ3Njcm9sbCcsIFRIRU1FVEFHUy5kb2N1bWVudE9uU2Nyb2xsLmluaXQpO1xyXG5cclxufSkoalF1ZXJ5KTtcclxuXHJcbiJdLCJzb3VyY2VSb290IjoiIn0=