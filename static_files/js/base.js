// 控制按钮的显示和消失
 $(window).scroll(function(){
            if($(window).scrollTop()>300){
                $('#return-top').fadeIn(300);
                }
             else{$('#return-top').fadeOut(200);}
                 })


// 点击按钮，使得页面返回顶部
$("#return-top").click(function(){
scrollTo(0,0);
});
// 鼠标悬浮按钮之上，图片消失，文字显示
$(".top_e").mouseover(function(){
    $("#img").hide();
    $("#font").show();
})
//鼠标离开，文字消失，图片显示。
$(".top_e").mouseout(function(){
    $("#font").hide();
    $("#img").show();
})