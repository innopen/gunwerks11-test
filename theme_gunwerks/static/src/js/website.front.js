odoo.define('theme_gunwerks.front', function(require){
    'use strict';

    var utils = require('web.utils');
    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.contactus = sAnimation.Class.extend({
        selector : ".as-contact-box",
        start: function() {
            var self = this;
            this.$target.find("input[name='csrf_token']").replaceWith('<input type="hidden" name="csrf_token" t-att-value="csrf_token  or request.csrf_token()"/>');
        },
    });

    sAnimation.registry.blog_snippet_actions = sAnimation.Class.extend({
        selector : ".s_blog_collection",
        start: function () {
            var self = this;
            if (self.editableMode){
                self.$target.empty().append('<div class="container"><div class="row">' + self.$target.attr('data-blog_col_name') + '</div></div>');
            }
            if (!this.editableMode) {
                $.get("/blog/get_blog_content", {
                    'blog_col_id': self.$target.attr('data-blog_col_id') || 0
                }).then(function (data){
                    if(data.trim()){
                        self.$target.empty().append(data);
                        self.$target.removeClass("hidden");
                    }
                });
            }
        },
    });

    sAnimation.registry.product_table_actions = sAnimation.Class.extend({
        selector : ".category_products_table",
        start: function () {
            var self = this;
            if (self.editableMode){
                self.$target.empty().append('<div class="container"><div class="seaction-head"><h2>' + self.$target.attr("data-collection_name") + '</h2></div></div>');
            }
            if(!self.editableMode){
                $.get("/shop/get_products_table",{
                    'category_id': self.$target.attr('data-collection_id') || 0,
                    'filters': self.$target.attr('data-filters') || '',
                    'is_image': self.$target.attr('data-is_image') || false,
                    'is_description': self.$target.attr('data-is_description') || false,
                }).then(function( data ) {
                    if(data){
                        self.$target.empty().append(data);
                        self.$target.removeClass('hidden');
                    }
                });
            }
        }
    });

    sAnimation.registry.advance_product_slider = sAnimation.Class.extend({
    selector : ".s_products_slider",
        start: function () {
            var self = this;
            if(self.editableMode){
                self.$target.empty().append('<div class="container"><div class="advance_product_slider"><div class="col-md-12"><div class="seaction-head"><h1>Product Slider</h1> </div></div></div></div>');
            }
            if(!this.editableMode){
                $.get("/shop/get_product_content",{
                    'prod_col_id':self.$target.attr('data-p_col_id') || 0
                }).then(function( data ) {
                    if(data){
                        self.$target.empty().append(data);
                        self.$target.removeClass('hidden');
                        self.$target.find(".prod_slider").owlCarousel({
                            items: 3,
                            margin: 30,
                            dots:false,
                            nav:true,
                            navText: ["<i class='fa fa-chevron-left'></i>","<i class='fa fa-chevron-right'></i>"],
                            navigation: false,
                            pagination: false,
                            responsive: {
                                0: {
                                    items: 1,
                                },
                                481: {
                                    items: 2,
                                },
                                768: {
                                    items: 3,
                                }
                            }
                        });
                    }
                });
            }
        }
    });
});
