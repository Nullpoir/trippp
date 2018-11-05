$(document).on("click",".sp-menu",function(){
  $(".sp-menu__list").toggleClass('is_sp-active');
});

$(document).on("click",".sp-menu__list",function(){
  $(".sp-menu__list").removeClass('is_sp-active');
});
