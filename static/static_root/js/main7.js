/*  ---------------------------------------------------
    Template Name: Fashi
    Description: Fashi eCommerce HTML Template
    Author: Colorlib
    Author URI: https://colorlib.com/
    Version: 1.0
    Created: Colorlib
---------------------------------------------------------  */

"use strict";

(function ($) {
  /*------------------
        Preloader
    --------------------*/
  $(window).on("load", function () {
    $(".loader").fadeOut();
    $("#preloder").delay(200).fadeOut("slow");
  });

  /*------------------
        Background Set
    --------------------*/
  $(".set-bg").each(function () {
    var bg = $(this).data("setbg");
    $(this).css("background-image", "url(" + bg + ")");
  });

  /*------------------
		Navigation
	--------------------*/
  $(".mobile-menu").slicknav({
    prependTo: "#mobile-menu-wrap",
    allowParentLinks: true,
  });

  /*------------------
        Hero Slider
    --------------------*/
  $(".hero-items").owlCarousel({
    loop: true,
    margin: 0,
    nav: true,
    items: 1,
    dots: false,
    animateOut: "fadeOut",
    animateIn: "fadeIn",
    navText: [
      '<i class="ti-angle-left"></i>',
      '<i class="ti-angle-right"></i>',
    ],
    smartSpeed: 1200,
    autoHeight: false,
    autoplay: true,
  });

  /*------------------
        Product Slider
    --------------------*/
  $(".product-slider").owlCarousel({
    loop: true,
    margin: 25,
    nav: true,
    items: 4,
    dots: true,
    navText: [
      '<i class="ti-angle-left"></i>',
      '<i class="ti-angle-right"></i>',
    ],
    smartSpeed: 1200,
    autoHeight: false,
    autoplay: true,
    responsive: {
      0: {
        items: 1,
      },
      576: {
        items: 2,
      },
      992: {
        items: 2,
      },
      1200: {
        items: 3,
      },
    },
  });

  /*------------------
       logo Carousel
    --------------------*/
  $(".logo-carousel").owlCarousel({
    loop: false,
    margin: 30,
    nav: false,
    items: 5,
    dots: false,
    navText: [
      '<i class="ti-angle-left"></i>',
      '<i class="ti-angle-right"></i>',
    ],
    smartSpeed: 1200,
    autoHeight: false,
    mouseDrag: false,
    autoplay: true,
    responsive: {
      0: {
        items: 3,
      },
      768: {
        items: 5,
      },
    },
  });

  /*-----------------------
       Product Single Slider
    -------------------------*/
  $(".ps-slider").owlCarousel({
    loop: false,
    margin: 10,
    nav: true,
    items: 3,
    dots: false,
    navText: [
      '<i class="fa fa-angle-left"></i>',
      '<i class="fa fa-angle-right"></i>',
    ],
    smartSpeed: 1200,
    autoHeight: false,
    autoplay: true,
  });

  /*------------------
        CountDown
    --------------------*/
  // For demo preview
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, "0");
  var mm = String(today.getMonth() + 1).padStart(2, "0"); //January is 0!
  var yyyy = today.getFullYear();

  if (mm == 12) {
    mm = "01";
    yyyy = yyyy + 1;
  } else {
    mm = parseInt(mm) + 1;
    mm = String(mm).padStart(2, "0");
  }
  var timerdate = mm + "/" + dd + "/" + yyyy;
  // For demo preview end

  console.log(timerdate);

  // Use this for real timer date
  /* var timerdate = "2020/01/01"; */

  $("#countdown").countdown(timerdate, function (event) {
    $(this).html(
      event.strftime(
        "<div class='cd-item'><span>%D</span> <p>Days</p> </div>" +
        "<div class='cd-item'><span>%H</span> <p>Hrs</p> </div>" +
        "<div class='cd-item'><span>%M</span> <p>Mins</p> </div>" +
        "<div class='cd-item'><span>%S</span> <p>Secs</p> </div>"
      )
    );
  });

  /*----------------------------------------------------
     Language Flag js
    ----------------------------------------------------*/
  $(document).ready(function (e) {
    //no use
    try {
      var pages = $("#pages")
        .msDropdown({
          on: {
            change: function (data, ui) {
              var val = data.value;
              if (val != "") window.location = val;
            },
          },
        })
        .data("dd");

      var pagename = document.location.pathname.toString();
      pagename = pagename.split("/");
      pages.setIndexByValue(pagename[pagename.length - 1]);
      $("#ver").html(msBeautify.version.msDropdown);
    } catch (e) {
      // console.log(e);
    }
    $("#ver").html(msBeautify.version.msDropdown);

    //convert
    $(".language_drop").msDropdown({
      roundedBorder: false
    });
    $("#tech").data("dd");
  });
  /*-------------------
		Range Slider
	--------------------- */
  var rangeSlider = $(".price-range"),
    minamount = $("#minamount"),
    maxamount = $("#maxamount"),
    minPrice = rangeSlider.data("min"),
    maxPrice = rangeSlider.data("max");
  rangeSlider.slider({
    range: true,
    min: minPrice,
    max: maxPrice,
    values: [minPrice, maxPrice],
    slide: function (event, ui) {
      minamount.val(ui.values[0]);
      maxamount.val(ui.values[1]);
    },
  });
  minamount.val(rangeSlider.slider("values", 0));
  maxamount.val(rangeSlider.slider("values", 1));

  /*-------------------
		Radio Btn
	--------------------- */
  $(".fw-size-choose .sc-item label, .pd-size-choose .sc-item label").on(
    "click",
    function () {
      $(
        ".fw-size-choose .sc-item label, .pd-size-choose .sc-item label"
      ).removeClass("active");
      $(this).addClass("active");
    }
  );

  /*-------------------
		Nice Select
    --------------------- */
  $(".sorting, .p-show").niceSelect();

  /*------------------
		Single Product
	--------------------*/
  $(".product-thumbs-track .pt").on("click", function () {
    $(".product-thumbs-track .pt").removeClass("active");
    $(this).addClass("active");
    var imgurl = $(this).data("imgbigurl");
    var bigImg = $(".product-big-img").attr("src");
    if (imgurl != bigImg) {
      $(".product-big-img").attr({
        src: imgurl
      });
      $(".zoomImg").attr({
        src: imgurl
      });
    }
  });

  $(".product-pic-zoom").zoom();

  /*-------------------
		Quantity change
	--------------------- */
  var proQty = $(".pro-qty");
  proQty.prepend('<span class="dec qtybtn">-</span>');
  proQty.append('<span class="inc qtybtn">+</span>');
  proQty.on("click", ".qtybtn", function () {
    var $button = $(this);
    var oldValue = $button.parent().find("input").val();
    if ($button.hasClass("inc")) {
      var newVal = parseFloat(oldValue) + 1;
    } else {
      // Don't allow decrementing below zero
      if (oldValue > 0) {
        var newVal = parseFloat(oldValue) - 1;
      } else {
        newVal = 0;
      }
    }
    $button.parent().find("input").val(newVal);
  });
})(jQuery);

/*-------------------
  Sorting
--------------------- */
$(document).ready(function () {
  $("#block-btn").click(function () {
    $("#straight-sorting").hide();
    $("#block-sorting").show();
    $("#straight-btn").css("background-color", "#ffffff");
    $("#block-btn").css("background-color", "#f6f6f6");
  });
  $("#straight-btn").click(function () {
    $("#block-sorting").hide();
    $("#straight-sorting").show();
    $("#straight-btn").css("background-color", "#f6f6f6");
    $("#block-btn").css("background-color", "#ffffff");
  });
});

/*-------------------
  filter-catagories
 --------------------- */
$(document).ready(function () {
  $(".list-btn")
    .hover(function () {
      cursorChange(this);
    })
    .click(function () {
      foldToggle(this);
      turnArrow(this);
    })
    .trigger("click");
});

function foldToggle(element) {
  $(element).next("ul").slideToggle();
}

function cursorChange(element, cursorType) {
  $(element).css("cursor", "pointer");
}

function turnArrow(element) {
  if ($(element).hasClass("before-active")) {
    $(element).removeClass("before-active");
    $(element).addClass("after-active");
  } else {
    $(element).removeClass("after-active");
    $(element).addClass("before-active");
  }
}

/*-------------------
		rating
  --------------------- */
$(document).ready(function () {
  $(".rating-star").click(function () {
    clickFillStar(this);
    starNumer(this);
  });
});

function clickFillStar(element) {
  if ($(element).hasClass("fa-star-o")) {
    $(element).removeClass("fa-star-o");
    $(element).addClass("fa-star");
  }
  if ($(element).nextAll().hasClass("fa-star")) {
    $(element).nextAll().removeClass("fa-star");
    $(element).nextAll().addClass("fa-star-o");
  }
  if ($(element).prevAll().hasClass("fa-star-o")) {
    $(element).prevAll().removeClass("fa-star-o");
    $(element).prevAll().addClass("fa-star");
  }
}

function starNumer(element) {
  var n = $(element).prevAll("i").length + 1;
  if ($(element).attr("id") == "price-star") {
    $("#price-rating").val(n);
    $("#price-rating-span").text(n);
  }
  if ($(element).attr("id") == "store-star") {
    $("#store-rating").val(n);
    $("#store-rating-span").text(n);
  }
  if ($(element).attr("id") == "delivery-star") {
    $("#delivery-rating").val(n);
    $("#delivery-rating-span").text(n);
  }
}

window.onload = function setStarNumber() {
  $(document).ready(function () {
    $(".pd-rating .rating-point").each(function () {
      var n = $(this).text();
      var rounded = (n | 0)
      var decimal = n - rounded
      if (decimal) {
        for (var j = 0; j < 4 - rounded; j++) {
          $(this).after("<i class='fa fa-star-o'></i>")
        }
        $(this).after("<i class='fa fa-star-half-o'></i>");
      } else {
        for (var j = 0; j < 5 - rounded; j++) {
          $(this).after("<i class='fa fa-star-o'></i>")
        }
      }
      for (var i = 0; i < rounded; i++) {
        $(this).after("<i class='fa fa-star'></i>")
      }
    });
    $(".at-rating .rating-point").each(function () {
      var n = $(this).text();
      var rounded = (n | 0)
      var decimal = n - rounded
      if (decimal) {
        for (var j = 0; j < 4 - rounded; j++) {
          $(this).after("<i class='fa fa-star-o'></i>")
        }
        $(this).after("<i class='fa fa-star-half-o'></i>");
      } else {
        for (var j = 0; j < 5 - rounded; j++) {
          $(this).after("<i class='fa fa-star-o'></i>")
        }
      }
      for (var i = 0; i < rounded; i++) {
        $(this).after("<i class='fa fa-star'></i>")
      }
    });
  });
};

/*-------------------
		icon-heart
  --------------------- */

$(document).ready(function () {
  $(".favorite-heart-icon").click(function () {
    clickHeart(this);
  });
});

function clickHeart(element) {
  if ($(element).hasClass("icon_heart_alt")) {
    $(element).removeClass("icon_heart_alt");
    $(element).addClass("icon_heart");
  } else {
    $(element).removeClass("icon_heart");
    $(element).addClass("icon_heart_alt");
  }
}

/*-------------------
		show-messages
  --------------------- */

toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": false,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": false,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "1000",
  "extendedTimeOut": "5000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

/*-------------------
		search-empty
  --------------------- */

$(document).ready(function () {
  $(".search-submit").click(function () {
    if ($(".search-text").val() == "") {
      $(".search-text").val("口紅");
    }
  });
});

$(document).ready(function () {
  $(".search-submit").submit(function () {
    if ($(".search-text").val() == "") {
      $(".search-text").val("口紅");
    }
  });
});