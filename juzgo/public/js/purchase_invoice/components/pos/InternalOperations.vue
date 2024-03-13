  <template>
    <div>
      <v-card
        class="selection mx-auto grey lighten-5 mt-3"
        style="max-height: 80vh; height: 80vh"
      >
        <v-divider></v-divider>
        <span class="font-weight-bold">Internal Operations</span>
        <v-row dense class="overflow-y-auto" style="max-height: 67vh;padding-top: 5px;">
          <v-col cols="12">
            <v-autocomplete
              dense
              auto-select-first
              outlined
              color="primary"
              :label="frappe._('Project')"
              v-model="project"
              :items="projects"
              item-text="project_name"
              item-value="name"
              background-color="white"
              :no-data-text="__('Project not found')"
              hide-details
              :filter="projectsFilter"
              :disabled="readonly"
              prepend-inner-icon="mdi-pencil"
              @click:prepend-inner="view_exists_doc('project/'+project)"
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="primary--text subtitle-1"
                      v-html="data.item.project_name"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-if="data.item.project_name != data.item.name"
                      v-html="`ID: ${data.item.name}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.abbr"
                      v-html="`Abbr.: ${data.item.abbr}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.phone_number"
                      v-html="`Phone No.: ${data.item.phone_number}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.lead"
                      v-html="`Lead: ${data.item.lead}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.ca_form"
                      v-html="`CA Form: ${data.item.ca_form}`"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              dense
              clearable
              auto-select-first
              outlined
              color="primary"
              :label="frappe._('Detailing ID')"
              v-model="detailing_id"
              :items="detailing_ids"
              item-text="name"
              item-value="name"
              background-color="white"
              :no-data-text="__('Detailing Page not found')"
              hide-details
              :filter="detailingFilter"
              :disabled="readonly"
              @change="get_detailing()"
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="primary--text subtitle-1"
                      v-html="data.item.name"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-if="data.item.project_name"
                      v-html="`Project Name: ${data.item.project_name}<br>Project ID: ${data.item.project}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.ca_form"
                      v-html="`CA Form.: ${data.item.ca_form}`"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
          <v-col cols="12">
            <v-autocomplete
              dense
              auto-select-first
              outlined
              color="primary"
              :label="frappe._('CA Form')"
              v-model="ca_form"
              :items="ca_forms"
              item-text="party_name"
              item-value="name"
              background-color="white"
              :no-data-text="__('CA Form not found')"
              :filter="caformFilter"
              prepend-inner-icon="mdi-pencil"
              @click:prepend-inner="view_exists_doc('ca-form/'+ca_form)"
              readonly
            >
              <template v-slot:item="data">
                <template>
                  <v-list-item-content>
                    <v-list-item-title
                      class="primary--text subtitle-1"
                      v-html="data.item.name"
                    ></v-list-item-title>
                    <v-list-item-subtitle
                      v-if="data.item.party_name"
                      v-html="`Party Name: ${data.item.party_name}<br>CA Form ID: ${data.item.name}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.whatsapp_number"
                      v-html="`Whatsapp Number: ${data.item.whatsapp_number}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.e_mail"
                      v-html="`E-Mail: ${data.item.e_mail}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.company"
                      v-html="`Company: ${data.item.company}`"
                    ></v-list-item-subtitle>
                    <v-list-item-subtitle
                      v-if="data.item.quality_of_lead"
                      v-html="`Quality Of Lead: ${data.item.quality_of_lead}`"
                    ></v-list-item-subtitle>
                  </v-list-item-content>
                </template>
              </template>
            </v-autocomplete>
          </v-col>
          
          <v-col cols="12">
            <v-select
              outlined
              v-model="customer_name"
              :items="customers_list"
              :label="frappe._('Customer Name')"
              multiple
              chips
              readonly
            ></v-select>
          </v-col>
          <v-col cols="12">
            <v-select
              outlined
              v-model="destination_name"
              :items="destination_list"
              :label="frappe._('Destination')"
              multiple
              chips
              readonly
            ></v-select>
          </v-col>
          <v-col cols="6">
            <v-menu
              v-model="detailing_detail.check_travel_from_datess"
              :close-on-content-click="false"
              transition="scale-transition"
              dense
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="detailing_detail.travel_from_dates"
                  label="Travel From Date"
                  outlined
                  readonly
                  dense
                  clearable
                  hide-details
                  v-bind="attrs"
                  v-on="on"
                  color="primary"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="detailing_detail.travel_from_dates"
                color="primary"
                no-title
                scrollable
                @input="detailing_detail.check_travel_from_datess= false"
              >
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="6">
            <v-menu
              v-model="detailing_detail.check_travel_to_datess"
              :close-on-content-click="false"
              transition="scale-transition"
              dense
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="detailing_detail.travel_to_dates"
                  label="Travel To Date"
                  outlined
                  readonly
                  dense
                  clearable
                  hide-details
                  v-bind="attrs"
                  v-on="on"
                  color="primary"
                ></v-text-field>
              </template>
              <v-date-picker
                v-model="detailing_detail.travel_to_dates"
                color="primary"
                no-title
                scrollable
                @input="detailing_detail.check_travel_to_datess= false"
              >
              </v-date-picker>
            </v-menu>
          </v-col>
          <v-col cols="4">
            <v-text-field
              v-model="detailing_detail.no_of_adults"
              :label="frappe._('Adults')"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
              readonly
            ></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-text-field
              v-model="detailing_detail.no_of_child"
              :label="frappe._('Child')"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
              readonly
            ></v-text-field>
          </v-col>
          <v-col cols="4">
            <v-text-field
              v-model="detailing_detail.no_of_pax"
              :label="frappe._('Pax')"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
              readonly
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="detailing_detail.duration_of_stay_in_destination"
              :label="frappe._('Duration of stay in Destination')"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
            ></v-text-field>
          </v-col>
          <v-col cols="6">
            <v-text-field
              v-model="detailing_detail.child_ages"
              :label="frappe._('Child Ages')"
              outlined
              dense
              background-color="white"
              clearable
              color="primary"
            ></v-text-field>
          </v-col>
          <v-col cols="12">
            <v-select
              dense
              hide-details
              outlined
              color="primary"
              background-color="white"
              :items="['','Yes','No']"
              :label="frappe._('Prepare Quote?')"
              v-model="detailing_detail.prepare_quote"
            ></v-select>
          </v-col>
          <v-col cols="12">
            <v-textarea 
              dense
              clearable
              outlined
              color="primary"
              :label="frappe._('Remarks')"
              v-model="detailing_detail.remarks"
              background-color="white"
              auto-grow
              row-height="25"
            ></v-textarea>
          </v-col>
        </v-row>
      </v-card>
      <v-card class="cards mb-0 mt-3 pa-2 grey lighten-5">
        <v-row no-gutters align="center" justify="center">
          <v-col cols="12" class="mt-2">
            <v-btn
              block
              class="pa-0"
              color="primary"
              dark
              @click="save"
              >{{ __('Save') }}</v-btn
            >
          </v-col>
          <!-- <v-col cols="6" class="mt-2">
            <v-btn
              block
              class="pa-0"
              color="accent"
              @click="print"
              dark
              >{{ __('Print') }}</v-btn
            >
          </v-col> -->
        </v-row>
      </v-card>
    </div>
  </template>
  <script>
  import { evntBus } from '../../bus';
  
  export default {
    data() {
      return {
        projects: [],
        project: '',
        readonly: false,
        detailing_ids: [],
        detailing_id: '',
        detailing_detail: '',
        ca_form:'',
        ca_forms: [],
        customers_list: [],
        customer:[],
        destination_name:[],
        destination_list:[],
      };
    },
  
    components: {
    },
  
    computed: {
      
    },
  
    methods: {
      view_exists_doc(link){
        const win = window.open(
          link,
          '_blank'
        );
        win.focus();
      },
      get_project_names() {
        const vm = this;
        frappe.call({
          method: 'juzgo.api.detailing.get_project_names',
          callback: function (r) {
            if (r.message) {
              vm.projects = r.message;
            }
          },
        });
      },
      projectsFilter(item, queryText, itemText) {
        const textOne = item.project_name
          ? item.project_name.toLowerCase()
          : '';
        const textTwo = item.abbr ? item.abbr.toLowerCase() : '';
        const textThree = item.phone_number ? item.phone_number.toLowerCase() : '';
        const textFour = item.mobile_no ? item.mobile_no.toLowerCase() : '';
        const textFifth = item.lead ? item.lead.toLowerCase() : '';
        const textsix = item.ca_form ? item.ca_form.toLowerCase() : '';
        const textseven = item.name.toLowerCase();
        const searchText = queryText.toLowerCase();
  
        return (
          textOne.indexOf(searchText) > -1 ||
          textTwo.indexOf(searchText) > -1 ||
          textThree.indexOf(searchText) > -1 ||
          textFour.indexOf(searchText) > -1 ||
          textFifth.indexOf(searchText) > -1 ||
          textsix.indexOf(searchText) > -1 ||
          textseven.indexOf(searchText) > -1
        );
      },         
      get_detailing_names() {
        const vm = this;
        frappe.call({
          method: 'juzgo.api.detailing.get_detailing_names',
          args:{
            project:vm.project
          },
          callback: function (r) {
            if (r.message) {
              vm.detailing_ids = r.message;
            }
          },
        });
      },
      detailingFilter(item, queryText, itemText) {
        const textOne = item.project_name
          ? item.project_name.toLowerCase()
          : '';
        const textTwo = item.project ? item.project.toLowerCase() : '';
        const textThree = item.ca_form ? item.ca_form.toLowerCase() : '';
        const textFour = item.name.toLowerCase();
        const searchText = queryText.toLowerCase();
  
        return (
          textOne.indexOf(searchText) > -1 ||
          textTwo.indexOf(searchText) > -1 ||
          textThree.indexOf(searchText) > -1 ||
          textFour.indexOf(searchText) > -1
        );
      },
      get_caform_names() {
        const vm = this;
        frappe.call({
          method: 'juzgo.api.detailing.get_caform_names',
          callback: function (r) {
            if (r.message) {
              vm.ca_forms = r.message;
            }
          },
        });
      },
      caformFilter(item, queryText, itemText) {
        const textOne = item.party_name
          ? item.party_name.toLowerCase()
          : '';
        const textTwo = item.whatsapp_number ? item.whatsapp_number.toLowerCase() : '';
        const textThree = item.e_mail ? item.e_mail.toLowerCase() : '';
        const textFour = item.company ? item.company.toLowerCase() : '';
        const textFive = item.quality_of_lead ? item.quality_of_lead.toLowerCase() : '';
        const textSix = item.name.toLowerCase();
        const searchText = queryText.toLowerCase();
  
        return (
          textOne.indexOf(searchText) > -1 ||
          textTwo.indexOf(searchText) > -1 ||
          textThree.indexOf(searchText) > -1 ||
          textFour.indexOf(searchText) > -1 ||
          textFive.indexOf(searchText) > -1 ||
          textSix.indexOf(searchText) > -1
        );
      },        
      get_detailing(){
        const vm = this;
        if(vm.detailing_id){
            frappe.call({
              method: 'juzgo.api.detailing.get_detailing',
              args: {
                detailing_id : vm.detailing_id,
              },
              callback: function (r) {
                if (r.message) {
                  let data = r.message
                  vm.project = data.project
                  vm.ca_form = data.ca_form
                  vm.detailing_detail = data 
                  vm.customer_name = []
                  vm.destination_name = []
                  data.customer.forEach((ele)=>{
                    vm.customer_name.push(ele.customer)
                  })
                  data.destination.forEach((ele)=>{
                    vm.destination_name.push(ele.destination_name)
                  })
                  if(vm.detailing_detail.ca_form){vm.get_ca_from_details()}
                }
              },
            });
        }
        else{
          vm.project = ''
          vm.ca_form = ''
          vm.detailing_detail = '' 
          vm.customer_name = []
          vm.destination_name = []
        }
      },    
      async save(){
        const vm = this
        if(vm.detailing_id){
            await frappe.call({
              method: 'juzgo.api.detailing.save_detailing',
              args: {
                detailing_id : vm.detailing_id,
                detailing_detail: vm.detailing_detail

              },
              callback: function (r) {
                if (r.message) {
                  evntBus.$emit('show_mesage', {
                    text: `Detailing Page ${vm.detailing_id} is Saved`,
                    color: 'success',
                  });
                  frappe.utils.play_sound('submit');
                }
              },
            });
          window.location.reload();
        }
        else{
          evntBus.$emit('show_mesage', {
            text: `Detailing ID is Not Selected...`,
            color: 'error',
          });
          frappe.utils.play_sound('error');
        }
      },
      get_last_data(){
        const vm = this
        frappe.call({
          method: 'juzgo.api.detailing.get_last_data',
          callback: function (r) {
            if (r.message) {
              let data = r.message
              vm.detailing_id = data.name
              vm.project = data.project
              vm.ca_form = data.ca_form
              vm.customer_name = []
              vm.destination_name = []
              data.customer.forEach((ele)=>{
                vm.customer_name.push(ele.customer)
              })
              data.destination.forEach((ele)=>{
                vm.destination_name.push(ele.destination_name)
              })
              vm.detailing_detail = data 
              if(vm.detailing_detail.ca_form){vm.get_ca_from_details()}
            }
          },
        });
      },
      async get_ca_from_details(){
        const vm = this
        await frappe.db.get_value('CA Form', {'name': vm.detailing_detail.ca_form}, ['travel_end_date','travel_start_date','no_of_nights','nos_of_days','no_of_paxs','no_of_adult','no_of_childrens','child_without_bed'], (r) => {
          vm.detailing_detail.no_of_adults = r.no_of_adult
          vm.detailing_detail.no_of_child = (r.no_of_childrens || 0) + (r.child_without_bed || 0)
          vm.detailing_detail.no_of_pax = r.no_of_paxs
          vm.detailing_detail.duration_of_stay_in_destination = r.no_of_nights+"N "+ r.nos_of_days+"D"
          vm.detailing_detail.travel_from_dates = r.travel_start_date
          vm.detailing_detail.travel_to_dates = r.travel_end_date
      })
      },
      print(){

      },
      get_customers_list(){
      if (this.customers_list.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Customer', {
          fields: ['name'],
          limit: 5000,
          order_by: 'name',
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.customers_list.push(el.name);
            });
          }
        });
      },
      get_destination_list(){
      if (this.destination_list.length > 0) return;
      const vm = this;
      frappe.db
        .get_list('Destination', {
          fields: ['name'],
          limit: 5000,
          order_by: 'name',
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              vm.destination_list.push(el.name);
            });
          }
        });
      },
      save_doc(e) {
        if (e.key === 's' && (e.ctrlKey || e.metaKey)) {
          e.preventDefault();
          this.save();
        }
      },
    },
  
    created() {
      this.$nextTick(function () {
        this.get_last_data()
        this.get_project_names()
        this.get_detailing_names()
        this.get_detailing()
        this.get_caform_names()
        this.get_customers_list()
        this.get_destination_list()
      })
      document.addEventListener('keydown', this.save_doc.bind(this));
    },
    
    destroyed() {
      document.removeEventListener('keydown', this.save_doc);
    },
    watch: {
      detailing_detail() {
        evntBus.$emit('send_detailing_detail', this.detailing_detail);
      },
      project(){
        this.get_detailing_names()
      }
    },
  };
  </script>
  
  <style scoped>
  .border_line_bottom {
    border-bottom: 1px solid lightgray;
  }
  .disable-events {
    pointer-events: none;
  }
  </style>
  
