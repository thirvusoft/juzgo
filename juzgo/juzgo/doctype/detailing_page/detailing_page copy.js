// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Detailing Page', {
    refresh: function(frm) {
        let wrapper = frm.fields_dict.hotels_html.wrapper;
        let ele = $(`<div></div>`).appendTo(wrapper)
        new frappe.juzgo.detailing1(ele[0])
        $(wrapper).append("<link href='/assets/juzgo/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>");
        $(wrapper).append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />");
        $(wrapper).append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />");
    }
});