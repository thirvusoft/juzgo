<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5 mt-3"
      style="max-height: 80vh; height: 80vh"
    >
      <v-divider></v-divider>
        <span class="font-weight-bold">Quotation Comparission</span>
        <v-col cols="12">
          <v-select
            dense
            hide-details
            outlined
            color="primary"
            background-color="white"
            :items="quotation_comparission_list"
            :label="frappe._('Quotation Comparission ID')"
            v-model="quotation_comparission"
          ></v-select>
        </v-col>
      <v-divider></v-divider>
      <div class="text-center d-flex pb-4">
        <v-btn @click="all">
          Expand ALL
        </v-btn>
        <v-btn @click="none">
          Collapse ALL
        </v-btn>
        <v-btn
          block
          class="pa-0"
          color="primary"
          dark
          @click="save"
          >{{ __('Save') }}</v-btn
        >
      </div>

      <v-expansion-panels
        class="overflow-y-auto" style="max-height: 75vh"
        v-model="panel"
        multiple
      >
        <v-expansion-panel>
          <v-expansion-panel-header>Hotel</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddSpots()"
                  >
                    Add Hotel
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <table class="custom-table">
                    <tr>
                      <th>
                        Hotel
                      </th>
                      <th v-for="item in quota_hotel_supplier" :key="item">
                        {{ item }}
                      </th>
                    </tr>
                    <tr v-for="item in quota_hotel_list" :key="item">
                      <th>
                        {{ item }}
                      </th>
                      <td v-for="dict in quota_hotel_dict" :key="dict">
                        <div v-for="d in Object.values(dict)" :key="d[0].name" >
                          <div v-for="dl in d" :key="dl.name" v-if="item == dl.hotel">
                            <v-row>
                              <v-col class="text-left">
                                <v-textarea
                                  dense
                                  color="primary"
                                  v-model="dl.notes"
                                  background-color="white"
                                  hide-details

                                  auto-grow
                                >
                                </v-textarea>
                              </v-col>
                            </v-row>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </table>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Spots</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddSpots()"
                  >
                    Add Spots
                  </v-btn>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <table class="custom-table">
                    <tr>
                      <th>
                        Spots
                      </th>
                      <th v-for="item in quota_spot_supplier" :key="item">
                        {{ item }}
                      </th>
                    </tr>
                    <tr v-for="item in quota_spot_list" :key="item">
                      <th>
                        {{ item }}
                      </th>
                      <td v-for="dict in quota_spot_dict" :key="dict">
                        <div v-for="d in Object.values(dict)" :key="d[0].name" >
                          <div v-for="dl in d" :key="dl.name" v-if="item == dl.spots">
                            <v-row>
                              <v-col class="text-left">
                                <v-textarea
                                  dense
                                  color="primary"
                                  v-model="dl.notes"
                                  background-color="white"
                                  hide-details

                                  auto-grow
                                >
                                </v-textarea>
                              </v-col>
                            </v-row>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </table>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </div>
  
</template>

<script>
import { evntBus } from '../../bus';

export default {
  data() {
    return {
      data:[],

      quotation_comparission_list: [],
      quotation_comparission:'',
      quotation_comparission_data: [],
      quota_hotel_supplier:[],
      quota_hotel_list:[],
      quota_hotel_dict:[],
      quota_spot_supplier:[],
      quota_spot_list:[],
      quota_spot_dict:[],

      panel: [],
      items: 2,

      Spots: [],
      Spots_ids:[],

      Hotel: [],
      Hotel_ids:[],


      get_hotel:[],
      get_spots:[],
      get_hotel_category:[],
      get_vehicle:[],
      get_transfer_type:[],
      get_room_type:[],
    };
  },

  methods: {

    makeid(length) {
      let result = '';
      const characters = 'abcdefghijklmnopqrstuvwxyz0123456789';
      const charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    },

    async save(){
      const vm = this
      if(vm.quotation_comparission){
          await frappe.call({
            method: 'juzgo.api.detailing.save_detailing_compare',
            args: {
              quotation_comparission_id : vm.quotation_comparission,
              quotation_comparission_data: vm.quotation_comparission_data,
              comarission_of_hotel: vm.quota_hotel_dict,
              comarission_of_spots: vm.quota_spot_dict,

            },
            callback: function (r) {
              if (r.message) {
                evntBus.$emit('show_mesage', {
                  text: `Detailing Comparission ${vm.quotation_comparission} is Saved`,
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
          text: `Detailing Comparission ID is Not Selected...`,
          color: 'error',
        });
        frappe.utils.play_sound('error');
      }
    },

    name_list_order(){
      this.get_spots = this.get_list("Spots",this.get_spots)
      this.get_hotel = this.get_list("Hotel Details",this.get_hotel)
      this.quotation_comparission_list = this.get_list("DP-Quotation comparission",this.quotation_comparission_list)
    },

    get_list(doctype,list){
      if (list.length > 0) return;
      frappe.db
        .get_list(doctype, {
          fields: ['name'],
          // filters:{''},
          limit: 5000,
          order_by: 'name',
        })
        .then((data) => {
          if (data.length > 0) {
            data.forEach((el) => {
              list.push(el.name);
            });
          }
        });
      return list
    },

    all () {
      this.panel = [...Array(this.items).keys()].map((k, i) => i)
    },
    none () {
      this.panel = []
    },
    push_ids_list(list,id_list){
      list.forEach((ele) => {
        if (id_list.indexOf(ele.det_id) === -1) {
          id_list.push(ele.det_id);
        }
      });
    },

    get_quotation_compare(){
      const vm = this
      frappe.call({
        method: 'juzgo.api.detailing.get_quotation_compare',
        args:{
          quotation_compare_id : vm.quotation_comparission
        },
        callback: function (r) {
          if (r.message) {
            vm.quotation_comparission_data = r.message
            vm.quotation_comparission_data.hotel.forEach( ele =>{
              if (!vm.quota_hotel_supplier.includes(ele.supplier)) {
                vm.quota_hotel_supplier.push(ele.supplier)
              }
              if (!vm.quota_hotel_list.includes(ele.hotel)) {
                vm.quota_hotel_list.push(ele.hotel)
              }
            })
            vm.quotation_comparission_data.hotel.forEach( ele =>{
              vm.quota_hotel_supplier[ele.supplier]={"hotel":ele.hotel,"notes":ele.notes}
            })
          }
          let output = vm.quotation_comparission_data.hotel.reduce((result, item) => {
            let group = result.find(group => group[item.supplier]);
            
            if (!group) {
              group = { [item.supplier]: [] };
              result.push(group);
            }

            let { supplier, ...itemWithoutSupp } = item;
            group[supplier].push(itemWithoutSupp);

            return result;
          }, []);
          vm.quota_hotel_dict = output
          vm.quotation_comparission_data.spots.forEach( ele =>{
            if (!vm.quota_spot_supplier.includes(ele.supplier)) {
              vm.quota_spot_supplier.push(ele.supplier)
            }
            if (!vm.quota_spot_list.includes(ele.spots)) {
              vm.quota_spot_list.push(ele.spots)
            }
          })
          vm.quotation_comparission_data.spots.forEach( ele =>{
            vm.quota_spot_supplier[ele.supplier]={"spots":ele.spots,"notes":ele.notes}
          })

          output = vm.quotation_comparission_data.spots.reduce((result, item) => {
            let group = result.find(group => group[item.supplier]);
            
            if (!group) {
              group = { [item.supplier]: [] };
              result.push(group);
            }

            let { supplier, ...itemWithoutSupp } = item;
            group[supplier].push(itemWithoutSupp);

            return result;
          }, []);
          vm.quota_spot_dict = output

        }
      });
    },
    
  },

  created() {
    this.name_list_order()
  },
  mounted: function () {
    this.$nextTick(function () {
      evntBus.$on('send_detailing_detail_id', (data) => {
        this.data = data
      })
    });
  },
  beforeDestroy() {
    evntBus.$off("send_detailing_detail_id");
  },
  watch:{
    quotation_comparission(){
      this.get_quotation_compare()
    }
  }
};

</script>

<style scoped>
.custom-table {
  border-collapse: collapse;
  width: 100%;
  margin-top:5px;
}

.custom-table th{
  border: 1px solid #ddd;
  padding: 3px;
  text-align: left;
  background-color: #2490ef;
  color: aliceblue;
}

.custom-table td {
  border: 1px solid #ddd;
  padding: 3px;
  text-align: left;
}

.custom-table th {
  font-weight: bold;
}
</style>
