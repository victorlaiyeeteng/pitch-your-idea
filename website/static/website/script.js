$(function() {
	$('a[href]:not([href^="#popup"])').click(function() {
		if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
		var target = $(this.hash);
		target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
		if (target.length) {
			$('html,body').animate({
			scrollTop: target.offset().top-100
			},1);
			return false;
		}
		}
	});
	});

$(document).ready(function(){
    $('#idea-image1').click(function(){
        $('#myModal1').css('display', 'block');
    })
    $('.close').click(function(){
        $('#myModal1').css('display', 'none');
    })
    $('#idea-image2').click(function(){
        $('#myModal2').css('display', 'block');
    })
    $('.close').click(function(){
        $('#myModal2').css('display', 'none');
    })
    $('#idea-image3').click(function(){
        $('#myModal3').css('display', 'block');
    })
    $('.close').click(function(){
        $('#myModal3').css('display', 'none');
    })
    $('#idea-image4').click(function(){
        $('#myModal4').css('display', 'block');
    })
    $('.close').click(function(){
        $('#myModal4').css('display', 'none');
    })
    $('#idea-image5').click(function(){
        $('#myModal5').css('display', 'block');
    })
    $('.close').click(function(){
        $('#myModal5').css('display', 'none');
    })
    $('.menu-bars').click(function(){
        $('.navbar .menu').toggleClass("active");
        $('.navbar-pages .menu').toggleClass("active");
        $('.menu-bars i').toggleClass("active");
    })
    $(window).scroll(function(){
        $('.image111').each( function(i) {
            var bottom_of_object = $(this).position().top + ($(this).outerHeight()/4);
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            if (bottom_of_window > bottom_of_object){
                $(this).animate({'opacity': '1'}, 500);
            }
        })
        $('.image113').each( function(i) {
            var bottom_of_object = $(this).position().top + ($(this).outerHeight()/4);
            var bottom_of_window = $(window).scrollTop() + $(window).height();
            if (bottom_of_window > bottom_of_object){
                $(this).animate({'opacity': '1'}, 700);
                $('.image112').animate({'opacity': '1'}, 700);
            }
        })
        if(this.scrollY > 20){
            $('.navbar').addClass("sticky");
            $('.navbar .logo a').addClass("sticky");
            $('.navbar .menu').addClass("sticky");
        } else {
            $('.navbar').removeClass("sticky");
			$('.navbar .logo a').removeClass("sticky");
            $('.navbar .menu').removeClass("sticky");
        }
    })
    
    $('.like-form').submit(function(e){
        e.preventDefault();
        const post_id = $(this).attr('id')
        const url = $(this).attr('action')
        let res;
        const likes = $(`.like-count${post_id}`).text()
        const trimCount = parseInt(likes)
        let result;
        const like_btn = $(`#like-btn${post_id}`).text()
        const like_btn_text = $.trim(like_btn)
        $(`#like-btn${post_id}`).mouseover(function() {
            $(this).css("cursor", "pointer");
            $(this).css("font-style", "italic");
        }).mouseout(function() {
            $(this).css("cursor", "default");
            $(this).css("font-style", "normal");
        });
        $.ajax({
            type:'POST', 
            url: url, 
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(), 
                'post_id': post_id, 
            },
            success: function(response){
                res = response["likes"]
                result = response["liked"]
                $(`#like-btn${post_id}`).text(result)
                $(`.like-count${post_id}`).text(res)
                if (result == "Liked") {
                    $(`#like-btn${post_id}`).css('background-color', 'rgba(152, 251, 152, 0.5)');
                } else {
                    $(`#like-btn${post_id}`).css('background-color', 'palegreen');
                    $(`#like-btn${post_id}`).css('border-color', 'black');
                }
                var likeicon = '<i class="far fa-thumbs-up" style="font-size: 19px;"></i> ';
                $(`#like-btn${post_id}`).prepend(likeicon);
                console.log('success', response)
            }, 
            error: function(response){
                console.log('error', response)
            }
            })
        })

    $('.favourite-form').submit(function(e){
        e.preventDefault();
        const post_id = $(this).attr('id')
        const url = $(this).attr('action')
        let result;
        const favourite_btn = $(`#favourite-btn${post_id}`).text()
        const favourite_btn_text = $.trim(favourite_btn)
        $(`#favourite-btn${post_id}`).mouseover(function() {
            $(this).css("cursor", "pointer");
            $(this).css("background-color", '#f12930b0');
        }).mouseout(function() {
            $(this).css("cursor", "default");
            $(this).css("background-color", '#f1292fce');
        });
        $.ajax({
            type:'POST', 
            url: url, 
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(), 
                'post_id': post_id,
            }, 
            success: function(response){
                result = response["favourited"]
                $(`#favourite-btn${post_id}`).text(result)
                if (result == 'Tracked') {
                    $(`#favourite-btn${post_id}`).css('background-color', '#eb4147ce');
                } else {
                    $(`#favourite-btn${post_id}`).css('background-color', '#f1292fce');
                    $(`#favourite-btn${post_id}`).css('border-color', 'black');
                }
                var charticon = '<i class="fas fa-chart-line" style="font-size: 19px;"></i> ';
                $(`#favourite-btn${post_id}`).prepend(charticon);
                console.log('success', response)
            }, 
            error: function(response){
                console.log('error', response)
            }
        })
    })

    $('.comment-form').submit(function(e){
        e.preventDefault();
        var _comment = $('.commentinput').val();
        var _postid = $('.commentsubmit').data('comment');
        var _user = $('.comment-form').data('user');
        const url = $(this).attr('action');
        
        $.ajax({
            url: url, 
            type: "POST", 
            data: {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'comment': _comment, 
                'post_id': _postid, 
                'user':_user
            }, 
            dataType: 'json', 
            beforeSend: function(){
                $(".commentsubmit").addClass('disabled').text('commenting...');
            }, 
            success: function(res){
                $(".commentsubmit").removeClass('disabled').text('Comment');
                if(res.bool==true){
                    $('.commentinput').val('');
                    var appendhtml = '<div style = "padding-bottom:2%;"><div class="individual-comment"><h4 style="padding-bottom: 1%;">'+_user+' - <span style="font-weight: 450; font-size: smaller;">Just Now</span></h4>\
                    <p>'+_comment+'</p>\
                    <p style="font-size:10px;font-style:itallic;padding-left:0.5%;">*Refresh for the idea to fully process your insight.</p>\
                    <br></div></div>';
                    $(appendhtml).hide().prependTo('.comment-list').fadeIn(700);
                }
            }
        })
    })

    var typed = new Typed(".change", {
        strings: ['Share your idea', 'Seek feedback', 'Continuously strengthen your idea'], 
        typeSpeed: 50, 
        backSpeed: 40, 
        loop: true
    })


    })

function goBack() {
    window.history.back();
}


