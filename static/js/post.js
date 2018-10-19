$(document).on("click",".js_confirm",function(){
  $(this).toggleClass('is_active');
  $(".js_send").toggleClass('is_active');
  $(".js_modify").toggleClass('is_active');
});

$(document).on("click",".js_modify",function(){
  $(this).toggleClass('is_active');
  $(".js_send").toggleClass('is_active');
  $(".js_confirm").toggleClass('is_active');
});
