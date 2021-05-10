$(document).ready(function(){
    $(window).scroll(function(){
        // sticky navbar on scroll script
        if(this.scrollY > 20){
            $('.navbar').addClass("sticky");
        }else{
            $('.navbar').removeClass("sticky");
        }

        // scroll-up button show/hide script
        if(this.scrollY > 500){
            $('.scroll-up-btn').addClass("show");
        }else{
            $('.scroll-up-btn').removeClass("show");
        }
    });

    // slide-up script
    $('.scroll-up-btn').click(function(){
        $('html').animate({scrollTop: 0});
        // removing smooth scroll on slide-up button click
        $('html').css("scrollBehavior", "auto");
    });

    $('.navbar .menu li a').click(function(){
        // applying again smooth scroll on menu items click
        $('html').css("scrollBehavior", "smooth");
    });

    // toggle menu/navbar script
    $('.menu-btn').click(function(){
        $('.navbar .menu').toggleClass("active");
        $('.menu-btn i').toggleClass("active");
    });


     // var someVar = document.getElementById("myvar").innerHTML;
      var someVar = document.getElementById("myvar").value;
     console.log(someVar)


    var a = someVar;

    a = a.replace(/'/g, '"');
    console.log(a)
    a = JSON.parse(a);


    var someVar1 = document.getElementById("myvar1").value;
     console.log(someVar1)


    var b = someVar1;

    b = b.replace(/'/g, '"');
    console.log(b)
    b = JSON.parse(b);



    var typed = new Typed(".typing", {

        strings: a,
        typeSpeed: 100,
        backSpeed: 60,
        loop: true
    });


    var typed = new Typed(".typing-2", {
        strings: b,
        typeSpeed: 100,
        backSpeed: 60,
        loop: true
    });

    // owl carousel script
    $('.carousel').owlCarousel({
        navigation : true,
        margin: 20,
        loop: true,
        autoplayTimeOut: 2000,
        autoplayHoverPause: true,
        responsive: {
            0:{
                items: 1,
                nav: false
            },
            600:{
                items: 2,
                nav: false
            },
            1000:{
                items: 3,
                nav: false
            }
        }
    });
});

// var slideIndex = 1;
// showSlides(slideIndex);
//
// function plusSlides(n) {
//   showSlides(slideIndex += n);
// }
//
// function currentSlide(n) {
//   showSlides(slideIndex = n);
// }
//
// function showSlides(n) {
//   var i;
//   var slides = document.getElementsByClassName("mySlides");
//   var dots = document.getElementsByClassName("dot");
//   if (n > slides.length) {slideIndex = 1}
//   if (n < 1) {slideIndex = slides.length}
//   for (i = 0; i < slides.length; i++) {
//       slides[i].style.display = "none";
//   }
//   for (i = 0; i < dots.length; i++) {
//       dots[i].className = dots[i].className.replace(" active", "");
//   }
//   slides[slideIndex-1].style.display = "block";
//   dots[slideIndex-1].className += " active";
// }
//

// var i = 0;
// var images = []; //array
// var time = 3000; // time in millie seconds
//
// //images
//
// images[0] = "url(http://127.0.0.1:8000/static/hero.jpg)";
// images[1] = "url(http://127.0.0.1:8000/static/main.jpg)";
// images[2] = "url(http://127.0.0.1:8000/static/hero.jpg)";
// //function
//
// function changeImage() {
//     var el = document.getElementById('home');
//     el.style.backgroundImage = images[i];
//     if (i < images.length - 1) {
//         i++;
//     } else {
//         i = 0;
//     }
//     setTimeout('changeImage()', time);
// }

// window.onload = changeImage;

// $(document).ready(function() {
//
//   $("#myvar").children().prop('disabled', true);
// });





//  var img_link = document.getElementById("main_img").value;
//  img_link="http://127.0.01:8000"+img_link
//  console.log( "http://127.0.0.1:8000"+img_link)
// // http://127.0.0.1:8000/media/images/Screenshot_59.png
//  function changeImg(){
//      var el = document.getElementById('home');
//      el.style.backgroundImage = "url("+img_link+")"
//
//  }


function login() {
     $("#login").trigger('click');
}
window.onload = login;


