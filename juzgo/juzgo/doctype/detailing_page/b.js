// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Detailing Page', {
    refresh: function(frm) {
        let wrapper = frm.fields_dict.hotels_html.wrapper;
        $(wrapper).append('<iframe id="hotels-sibi" style="height: 100%; width: 100%; border: 0;"></iframe>')

        console.log("----------------")
        const $iframe = $(wrapper).find("iframe");
		let $iframe_body = $iframe.contents();
        
        console.log($iframe, $iframe_body, '---------------');
        console.log($(wrapper).find('iframe')[0])

        $iframe_body.find("head").html(
			`<link href='/assets/juzgo/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>
            <script type="text/javascript" src="/assets/juzgo/node_modules/vuetify/dist/vuetify.js"></script>
            <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />
            <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />`
		);

        // $('#hotels-sibi').load(function(){
        //     $(wrapper).find('iframe').find('body').html('Hey, i`ve changed content of <body>!    Yay!!!');
        // });
        // let ele = $(`<div></div>`).appendTo($(wrapper).find('iframe')[0])
        console.log('---------------------------------------------------')
        console.log( $iframe_body.find("body")[0])
        new frappe.juzgo.detailing1($iframe_body.find("body")[0])
        // $(ele).append("<link href='/assets/juzgo/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>");
        // $(ele).append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />");
        // $(ele).append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />");
    }
});