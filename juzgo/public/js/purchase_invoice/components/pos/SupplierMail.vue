<template>
  <div>
    <v-data-table
      :headers="visaSupplierHeaders"
      :items="visaSupplier"
      :single-expand="visaSuppliersingleExpand"
      :expanded.sync="visaSupplierexpanded"
      item-key="page_row_id"
      show-expand
      sort-by="destination"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Visa Supplier</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="visaSupplierdialog"
            max-width="700px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                New Item
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.destination"
                        label="Destination"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.supplier"
                        label="Supplier"
                      ></v-text-field>
                    </v-col>
                    <!-- <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.supplier_name"
                        label="Supplier Name"
                      ></v-text-field>
                    </v-col> -->
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.supplier_mail_id"
                        label="Supplier Email ID"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <!-- <v-card-subtitle>
                    <span class="text-h6">CA Form Detailes</span>
                  </v-card-subtitle> -->
                  
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.travel_from_dates"
                        label="Travel From dates"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.travel_to_dates"
                        label="Travel To dates"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.duration_of_stay_in_destination"
                        label="Duration of stay in Destination"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.no_of_adults"
                        label="No of Adults"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.no_of_child"
                        label="No of Child"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.child_ages"
                        label="Child Ages"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.visa_type"
                        label="Visa Type"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="visaSuppliereditedItem.questions"
                        label="Questions"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="visaSupplierclose"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="visaSuppliersave"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <v-row class="ma-0 pa-0">
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Destination')"
                background-color="white"
                hide-details
                v-model="item.destination"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Supplier')"
                background-color="white"
                hide-details
                v-model="item.supplier"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Supplier Name')"
                background-color="white"
                hide-details
                v-model="item.supplier_name"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Supplier Email ID')"
                background-color="white"
                hide-details
                v-model="item.supplier_mail_id"
              ></v-text-field>
            </v-col>
          </v-row>
        </td>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          @click="visaSupplierdeleteItemConfirm"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>

    <v-data-table
      :headers="SupplierHeaders"
      :items="Supplier"
      :single-expand="SuppliersingleExpand"
      :expanded.sync="Supplierexpanded"
      item-key="page_row_id"
      show-expand
      sort-by="destination"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Supplier</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="Supplierdialog"
            max-width="500px"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="primary"
                dark
                class="mb-2"
                v-bind="attrs"
                v-on="on"
              >
                New Item
              </v-btn>
            </template>
            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="SuppliereditedItem.supplier"
                        label="Supplier"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="SuppliereditedItem.supplier_name"
                        label="Supplier Name"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="SuppliereditedItem.supplier_mail_id"
                        label="Supplier Email ID"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="Supplierclose"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="Suppliersave"
                >
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <v-row class="ma-0 pa-0">
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Destination')"
                background-color="white"
                hide-details
                v-model="item.destination"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Supplier')"
                background-color="white"
                hide-details
                v-model="item.supplier"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Supplier Name')"
                background-color="white"
                hide-details
                v-model="item.supplier_name"
              ></v-text-field>
            </v-col>
            <v-col cols="4">
              <v-text-field
                dense
                outlined
                color="primary"
                :label="frappe._('Supplier Email ID')"
                background-color="white"
                hide-details
                v-model="item.supplier_mail_id"
              ></v-text-field>
            </v-col>
          </v-row>
        </td>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          @click="SupplierdeleteItemConfirm"
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </div>
</template>


<script>
  import { evntBus } from '../../bus';

  export default {
    data: () => ({
      detailing_detail:'',

      visaSupplierdialog: false,
      dialogDelete: false,
      visaSupplierexpanded: [],
      visaSuppliersingleExpand: false,

      visaSupplierHeaders: [
        {
          text: 'Destination',
          align: 'start',
          value: 'destination',
        },
        { text: 'Supplier', value: 'supplier' },
        { text: 'Supplier Name', value: 'supplier_name' },
        { text: 'Supplier Mail ID', value: 'supplier_mail_id' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      visaSupplier: [],
      visaSuppliereditedIndex: -1,
      visaSuppliereditedItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '',
      },
      visaSuppliereddefaultItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '',
      },


      Supplierdialog: false,
      Supplierexpanded: [],
      SuppliersingleExpand: false,

      SupplierHeaders: [
        { text: 'Supplier', value: 'supplier' },
        { text: 'Supplier Name', value: 'supplier_name' },
        { text: 'Supplier Mail ID', value: 'supplier_mail_id' },
        { text: 'Hotels', value: 'hotels' },
        { text: 'Spots', value: 'spots' },
        { text: 'Vehicle', value: 'vehicle' },
        { text: 'Optional Costs', value: 'optional_costs' },
        { text: 'Others', value: 'others' },
        { text: 'Cruise', value: 'cruise' },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      Supplier: [],
      SuppliereditedIndex: -1,
      SuppliereditedItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '',
      },
      SuppliereddefaultItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '',
      },
    }),

    computed: {
      formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
      },
    },

    methods: {

      deleteItemConfirm () {
        this.desserts.splice(this.editedIndex, 1)
      },

      visaSupplierdeleteItemConfirm () {
        // Visa Supplier
        this.visaSupplier.splice(this.visaSuppliereditedIndex, 1)
      },

      visaSupplierclose () {
        this.visaSupplierdialog = false
        this.$nextTick(() => {
          this.visaSuppliereditedItem = Object.assign({}, this.visaSupplierdefaultItem)
          this.visaSuppliereditedIndex = -1
        })
      },

      visaSuppliersave () {
        if (this.visaSuppliereditedIndex > -1) {
          Object.assign(this.visaSupplier[this.visaSuppliereditedIndex], this.visaSuppliereditedItem)
        } else {
          this.visaSuppliereditedItem.page_row_id = this.makeid(20)
          this.visaSupplier.push(this.visaSuppliereditedItem)
        }
        this.visaSupplierclose()
      },

      

      SupplierdeleteItemConfirm () {
        // Supplier  
        this.Supplier.splice(this.SuppliereditedIndex, 1)
      },

      Supplierclose () {
        this.Supplierdialog = false
        this.$nextTick(() => {
          this.SuppliereditedItem = Object.assign({}, this.SupplierdefaultItem)
          this.SuppliereditedIndex = -1
        })
      },

      Suppliersave () {
        if (this.SuppliereditedIndex > -1) {
          Object.assign(this.Supplier[this.SuppliereditedIndex], this.SuppliereditedItem)
        } else {
          this.SuppliereditedItem.page_row_id = this.makeid(20)
          this.Supplier.push(this.SuppliereditedItem)
        }
        this.Supplierclose()
      },


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
    },

    watch: {
      visaSupplierdialog (val) {
        val || this.visaSupplierclose()
      },
      Supplierdialog (val) {
        val || this.Supplierclose()
      },
          
    },

    created () {
      this.$nextTick(function () {
        evntBus.$on('send_detailing_detail', (data) => {
          this.visaSupplier = data.visa_supplier
          this.detailing_detail = data
          this.Supplier = data.supplier
          this.Supplier.forEach(ele => {
            ele.page_row_id = this.makeid(20)
          });
          this.visaSupplier.forEach(ele => {
            ele.page_row_id = this.makeid(20)
          });
        });
      });
    },
  }
</script>