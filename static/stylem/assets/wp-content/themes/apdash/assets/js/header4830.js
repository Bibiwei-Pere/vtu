/* accordion menu plugin*/ ;
// (function ($, window, document, undefined) {
// 	"use strict";
//
// 	var pluginName = "mobileMenu";
// 	var defaults = {
// 		speed: 400,
// 		showDelay: 0,
// 		hideDelay: 0,
// 		singleOpen: true,
// 		clickEffect: true,
// 		indicator: 'active',
// 		subMenu: 'sub-menu',
// 		subMenu2: 'sub-menu',
// 		event: 'click touchstart' // click, touchstart
// 	};
//
// 	function Plugin(element, options) {
// 		this.element = element;
// 		this.settings = $.extend({}, defaults, options);
// 		this._defaults = defaults;
// 		this._name = pluginName;
// 		this.init();
// 	}
// 	$.extend(Plugin.prototype, {
// 		init: function () {
// 			this.openSubmenu();
// 			// this.submenuIndicators();
// 			if (defaults.clickEffect) {
// 				this.addClickEffect();
// 			}
// 		},
// 		openSubmenu: function () {
// 			$(this.element).children(".site-main-menu").find("li").bind(defaults.event, function (e) {
// 				e.stopPropagation();
// 				e.preventDefault();
// 				var $subMenus = $(this).children("." + defaults.subMenu);
// 				var $allSubMenus = $(this).find("." + defaults.subMenu);
// 				if ($subMenus.length > 0) {
// 					if ($subMenus.css("display") == "none") {
// 						$subMenus.slideDown(defaults.speed).siblings("a").addClass(defaults.indicator);
// 						if (defaults.singleOpen) {
// 							$(this).siblings().find("." + defaults.subMenu).slideUp(defaults.speed)
// 								.end().find("a").removeClass(defaults.indicator);
// 						}
// 						return false;
// 					} else {
// 						$(this).find("." + defaults.subMenu).delay(defaults.hideDelay).slideUp(defaults.speed);
// 					}
// 					if ($allSubMenus.siblings("a").hasClass(defaults.indicator)) {
// 						$allSubMenus.siblings("a").removeClass(defaults.indicator);
// 					}
// 				}
// 				// window.location.href = $(this).children("a").attr("href");
//
//
//                 var attr = $(this).children("a").attr('target');
//
//                 var openPageUrl = $(this).children("a").attr("href");
//                 var openPageUrl2 = $(this).find('a').attr("href");
//
//
// 				var openPageUrl = $(this).children("a").attr("href") || $(this).find('.tt-menu-item a').attr("href");
//
// 				console.log(openPageUrl2);
//
// 				console.log(openPageUrl);
//
//                 if (attr && attr.toLowerCase() == '_blank') {
//                     window.open(openPageUrl, '_blank');
//                 } else {
//                     window.location.href = openPageUrl;
//                 }
// 			});
// 		},
//
// 		addClickEffect: function () {
// 			var ink, d, x, y;
// 			$(this.element).find("a").bind("click touchstart", function (e) {
// 				$(".ink").remove();
// 				if ($(this).children(".ink").length === 0) {
// 					$(this).prepend("<span class='ink'></span>");
// 				}
// 				ink = $(this).find(".ink");
// 				ink.removeClass("animate-ink");
// 				if (!ink.height() && !ink.width()) {
// 					d = Math.max($(this).outerWidth(), $(this).outerHeight());
// 					ink.css({
// 						height: d,
// 						width: d
// 					});
// 				}
// 				x = e.pageX - $(this).offset().left - ink.width() / 2;
// 				y = e.pageY - $(this).offset().top - ink.height() / 2;
// 				ink.css({
// 					top: y + 'px',
// 					left: x + 'px'
// 				}).addClass("animate-ink");
// 			});
// 		}
// 	});
// 	$.fn[pluginName] = function (options) {
// 		this.each(function () {
// 			if (!$.data(this, "plugin_" + pluginName)) {
// 				$.data(this, "plugin_" + pluginName, new Plugin(this, options));
// 			}
// 		});
// 		return this;
// 	};
//
// 	$(".menu-primary-menu-container").mobileMenu();
//
//
// })(jQuery, window, document);

(function($, window, document) {
	"use strict";

	// $(window).on("scroll load", function() {
	// 	if ($(this).scrollTop() >= 30) {
	// 		if ($(".site-header.header_trans-fixed").length) {
	// 			$(".site-header.header_trans-fixed").not(".fixed-dark").addClass("pix-header-fixed");
	// 			$(".fixed-dark").addClass("bg-fixed-dark");
	// 			$(".sticky-logo, .header-button-scroll").show();
	// 			$(".main-logo, .header-button-default").hide()
	// 		}
	// 		if ($(".right-menu.modern").length) {
	// 			$(".right-menu.modern").closest(".fixed-header").addClass("fixed-header-scroll")
	// 		}
	// 	} else {
	// 		if ($(".site-header.header_trans-fixed").length) {
	// 			$(".site-header.header_trans-fixed").not(".fixed-dark").removeClass("pix-header-fixed");
	// 			$(".fixed-dark").removeClass("bg-fixed-dark");
	// 			$(".sticky-logo, .header-button-scroll").hide();
	// 			$(".main-logo, .header-button-default").show()
	// 		}
	// 		if ($(".right-menu.modern").length) {
	// 			$(".right-menu.modern").closest(".fixed-header").removeClass("fixed-header-scroll")
	// 		}
	// 	}
	// });


	// if ($(window).width() >= $(".menu-wrapper").data("top")) {
	// 	$('.site-main-menu li:not(.menu-item-has-children) > a[href^="#"]').on("click", function(e) {
	// 		e.preventDefault();
	// 		var elem = $(this).attr("href");
	// 		if ($(elem).length) {
	// 			$("html,body").animate({
	// 				scrollTop: $(elem).offset().top - $(".header_trans-fixed").outerHeight() - $("#wpadminbar").outerHeight()
	// 			}, "slow")
	// 		}
	// 	})
	// }

	// $(".toggle-menu").on("click", function(e) {
	// 	e.preventDefault();
	// 	$("html").addClass("no-scroll sidebar-open").height(window.innerHeight + "px");
	// 	if ($("#wpadminbar").length) {
	// 		$(".sidebar-open .site-nav").css("top", "46px")
	// 	} else {
	// 		$(".sidebar-open .site-nav").css("top", "0")
	// 	}
	// });


	// if ($('body').hasClass("admin-bar")) {
	// 	$('body').addClass('header-position');
	// }


	// $(".close-menu").on("click", function(e) {
	// 	e.preventDefault();
	// 	$("html").removeClass("no-scroll sidebar-open").height("auto")
	// });

	function menuArrows() {
		// var mobW = $(".site-header").attr("data-mobile-menu-resolution");
		var mobW = $(".site-header").attr("data-mobile-menu-resolution");
		// if ( $(".site-header").hasClass("mobile-header") ) {
		if (window.outerWidth < mobW || $(".site-header").hasClass(".mobile-header")) {
			if (!$(".site-header .menu-item-has-children i.ti-plus").length) {
				$(".site-header .menu-item-has-children").append('<i class="ti-plus"></i>');
				$(".site-header .menu-item-has-children i.ti-plus").addClass("hide-drop");
			}

			$(".site-header .menu-item-has-children i.ti-plus").on("click", function() {
				if (!$(this).hasClass("animation")) {
					$(this).parent().toggleClass("is-open");
					$(this).addClass("animation");
					$(this).parent().siblings().removeClass("is-open").find(".fa").removeClass("hide-drop").prev(".sub-menu").slideUp(250);
					if ($(this).hasClass("hide-drop")) {
						if ($(this).closest(".sub-menu").length) {
							$(this).removeClass("hide-drop").prev(".sub-menu").slideToggle(250)
						} else {
							$(".site-header .menu-item-has-children i").addClass("hide-drop").next(".sub-menu").hide(250);
							$(this).removeClass("hide-drop").prev(".sub-menu").slideToggle(250)
						}
					} else {
						$(this).addClass("hide-drop").prev(".sub-menu").hide(100).find(".site-header .menu-item-has-children a").addClass("hide-drop").prev(".sub-menu").hide(250)
					}
				}

				setTimeout(removeClass, 250);

				function removeClass() {
					$(".site-header .site-main-menu i.ti-plus").removeClass("animation")
				}

			})
		} else {
			$(".site-header .menu-item-has-children i.ti-plus").remove()
		}
	}




	$(".additional-nav").on("click", function(e) {
		e.preventDefault();
		$(".additional-menu-wrapper").addClass("menu-open");
		$(".menu-wrapper").addClass("additional-menu-open")
	});
	$(".additional-nav-close, .additional-menu-overlay").on("click", function() {
		$(".additional-menu-wrapper").removeClass("menu-open");
		$(".menu-wrapper").removeClass("additional-menu-open")
	});

	$(window).on("load resize", function() {
		menuArrows();
	});
	// window.addEventListener("orientationchange", function() {
	// 	menuArrows()
	// });
})(jQuery, window, document);