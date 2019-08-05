# -*- coding: utf-8 -*-

from odoo import http, tools, _
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_form.controllers.main import WebsiteForm
from odoo.addons.website_crm.controllers.main import WebsiteForm


class WebsiteEvent(WebsiteEventController):

    @http.route()
    def events(self, page=1, **searches):
        searches.setdefault("address_id", "all")
        result = super(WebsiteEvent, self).events(page, **searches)

        values = result.qcontext
        values["types"].clear()
        values["dates"][0][1] = _('By Date')

        searches = values["searches"]

        selected_id = searches['address_id']
        values["selected_id"] = selected_id

        selected_date_id = searches['date']
        values["selected_date_id"] = selected_date_id

        selected_type_id = searches['type']
        values["selected_type_id"] = selected_type_id

        domain = [("state", "in", ("draft", "confirm", "done"))]

        def dom_without(without):
            return [leaf for leaf in domain if leaf[0] not in without]

        for date in values["dates"]:
            if values['searches']['date'] == date[0]:
                domain += date[2]
                break

        if values["current_type"]:
            domain.append(("event_type_id", "=", values["current_type"].id))

        if values["current_country"]:
            domain.append(("country_id", "=", values["current_country"].id))
        elif searches["country"] == 'online':
            domain.append(("country_id", "=", False))

        Event = request.env['event.event']

        types = Event.read_group(domain, ["id", "event_type_id"], groupby=[
                                 "event_type_id"], orderby="event_type_id")
        types.insert(0, {
            'event_type_id_count': sum([int(type['event_type_id_count']) for type in types]),
            'event_type_id': ("all", _("By Event Type"))
        })

        values["types"] = types

        lines = Event.read_group(
            domain, ["id", "address_id"], groupby='address_id', orderby="address_id")

        lines.insert(0, {"address_id_count": sum(x['address_id_count'] for x in lines),
                         "address_id": ("all", _("By Location"))
                         })

        values["lines"] = lines
        values["current_address_id"] = searches["address_id"]

        if searches["address_id"] != "all":
            domain.append(("address_id", "=", int(searches["address_id"])))

            values["types"][1:] = Event.read_group(
                dom_without({"event_type_id"}),
                ["id", "event_type_id"],
                groupby=["event_type_id"],
                orderby="event_type_id")
            values["types"][0]["event_type_id_count"] = sum(
                int(type_['event_type_id_count'])
                for type_ in values["types"][1:])

            values["countries"][1:] = Event.read_group(
                dom_without({"country_id"}),
                ["id", "country_id"],
                groupby="country_id",
                orderby="country_id")
            values["countries"][0]["country_id_count"] = sum(
                int(type_['country_id_count'])
                for type_ in values["countries"][1:])

            for date in values["dates"]:
                if date[0] != 'old':
                    date[3] = Event.search_count(
                        dom_without({"date_end", "date_begin"}) + date[2])

        step = 10
        values["pager"] = http.request.website.pager(
            url="/event",
            url_args={
                "date": searches.get("date"),
                "type": searches.get("type"),
                "country": searches.get("country"),
                "address_id": searches.get("address_id"),
            },
            total=Event.search(domain, count=True),
            page=page,
            step=step,
            scope=5)

        order = 'website_published desc, date_begin'
        if searches["date"] == "old":
            order += " desc"
        values["event_ids"] = Event.search(
            domain,
            limit=step,
            offset=values["pager"]["offset"],
            order=order)

        result.qcontext = values
        return result
