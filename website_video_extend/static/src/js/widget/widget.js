odoo.define('website_video_extend.widget', function (require) {
'use strict';

var widget = require('web_editor.widget');
var core = require('web.core');
var QWeb = core.qweb;

 widget.MediaDialog.include({
    template: 'web_editor.dialog.media',
    xmlDependencies:  widget.MediaDialog.prototype.xmlDependencies.concat(
        ['/website_video_extend/static/src/xml/editor.xml']
    ) ,
    events : _.extend({}, widget.MediaDialog.prototype.events, {
        "click #editor-media-video-host" : "update_video_content",
        'click .existing-attachments-videos .existing-attachments .record-div[data-src]': 'select_existing_video',
        'click .media_attachment_video' : 'open_modify'

    }),
    start: function () {
	return this._super.apply(this, arguments);
        
    }, 
    
    open_modify : function(){    
    },
    save: function () {
        var self = this;

	var $m = $(this.range.sc).find('.media_attachment_video')        
		if($('#editor-media-video-mp4').hasClass('active') && self.options && self.options['vide_background']==1){
				
					var $selected = $('.record-div.o_selected')
					if ($selected && $selected[0]){
					var data_id = $selected.attr('data-id');
			
					var domain = [['id','=',data_id]]

					return this._rpc({
									model: 'website.video.content',
									method: 'get_file_content',
									args: [data_id],
								}).then(function(result) {	

				            var $content = '<div class="media_attachment_video o_image"><video class="o_viewer_video" controls="controls"  autoplay="autoplay"><source src="/web/image/'+result[0]['id']+'" data-type="'+result[0]['mimetype']+'" /></video></div>'
				                
								if($(self.range.sc)){
									$(self.range.sc).attr('data-video-url','/web/image/'+result[0]['id'])
									$(self.range.sc).attr('data-video-mimetype',result[0]['mimetype'])
								}

								self.trigger_up('rte_change', {target: self.media});
								if (self.$modal) {
									self.$modal.modal('hide');
									self.$modal.remove();
								}


				
								});
				    
				    

					}
				}
		



else if($('#editor-media-video-mp4').hasClass('active') && self.options){

					var $selected = $('.record-div.o_selected')
					if ($selected && $selected[0]){
					var data_id = $selected.attr('data-id');
			
					var domain = [['id','=',data_id]]

					return this._rpc({
							model: 'website.video.content',
									method: 'get_file_content',
									args: [data_id],
								}).then(function(result) {

								if ($(self.range.sc).closest('.media_attachment_video').length==1){
								var $content = '<video class="o_viewer_video" controls="controls"  autoplay="autoplay"><source src="/web/image/'+result[0]['id']+'" data-type="'+result[0]['mimetype']+'" /></video>'
$(self.range.sc).html($content)
self.trigger_up('rte_change', {target: self.media});
if (self.$modal) {
									self.$modal.modal('hide');
									self.$modal.remove();
								}
}
else{
var $content = '<div class="media_attachment_video o_image"><video class="o_viewer_video" controls="controls"  autoplay="autoplay"><source src="/web/image/'+result[0]['id']+'" data-type="'+result[0]['mimetype']+'" /></video></div>'
$(self.range.sc).html($content)
self.trigger_up('rte_change', {target: self.media});
if (self.$modal) {
									self.$modal.modal('hide');
									self.$modal.remove();
								}
}
								})
}
}
        
        else{

		return this._super.apply(this, arguments);
		}
				
    },    
    update_video_content: function () {
    	var self = this
		    $('[href="#editor-media-image"]').parent().removeClass('active')
		    $('[href="#editor-media-image"]').addClass('hidden');
		    $('#editor-media-image').addClass('hidden');
		return this._rpc({
		        model: 'website.video.content',
		        method: 'search_read',
		        args: [],
		        kwargs: {
		            domain: [],
		            fields: ['name', 'video_type', 'video_url','id'],
		            order: [{name: 'id', asc: false}]
		        }
		    }).then(function(result) {	

		    $('.existing-attachments-videos').replaceWith(QWeb.render('web_editor.dialog.video-mp4.existing', {rows: result}))

		    $('#editor-media-video-host').parent().addClass('active');

		    

		    
		    });
        
    	
    },
    select_existing_video: function (e, force_select) {



    $('.existing-attachments-videos .existing-attachments .record-div').removeClass("o_selected");
    $(e.currentTarget).addClass("o_selected");

    }            
})

var MediaDialogMP4 = widget.MediaDialog.extend({
    template: 'web_editor.dialog.video-mp4',
    xmlDependencies:  widget.MediaDialog.prototype.xmlDependencies.concat(
        ['/website_video_extend/static/src/xml/editor.xml']
    ),

})
return {
    MediaDialogMP4: MediaDialogMP4,
    }
})
