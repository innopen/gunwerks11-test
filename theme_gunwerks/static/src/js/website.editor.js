odoo.define('theme_gunwerks.editor', function(require){
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');
    var weContext = require('web_editor.context');
    var web_editor = require('web_editor.editor');
    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var qweb = core.qweb;
    var _t = core._t;

    ajax.loadXML('/theme_gunwerks/static/src/xml/target_id_modify_template.xml', qweb);
    ajax.loadXML('/theme_gunwerks/static/src/xml/product_dynamic_table2.xml', qweb);


    options.registry.target_id_snippet_actions = options.Class.extend({
        modify_id: function(previewMode, value){
            var self = this;
            if(previewMode == false){
                self.$modal = $(qweb.render("theme_gunwerks.target_id_section_modify"));
                self.$modal.find(".modal-content > .modal-body input[name='modify_id_value']").attr("value", self.$target.attr("id"));
                self.$modal.appendTo('body');
                self.$modal.modal();
                var $modify_id_input = self.$modal.find(".modify_id_container input[name='modify_id_value']"),
                    $btn_apply = self.$modal.find("#btn_apply");
                $btn_apply.on('click', function(){
                    self.$target.attr('id',$modify_id_input.val());
                });
            }
            return self;
        },
    });

    options.registry.blog_snippet_actions = options.Class.extend({
        popup_template_id: "blog_snippet_popup_template",
        popup_title: _t("Select Blog Collection"),
        blog_snippet_configure: function (previewMode, value) {
            var self = this;
            var def = wUtils.prompt({
                'id': this.popup_template_id,
                'window_title': this.popup_title,
                'select': _t("Collection"),
                'init': function (field) {
                    return rpc.query({
                        model: 'blog.configure',
                        method: 'name_search',
                        args: ['', []],
                        context: weContext.get(),
                    });
                },
            });
            def.then(function (collection_id) {
                self.$target.attr("data-blog_col_id", collection_id);
                rpc.query({
                    model :'blog.configure',
                    method:'read',
                    args: [[parseInt(collection_id)]],
                    context: weContext.get()
                }).then(function (data){
                    if(data && data[0] && data[0].name){
                        self.$target.attr("data-blog_col_name", data[0].name)
                        self.$target.empty().append('<div class="container"><div class="row">'+ data[0].name+'</div></div>');
                    }
                    else{
                        self.$target.attr("data-blog_col_id", "0").attr("data-blog_col_name", "NO BLOG COLLECTION SELECTED");
                    }
                });
            });
            return def;
        },
        onBuilt: function () {
            var self = this;
            this._super();
            this.blog_snippet_configure('click').fail(function () {
                self.getParent()._onRemoveClick($.Event("click"));
            });
        },
        cleanForSave: function(){
            this.$target.addClass("hidden");
        }
    });

    options.registry.product_slider_actions = options.Class.extend({
        popup_template_id: "product_slider_popup_template",
        popup_title: _t("Select Product Collection"),
        product_slider_configure: function(type,value) {
            var self = this;
            var def = wUtils.prompt({
                'id': this.popup_template_id,
                'window_title': this.popup_title,
                'select': _t("Collection"),
                'init': function (field) {
                    return rpc.query({
                        model: 'multitab.configure',
                        method: 'name_search',
                        args: ['', []],
                        context: weContext.get(),
                    });
                },
            });            
            def.then(function (collection_id) {
                self.$target.attr("data-p_col_id", collection_id);
                ajax.jsonRpc('/web/dataset/call', 'call', {
                    model: 'multitab.configure',
                    method: 'read',
                    args: [[parseInt(collection_id)], ['name'], weContext.get()],
                }).then(function (data) {
                    if(data && data[0] && data[0].name){
                        self.$target.attr("data-p_col_name", data[0].name)
                        self.$target.empty().append('<div class="container"><div class="row">' + data[0].name + '</div></div>');   
                    }
                    else{
                        self.$target.attr("data-p_col_id", "0").attr("data-p_col_name", "NO PRODUCT COLLECTION SELECTED");
                    }
                });
            });
            return def;
        },

        onBuilt: function () {
            var self = this;
            this._super();
            this.product_slider_configure('click').fail(function () {
                self.getParent()._onRemoveClick($.Event("click"));
            });
        },

        cleanForSave: function(){
            this.$target.addClass("hidden");
        }
    });

    options.registry.product_table_actions = options.Class.extend({
        product_table_configure: function(previewMode, value){
            var self = this;
            if(previewMode === false || previewMode === "click"){
                self.$modal = $(qweb.render("theme_gunwerks.p_table_popup_template"));
                $('body > #product_table_modal').remove();
                self.$modal.appendTo('body');
                self._rpc({
                    model: 'product.public.category',
                    method: 'name_search',
                    args: ['', []],
                    context: weContext.get()
                }).then(function(data){
                    var s_tab_ele = $("#product_table_modal select[id='s_tab_category']");
                    s_tab_ele.empty();
                    if(data){
                        for(var i = 0; i < data.length; i++){
                            s_tab_ele.append("<option value='" + data[i][0] + "'>" + data[i][1] + "</option>");
                        }
                        if(self.$target.attr("data-collection_id") !== "0"){
                            s_tab_ele.val(parseInt(self.$target.attr("data-collection_id"))).change();
                        }
                    }
                });
                self.$modal.on('change', "#s_tab_category", function(e){
                    var collection_id = parseInt(self.$modal.find("#s_tab_category option:selected").val());
                    var $sel_ele = self.$modal.find("#filters_group");
                    if(!collection_id){
                        $sel_ele.html( "<div class='col-sm-9 col-md-offset-3'><strong class='text-danger'>Please select category.</strong></div>");
                    }
                    else{
                        $.get("/shop/get_filter_list", {
                            'category_id': collection_id || 0,
                        }).then(function(data) {
                            $sel_ele.empty().html( data );
                        });
                    }
                });
                self.$modal.on('click', ".btn_apply", function(e){
                    var $form = self.$modal.find("form");
                    var collection_name = $form.find("#s_tab_category option:selected").text();
                    if(!collection_name)
                        collection_name = "NO CATEGORY SELECTED";
                    var filters = $.map($('select[name="filter"]'), function (e) {
                        return $('option:selected', e).val();
                    });
                    var is_image = false;
                    var is_description = false;

                    if(self.$modal.find("#is_image").is(":checked")){
                       is_image = true; 
                    }
                    if(self.$modal.find("#is_description").is(":checked")){
                       is_description = true; 
                    }

                    self.$target.attr("data-collection_id", $form.find("#s_tab_category").val());
                    self.$target.attr("data-collection_name", collection_name);
                    self.$target.attr("data-filters", filters);
                    self.$target.attr("data-is_image", is_image);
                    self.$target.attr("data-is_description", is_description);
                });

                if(self.$target.attr("data-is_image")){
                    var ed_image = self.$target.attr("data-is_image").toLowerCase() == 'true' ? true : false; 
                    self.$modal.find("#is_image").prop('checked', ed_image);
                }

                if(self.$target.attr("data-is_description")){
                    var ed_description = self.$target.attr("data-is_description").toLowerCase() == 'true' ? true : false;
                    self.$modal.find("#is_description").prop('checked', ed_description);
                }

                self.$modal.modal();
            }
            return self;
        },

        onBuilt: function () {
            var self = this;
            this._super();
            this.product_table_configure('click');
        },

        cleanForSave: function(){
            this.$target.addClass("hidden");
        }
    });
});
