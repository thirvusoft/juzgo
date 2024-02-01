frappe.pages['detailing1'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Detailing Page',
		single_column: true
	});
	this.page.$juzgo = new frappe.juzgo.detailing1(this.page)
	$('div.navbar-fixed-top').find('.container').css('padding', '0');

	$("head").append("<link href='/assets/juzgo/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>");
	$("head").append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />");
	$("head").append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />");
}