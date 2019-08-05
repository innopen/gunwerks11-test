odoo.define('website_video_extend.editor_js',function(require) {
'use strict';
var editor = require('web_editor.editor');
var core = require('web.core');
var Widget = require('web.Widget');
var options = require('web_editor.snippets.options');
var widget = require('web_editor.widget');
var qweb = core.qweb;
var ajax = require('web.ajax');
ajax.loadXML('/website_video_extend/static/src/xml/snippet.xml',qweb);



//var BodyManager = require('web_editor.BodyManager');
options.registry.WebsiteVideo = options.Class.extend({
    start: function () {
        var self = this;
        var def = this._super.apply(this, arguments);

        

    },
    video_backgroud_content : function (type, value) {
       var value = this.$target.attr('data-video-backgruond');
       var $image = $('<img />', {class: 'hidden o_viewer_video', src: value}).appendTo(this.$target);
		var self = this;
		var $editable = this.$target.closest('.o_editable');
		var options = {
		    res_model: $editable.data('oe-model'),
		    res_id: $editable.data('oe-id'),
		    video_dialog : 1,
		    select_images : false,
		    vide_background : 1,
		};
		var _editor = new widget.MediaDialog(this, options, null, $image[0])
		_editor.opened().then(function () {
            _editor.$('[href="#editor-media-video"],[href="#editor-media-icon"],[href="#editor-media-document"]').addClass('hidden');
            _editor.$('[href="#editor-media-video-mp4"]').trigger('click');


		});
		_editor.on('closed', this, function () {
		    $image.remove();
		});
		_editor.open();
    },
    video_backgroud_setting : function (type, value) {
       var self = this;
       var background = this.$target.attr('data-video-backgruond');

       var bg_mute = this.$target.attr('data-bg_mute');
       var bg_loop = this.$target.attr('data-bg_loop');
       var bg_auto_play = this.$target.attr('data-bg_auto_play');
       var hide_bg_controlles = 'true';
       self.$modal = $(qweb.render("website_video_extend.background_video_setting",{controlles: hide_bg_controlles,mute: bg_mute, loop:bg_loop,auto_play:bg_auto_play }));
       self.$modal.appendTo('body');
       self.$modal.modal();
       var  $video_bg = self.$modal.find("#video-backgruond"),

	    $video_bg_mute = self.$modal.find("#bg_mute"),
	    $video_bg_loop=self.$modal.find("#bg_loop"),
	    $video_bg_auto_play = self.$modal.find("#bg_auto_play"),
	    $cancel = self.$modal.find("#cancel"),
	    $sub_data = self.$modal.find("#sub_data");
	    $sub_data.on('click', function() {
						    						    

	        self.$target.attr('data-bg_mute', $video_bg_mute[0].checked);
	        self.$target.attr('data-bg_loop', $video_bg_loop[0].checked);
	        self.$target.attr('data-bg_auto_play', $video_bg_auto_play[0].checked);

	    })

       
    },

    video_setting : function (type, value) {
       var self = this;
       var background = this.$target.attr('data-video-backgruond');

       var bg_mute = this.$target.attr('data-bg_mute');
       var bg_loop = this.$target.attr('data-bg_loop');
       var bg_auto_play = this.$target.attr('data-hide_bg_controlles');
       var hide_bg_controlles = this.$target.attr('data-bg_auto_play');
       self.$modal = $(qweb.render("website_video_extend.background_video_setting",{controlles: hide_bg_controlles,mute: bg_mute, loop:bg_loop,auto_play:bg_auto_play }));
       self.$modal.appendTo('body');
       self.$modal.modal();
       var  $video_bg = self.$modal.find("#video-backgruond"),

	    $video_bg_mute = self.$modal.find("#bg_mute"),
	    $video_bg_loop=self.$modal.find("#bg_loop"),
	    $video_bg_auto_play = self.$modal.find("#bg_auto_play"),
	    $video_bg_controlles = self.$modal.find('#hide_bg_controlles'),
	    $cancel = self.$modal.find("#cancel"),
	    $sub_data = self.$modal.find("#sub_data");
	    $sub_data.on('click', function() {

		if($video_bg_mute[0].checked==true || $video_bg_mute[0].checked==1){
		self.$target.muted = true;
		self.$target.attr('muted','muted')
		}
		else{
		self.$target.muted = false;
		self.$target.removeAttr('muted')
		}
		if($video_bg_loop[0].checked==true || $video_bg_loop[0].checked==1){
		self.$target.loop = 'loop';
		self.$target.attr('loop','loop')
		}
		else{
		self.$target.loop = 0;
		self.$target.removeAttr('loop')
		}
		if($video_bg_auto_play[0].checked==true || $video_bg_auto_play[0].checked==1){
		self.$target.autoplay = 'autoplay';
		self.$target.attr('autoplay','autoplay')
		}
		else{
		self.$target.autoplay = false;
		self.$target.removeAttr('autoplay')
		}
		if($video_bg_controlles[0].checked==true || $$video_bg_controlles[0].checked==1){
		self.$target.controls = false;
		self.$target.removeAttr('controls')
		}
		else{
		self.$target.autoplay = false;
		self.$target.removeAttr('autoplay')
		}

	    })

       
    },
    
    video_backgroud : function (type, value) {
       var value = this.$target.find('.o_viewer_video source').attr('src');
       var $image = $('<img />', {class: 'hidden o_viewer_video', src: value}).appendTo(this.$target);
		var self = this;
		var $editable = this.$target.closest('.o_editable');
		var options = {
		    res_model: $editable.data('oe-model'),
		    res_id: $editable.data('oe-id'),
		    video_dialog : 1,
		    select_images : false,
		};
		var _editor = new widget.MediaDialog(this, options, null, $image[0])
		_editor.opened().then(function () {
            _editor.$('[href="#editor-media-video"],[href="#editor-media-icon"],[href="#editor-media-document"]').addClass('hidden');
            _editor.$('[href="#editor-media-video-mp4"]').trigger('click');


		});
		_editor.on('closed', this, function () {
		    $image.remove();
		});
		_editor.open();
    },
    modifyvideo : function (type, value) {
            var self = this;
  			var domain = [['id','=',value]]
			return this._rpc({
							model: 'website.video.content',
							method: 'get_file_content',
							args: [value],
						}).then(function(result) {	
                    var $content = '<video class="o_viewer_video" controls="controls" autoplay="autoplay"><source src="/web/image/'+result[0]['id']+'" data-type="'+result[0]['mimetype']+'"/></video>'


self.$target.parent().empty().append($content)
					    return self;
				
						});
}

})










    
    
    
})    
