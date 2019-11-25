odoo.define('gunwerks_ballistics.website_front', function(require){
    'use strict';

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;

    $(document).on("click", "li.gw_menu", function(e){
        var $dd_el = $(this).closest(".gw_dd");
        $dd_el.attr("data-selected", $(this).attr("data-val"));
    });

    $(document).on("click", ".dd_wsp li.ws_menu", function(e){
        var $ws_sel = $(this).closest(".dd_wsp");
        $ws_sel.attr("data-selected", $(this).attr("data-val"));
        var $ballistics_ele = $ws_sel.parents(".ballistics_layout");
        var $pf_sel = $ballistics_ele.find(".profile-env-section .dd_pf");
        $pf_sel.find("li.pf_menu.profile_ids").remove();
        var $pf_tabs = $ballistics_ele.find("ul.ws_profiles_tab");
        $pf_tabs.find("li:not('.def_pf_tab')").remove();
        // var $pf_tabpane = $ballistics_ele.find("div.ws_profiles_tabpane");

        if($ws_sel.attr("data-selected") === "" || $ws_sel.attr("data-selected") === "new"){
            $pf_sel.attr("data-selected", "");
            $pf_tabs.find("li.def_pf_tab").removeClass("hidden");
            // $pf_tabpane.find("div.tab-pane.def_pf_tabpane").removeClass("hidden");
        }
        else{
            ajax.jsonRpc('/get_ws_profiles', 'call', {
                'workspace_id': $ws_sel.attr("data-selected")
            }).then(function(data){
                if(data){
                    if(data.profiles.length){
                        $pf_tabs.find("li.def_pf_tab").addClass("hidden");
                        // $pf_tabpane.find("div.tab-pane.def_pf_tabpane").addClass("hidden");
                        for(var i = 0; i < data.profiles.length; i++){
                            $pf_sel.find(".dropdown-menu").append("<li class='pf_menu gw_menu profile_ids' data-val='" + data.profiles[i].id + "'><span>" + data.profiles[i].name + "</span></li>");
                            var act_str = "";
                            // if(i === 0)
                            //     act_str = " active"
                            $pf_tabs.append(
                                "<li class='pf_tab nav-item" + act_str + "' data-pf_id='" + data.profiles[i].id +
                                "' data-env_id='" + data.profiles[i].p_env + "'>" +
                                "<a class='nav-link" + act_str + "' data-toggle='tab' href='#prof" + data.profiles[i].id + "'>" + 
                                data.profiles[i].name + "</li>"
                            );
                            // $pf_tabpane.append(
                            //     "<div class='tab-pane container" + act_str + "' id='prof" + data.profiles[i].id +
                            //     "' data-pf_id='" + data.profiles[i].id + "'>" + data.profiles[i].bl_data + "</div>"
                            // );
                        }
                        // debugger;
                        $pf_tabs.find("li.pf_tab:not('.def_pf_tab'):eq(0) > a").tab("show");
                        $pf_tabs.find("li.pf_tab:not('.def_pf_tab'):eq(0)").trigger("click");
                    }
                    else{
                        $pf_tabs.find("li.def_pf_tab").removeClass("hidden");
                        // $pf_tabpane.find("div.tab-pane.def_pf_tabpane").removeClass("hidden");
                    }
                }
            });
        }
    });

    $(document).on("click", ".dd_pf li.pf_menu", function(e){
        var $pf_sel = $(this).closest(".dd_pf");
        $pf_sel.attr("data-selected", $(this).attr("data-val"));

    });

    var update_profile_props = function($el, data){
        var $ballistics_ele = $el.closest(".ballistics_layout");
        var $left_ele = $ballistics_ele.find(".pf_props");
        $left_ele.find("li[data-prop='bullet_dia'] .value").text(data.pf.bullet_diameter)
        if(data.pf.zero_angle_active === 1)
            $left_ele.find("input[name='zr_angle']").prop("checked", true);
        else
            $left_ele.find("input[name='zr_angle']").prop("checked", false);
        $left_ele.find("li[data-prop='zero_range'] .value").text(data.pf.zero_range);
        $left_ele.find("li[data-prop='zero_angle'] .value").text(data.pf.zero_angle);
        $left_ele.find("li[data-prop='scope_height'] .value").text(data.pf.scope_height);
        $left_ele.find("li[data-prop='twist_rate'] .value").text(data.pf.twist_rate);
        $left_ele.find("li[data-prop='twist_dir'] .value").text(data.pf.twist_dir);
        $left_ele.find("li[data-prop='muzzle_vel'] .value").text(data.pf.muzzle_vel);
        $left_ele.find("li[data-prop='bullet_weight'] .value").text(data.pf.bullet_weight);
        $left_ele.find("li[data-prop='bullet_length'] .value").text(data.pf.bullet_length);
        $left_ele.find("li[data-prop='drag_function'] .value").text(data.pf.drag_function);
        $left_ele.find("li[data-prop='bc'] .value").text(data.pf.bc);
        if(data.pf.input_units === "si")
            $ballistics_ele.find(".input-units input[name='input_unit']").val(data.pf.input_units).prop("checked", true);
        else
            $ballistics_ele.find(".input-units input[name='input_unit']").val(data.pf.input_units).prop("checked", false);
    }

    var update_prof_grid = function($el, data){
        var $ballistics_ele = $el.closest(".ballistics_layout");
        $ballistics_ele.find("#pf_gridview").empty().attr("data-pf_id", data.pf.id).append(data.pf.bl_grid);
    }

    var update_env_infos = function($el, data){
        var $ballistics_ele = $el.closest(".ballistics_layout");
        var $env_ele = $ballistics_ele.find(".env_props");
        if(data.env){
            $env_ele.find("li[data-prop='density_altitude'] .value").text(data.env.density_altitude);
            $env_ele.find("li[data-prop='elevation'] .value").text(data.env.elevation);
            $env_ele.find("li[data-prop='temperature'] .value").text(data.env.temperature);
            $env_ele.find("li[data-prop='pressure'] .value").text(data.env.pressure);
            $env_ele.find("li[data-prop='humidity'] .value").text(data.env.humidity);
            $env_ele.find("li[data-prop='shot_direction'] .value").text(data.env.shot_direction);
            $env_ele.find("li[data-prop='shot_angle'] .value").text(data.env.shot_angle);
            $env_ele.find("li[data-prop='shot_cant'] .value").text(data.env.shot_cant);
            $env_ele.find("li[data-prop='latitude'] .value").text(data.env.latitude);
            $env_ele.find("li[data-prop='base_wind'] .value").text(data.env.base_wind);
            $env_ele.find("li[data-prop='base_wind_dir'] .value").text(data.env.base_wind_dir);
        }
    }

    $(document).on("click", ".ws_profiles_tab .pf_tab", function(e){
        var $curr_pf = $(this);
        ajax.jsonRpc('/get_profile_info', 'call', {
            'profile_id': $curr_pf.attr("data-pf_id"),
            'env_id': $curr_pf.attr("data-env_id")
        }).then(function(data){
            if(data){
                // debugger;
                update_profile_props($curr_pf, data);
                update_env_infos($curr_pf, data);
                update_prof_grid($curr_pf, data);
            }
        });
    });

    $(document).on("click", ".btn_expand", function(e){
        var $sec = $(this).closest(".col_sect")
        if($sec.hasClass("open")){
            $sec.removeClass("open");
            $(this).text(_t("More"));
        }
        else{
            $sec.addClass("open");
            $(this).text(_t("Less"));
        }
    });
});
