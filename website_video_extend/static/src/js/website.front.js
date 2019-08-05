odoo.define('website_video_extend.front_js',function(require){
    'use strict';
    var sAnimation = require('website.content.snippets.animation');
    var ajax = require('web.ajax');

function isAnyPartOfElementInViewport(el) {

    const rect = el.getBoundingClientRect();
    // DOMRect { x: 8, y: 8, width: 100, height: 100, top: 8, right: 108, bottom: 108, left: 8 }
    const windowHeight = (window.innerHeight || document.documentElement.clientHeight);
    const windowWidth = (window.innerWidth || document.documentElement.clientWidth);

    // http://stackoverflow.com/questions/325933/determine-whether-two-date-ranges-overlap
    const vertInView = (rect.top <= windowHeight) && ((rect.top + rect.height) >= 0);
    const horInView = (rect.left <= windowWidth) && ((rect.left + rect.width) >= 0);

    return (vertInView && horInView);
}

$( document ).ready(function() {
$('.o_viewer_video[autoplay="autoplay"], .videoBG video').each(function( index ) {

if (!isAnyPartOfElementInViewport(this)){
$(this).attr('muted','muted');
}
})


    

  sAnimation.registry.advance_background_video = sAnimation.Class.extend({
    selector : "section[data-video-url]",
        start: function () {
            var self = this;  
        if (self.editableMode && self.$target.find('.videoBG_wrapper').length==1)
            {
            	self.$target.replaceWith(self.$target.find('.videoBG_wrapper').html());
            }
        
        else if(!self.editableMode) {

	}
}
        
        })
        
               
    

})
window.onload = function() {
    $('.o_viewer_video[autoplay="autoplay"]').each(function( index ) {
	var video = $(this)[0]
   if(!video.paused  && !isAnyPartOfElementInViewport(this)) {

	var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
		    && video.readyState > 2;
	if (isPlaying) {
	video.pause()
	video.removeClass('played');
		}
     	
     }
     
    if (isAnyPartOfElementInViewport(this)){
	var video = $(this)[0]
	var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
	    && video.readyState > 2;

	if (!isPlaying) {
if( video.hasClass('played')){

}
else{
video.currentTime = 0
setTimeout(() => video.play().catch((err) => console.info(err)), 1000);
video.addClass('played');
}

	  

	}
     }
     
    })

  $('section[data-video-url]').each(function( index ) {
    var self = this;
if(!$(self).parent().hasClass('videoBG_wrapper')){
var len_bg = $(self).find('.videoBG_wrapper').length;



    if (isAnyPartOfElementInViewport(self)){


    	if (len_bg==1){


		var video =$(self).find('video')[0];
		var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
		    && video.readyState > 2;


		if (!isPlaying && $(self).find('video').attr('autoplay')=='autoplay') {
if(video.hasClass('played')){
}
else{
video.currentTime = 0
setTimeout(() => video.play().catch((err) => console.info(err)), 1000);
video.addClass('played');
}
			}
    	
    	}
    	else if(len_bg==0){


ajax.jsonRpc("/shop/get_content_delivery_video_urls", 'call', {
            'src': $(self).attr('data-video-url'),
        }).then(function (data) {


            if (data) {

if($(self).find('.videoBG_wrapper').length==0 & $(".o_editable[data-oe-model]").length==0){

$(self).videoBG({
				mp4:data,
				mimetype : $(self).attr('data-video-mimetype'),
				scale:true,
				zIndex:0,
				fullscreen:false,
				controlls : $(self).attr('data-hide_bg_controlles'),
				mute : $(self).attr('data-bg_mute'),
				loop : $(self).attr('data-bg_loop'),
				autoplay : $(self).attr('data-bg_auto_play'),
				opacity:1,



			});
            }
}
        });

    
}
     }
   else{
    	if (len_bg==1){


	var video =$(self).find('video')[0];
	var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
		    && video.readyState > 2;
	if (isPlaying && $(self).find('video').attr('autoplay')=='autoplay') {
	//video.pause()
		}
	$(self).html($(self).find('.videoBG_wrapper').innerHTML)
	}
}
}
     
    })

}

$(window).scroll(function(e)
  {
  //$('.o_viewer_video[autoplay="autoplay"]:in-viewport')


    $('.o_viewer_video[autoplay="autoplay"]').each(function( index ) {
	var video = $(this)[0]
   if(!video.paused  && !isAnyPartOfElementInViewport(this)) {

	var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
		    && video.readyState > 2;
	if (isPlaying) {
	video.pause()
		}
     	
     }
     
    if (isAnyPartOfElementInViewport(this)){
	var video = $(this)[0]
	var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
	    && video.readyState > 2;

	if (!isPlaying) {
video.currentTime = 0
setTimeout(() => video.play().catch((err) => console.info(err)), 1000);
	}
     }
     
    })

  $('section[data-video-url]').each(function( index ) {
    var self = this;
if(!$(self).parent().hasClass('videoBG_wrapper')){
var len_bg = $(self).find('.videoBG_wrapper').length;



    if (isAnyPartOfElementInViewport(self)){


    	if (len_bg==1){


		var video =$(self).find('video')[0];
		var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
		    && video.readyState > 2;


		if (!isPlaying && $(self).find('video').attr('autoplay')=='autoplay') {
video.currentTime = 0
setTimeout(() => video.play().catch((err) => console.info(err)), 1000);
			}
    	
    	}
    	else if(len_bg==0){


ajax.jsonRpc("/shop/get_content_delivery_video_urls", 'call', {
            'src': $(self).attr('data-video-url'),
        }).then(function (data) {

            if (data) {
if($(self).find('.videoBG_wrapper').length==0){

$(self).videoBG({
				mp4:data,
				mimetype : $(self).attr('data-video-mimetype'),
				scale:true,
				zIndex:0,
				fullscreen:false,
				controlls : $(self).attr('data-hide_bg_controlles'),
				mute : $(self).attr('data-bg_mute'),
				loop : $(self).attr('data-bg_loop'),
				autoplay : $(self).attr('data-bg_auto_play'),
				opacity:1,



			});
            }
}
        });

    
}
     }
   else{
    	if (len_bg==1){


	var video =$(self).find('video')[0];
	var isPlaying = video.currentTime > 0 && !video.paused && !video.ended 
		    && video.readyState > 2;
	if (isPlaying && $(self).find('video').attr('autoplay')=='autoplay') {
	//video.pause()
		}
	$(self).html($(self).find('.videoBG_wrapper').innerHTML)
	}
}
}
     
    })
	


 
  

});
 
  
})
