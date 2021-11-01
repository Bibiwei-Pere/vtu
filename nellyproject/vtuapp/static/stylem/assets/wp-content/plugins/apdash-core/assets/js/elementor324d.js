(function ($, elementor) {
    "use strict";

    var Apdash = {

        init: function () {

            var widgets = {
                'tt-hero-static.default': Apdash.Banner,
                'at-coming-soon.default': Apdash.ComingSoon,
                'tt-screenshots.default': Apdash.Slider,
                'tt-pricing-table.default': Apdash.Pricing,
                'tt-google-map.default': Apdash.GoogleMap,
                'tt-testimonial.default': Apdash.Testimonial,
                'tt-testimonial-two.default': Apdash.TestimonialTwo,
                'tt-banner-slider.default': Apdash.BannerSlider,
                'tt-logo-carousel.default': Apdash.Logo,
                'tt-pricing-slider.default': Apdash.VpsSlider,
            };
            $.each(widgets, function (widget, callback) {
                elementor.hooks.addAction('frontend/element_ready/' + widget, callback);
            });

        },

        Pricing: function ($scope) {
            // var element = $scope.find('#js-contcheckbox');
            // element.change(function () {
            //     if (this.checked) {
            //         $('.yearly-price').css('display', 'none');
            //         $('.monthly-price').css('display', 'block');
            //         // $('.afterinput').addClass('active');
            //         $('.pricing-switch-wrap').removeClass('yearly');
            //         // $('.beforeinput').removeClass('active');


            //     } else {
            //         $('.pricing-switch-wrap').addClass('yearly');
            //         $('.yearly-price').css('display', 'block');
            //         $('.monthly-price').css('display', 'none');
            //         // $('.afterinput').removeClass('active');
            //         // $('.beforeinput').addClass('active');
            //     }
            // });


            // var element = $scope.find('#js-contcheckbox');
            // element.change(function () {
            //     if (this.checked) {
			// 	    $('.monthly-price').css('display', 'none');
			// 	    $('.yearly-price').css('display', 'block');
            //         $('.pricing-switch-wrap').addClass('yearly');	
            //         $('.pricing-switch-wrap').removeClass('monthly');			
			// 	} else {
			// 	    $('.monthly-price').css('display', 'block');
			// 	    $('.yearly-price').css('display', 'none');
            //         $('.pricing-switch-wrap').removeClass('yearly');
            //         $('.pricing-switch-wrap').addClass('monthly');					
			// 	}
            // });

              var element = $scope.find('#js-contcheckbox');
              element.change(function () {
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

        },

        GoogleMap: function ($scope) {
            var map = $scope.find('.gmap3-area');

            map.each(function () {
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
                })
                // .marker(function (map) {
                //     return {
                //         position: map.getCenter(),
                //         icon: mrkr
                //     };
                // })

            });

        },

        Banner: function ($scope) {
            var counting = $scope.find('.countdown');

            counting.each(function (index, value) {
                var count_year = $(this).attr("data-count-year");
                var count_month = $(this).attr("data-count-month");
                var count_day = $(this).attr("data-count-day");
                var count_date = count_year + '/' + count_month + '/' + count_day;
                $(this).countdown(count_date, function (event) {
                    $(this).html(
                        event.strftime('<div class="counting"><span class="CountdownContent">%D<span class="CountdownLabel">Days</span></span><span class="CountdownSeparator">:</span></div><div class="counting"><span class="CountdownContent">%H <span class="CountdownLabel">Hours</span></span><span class="CountdownSeparator">:</span></div><div class="counting"><span class="CountdownContent">%M <span class="CountdownLabel">Minutes</span></span><span class="CountdownSeparator">:</span></div><div class="counting"><span class="CountdownContent">%S <span class="CountdownLabel">Seconds</span></span></div>')
                    );
                });
            });
        },

        ComingSoon: function ($scope) {
            var counting = $scope.find('.countdown');

            counting.each(function (index, value) {
                var count_year = $(this).attr("data-count-year");
                var count_month = $(this).attr("data-count-month");
                var count_day = $(this).attr("data-count-day");
                var count_date = count_year + '/' + count_month + '/' + count_day;
                $(this).countdown(count_date, function (event) {
                    $(this).html(
                        event.strftime('<div class="counting"><span class="CountdownContent">%D<span class="CountdownLabel">Days</span></span><span class="CountdownSeparator">:</span></div><div class="counting"><span class="CountdownContent">%H <span class="CountdownLabel">Hours</span></span><span class="CountdownSeparator">:</span></div><div class="counting"><span class="CountdownContent">%M <span class="CountdownLabel">Minutes</span></span><span class="CountdownSeparator">:</span></div><div class="counting"><span class="CountdownContent">%S <span class="CountdownLabel">Seconds</span></span></div>')
                    );
                });
            });
        },


        Slider: function ($scope) {
            var slideInit = $scope.find('[data-swiper]');

            slideInit.each(function () {
                var swps = document.querySelectorAll('[data-swiper]');

                if (swps.length > 0) {
                    swps.forEach(function (swp) {
                        var config = JSON.parse(swp.getAttribute('data-swiper'));
                        var mySwiper = new Swiper(swp, config);

                        $('.swiper-slide').on('mouseover', function () {
                            mySwiper.autoplay.stop();
                        });

                        $('.swiper-slide').on('mouseout', function () {
                            mySwiper.autoplay.start();
                        });
                    });

                }
            });
        },


        Testimonial: function ($scope) {

            var slideInit = $scope.find('[data-testi]');

            slideInit.each(function () {
                var swps = document.querySelectorAll('[data-testi]');

                if (swps.length > 0) {
                    swps.forEach(function (swp) {
                        var config = JSON.parse(swp.getAttribute('data-testi'));
                        var mySwiper = new Swiper(swp, config);

                        $('.swiper-slide').on('mouseover', function () {
                            mySwiper.autoplay.stop();
                        });

                        $('.swiper-slide').on('mouseout', function () {
                            mySwiper.autoplay.start();
                        });
                    });

                }


            });
        },

        TestimonialTwo: function ($scope) {
            var slideInit = $scope.find('[data-testi]');

            slideInit.each(function () {
                var swps = document.querySelectorAll('[data-testi]');

                if (swps.length > 0) {
                    swps.forEach(function (swp) {
                        var config = JSON.parse(swp.getAttribute('data-testi'));
                        var mySwiper = new Swiper(swp, config);

                        $('.swiper-slide').on('mouseover', function () {
                            mySwiper.autoplay.stop();
                        });

                        $('.swiper-slide').on('mouseout', function () {
                            mySwiper.autoplay.start();
                        });
                    });
                }
            });
        },

        BannerSlider: function ($scope) {
            var slider = $scope.find('.banner__slider');

            slider.each(function () {
            let mainSliderSelector = '.banner__slider',
            interleaveOffset = 0.5;

            var loop = $(this).data('loop') || true,
            direction = $(this).data('direction') || 'vertical',
            speed = $(this).data('speed') || 1000,
            autoplay = $(this).data('autoplay') || 5000;

            let mainSliderOptions = {
                slidesPerView: 1,
                loop: loop,
                    // direction: direction,
                    speed: speed,
                    // loopAdditionalSlides: 10,
                    watchSlidesProgress: true,
                    autoplay: {
                        delay: autoplay
                    },
                    // mousewheel: {
                    //     invert: false,
                    // },

                    // navigation: {
                    //     nextEl: '.swiper_prev',
                    //     prevEl: '.swiper_next',
                    // },
                    pagination: {
                        el: '.pagination-banner',
                        clickable: true,
                    },
                    on: {
                        init: function () {
                            this.autoplay.stop();
                        },
                        // progress: function () {
                        //     let swiper = this;
                        //     for (let i = 0; i < swiper.slides.length; i++) {
                        //         let slideProgress = swiper.slides[i].progress,
                        //         innerOffset = swiper.width * interleaveOffset,
                        //         innerTranslate = slideProgress * innerOffset;
                        //         swiper.slides[i].querySelector(".banner__image").style.transform =
                        //         "translate3d(" + innerTranslate + "px, 0, 0)";
                        //     }
                        // },
                        // touchStart: function () {
                        //     let swiper = this;
                        //     for (let i = 0; i < swiper.slides.length; i++) {
                        //         swiper.slides[i].style.transition = "";
                        //     }
                        // },
                        // setTransition: function (speed) {
                        //     let swiper = this;
                        //     for (let i = 0; i < swiper.slides.length; i++) {
                        //         swiper.slides[i].style.transition = speed + "ms";
                        //         swiper.slides[i].querySelector(".banner__image").style.transition =
                        //         speed + "ms";
                        //     }
                        // }
                    }
                };
                let mainSlider = new Swiper(slider, mainSliderOptions);
            });
        },

        VpsSlider: function($scope) {
            // var cPlan = $('#c-plan');

            var cPlan = $scope.find('#c-plan');

            if (cPlan.length) {
    
                cPlan.slider({
                    tooltip: 'always'
                });
                cPlan.on("slide", function (e) {
    
                    $.each(vpsPriceInfo, function (index, vpsObj) {
                        if (vpsObj.vpsCore == e.value) {
                            setVpsValue(vpsObj);
                        }
                    });
                });
    
                initSlider();
            }
    
            function initSlider() {
    
    
                cPlan.value = cPlan.data("slider-value");
                var defaultVpsCore = parseInt(cPlan.value);
                $.each(vpsPriceInfo, function (index, vpsObj) {
                    // defaultVpsCore is default valeu to show. For my demo, I have set 6 from HTML.
                    // vps-hosting.html: <input id="c-plan" type="text" data-slider-min="1" data-slider-max="12" data-slider-step="1" data-slider-value="6" data-currency="$" data-unit="GB">. 
                    // You need to change accourting to your need.
                    if (vpsObj.vpsCore == defaultVpsCore) {
                        $('.slider .tooltip', '#custom-plan').append('<div class="tooltip-up"></div>');
                        $('.slider .tooltip-inner', '#custom-plan').attr("data-unit", cPlan.data("unit"));
                        $('.slider .tooltip-up', '#custom-plan').attr("data-currency", cPlan.data("currency"));
                        setVpsValue(vpsObj);
                    }
                });
            }
    
            function setVpsValue(vpsObj) {
                $('.slider .tooltip-up', '#custom-plan').text(vpsObj.vpsCore);
                $('.vpsPrice', '#custom-plan').text(cPlan.data("currency") + vpsObj.vpsPrice);
                $('.vpsCore span', '#custom-plan').text(vpsObj.vpsCore);
                $('.vpsMemory span', '#custom-plan').text(vpsObj.vpsMemory);
                $('.vpsStorage span', '#custom-plan').text(vpsObj.vpsStorage);
                $('.vpsBandwidth span', '#custom-plan').text(vpsObj.vpsBandwidth);
                $('.vpsWHmcsUrl', '#custom-plan').attr("href", vpsObj.vpsWHmcsUrl);
            }
        },



        Logo: function ($scope) {

            var slideInit = $scope.find('[data-logo]');

            slideInit.each(function () {
                var swps = document.querySelectorAll('[data-logo]');

                if (swps.length > 0) {
                    swps.forEach(function (swp) {
                        var config = JSON.parse(swp.getAttribute('data-logo'));
                        var mySwiper = new Swiper(swp, config);

                        $('.swiper-slide').on('mouseover', function () {
                            mySwiper.autoplay.stop();
                        });

                        $('.swiper-slide').on('mouseout', function () {
                            mySwiper.autoplay.start();
                        });
                    });

                }


            });
        },


    };
    $(window).on('elementor/frontend/init', Apdash.init);
}(jQuery, window.elementorFrontend));