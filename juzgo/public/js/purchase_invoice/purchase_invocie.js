import Home from "./Home.vue";

frappe.provide("frappe.juzgo");

frappe.juzgo.detailing1 = class {
    constructor({ parent }) {
        this.$parent = $(document);
        this.page = parent.page;
        this.make_body();

    }
    make_body () {
        this.$el = this.$parent.find('.main-section');
        $("head").append("<link href='/assets/juzgo/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>");
        $("head").append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />");
        $("head").append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />");
        this.vue = new Vue({
            vuetify: new Vuetify(
                {
                    theme: {
                        themes: {
                            light: {
                                background: '#FFFFFF',
                                primary: '#2490ef',
                                secondary: '#00BCD4',
                                accent: '#9575CD',
                                success: '#66BB6A',
                                info: '#2196F3',
                                warning: '#FF9800',
                                error: '#E86674',
                                orange: '#E65100',
                                golden: '#A68C59',
                                badge: '#F5528C',
                                customPrimary: '#085294',
                            },
                        },
                    },
                }
            ),
            el: this.$el[0],
            data: {
            },
            render: h => h(Home),
        });
    }
    setup_header () {

    }

};

// import Home from "./Home.vue";
// import Invoice from "./components/pos/Invoice.vue";
// frappe.provide("frappe.juzgo");

// frappe.juzgo.detailing1 = class {
//   constructor(wrapper) {
//     this.display_area = wrapper;
//     this.make_body();
//   }
//   make_body() {
//     console.log(this.display_area);
//     this.vue = new Vue({
//       vuetify: new Vuetify({
//         theme: {
//           themes: {
//             light: {
//               background: "#FFFFFF",
//               primary: "#0097A7",
//               secondary: "#00BCD4",
//               accent: "#9575CD",
//               success: "#66BB6A",
//               info: "#2196F3",
//               warning: "#FF9800",
//               error: "#E86674",
//               orange: "#E65100",
//               golden: "#A68C59",
//               badge: "#F5528C",
//               customPrimary: "#085294",
//             },
//           },
//         },
//       }),
//       el: this.display_area,
//       data: {},
//       render(createElement) {
//         return createElement(Home);
//       },
//     });
//   }
// };
