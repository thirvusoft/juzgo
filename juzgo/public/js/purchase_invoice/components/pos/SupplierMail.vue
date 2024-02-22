<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5 mt-3"
      style="max-height: 80vh; height: 80vh"
    >
      <v-card
      class="overflow-y-auto" style="max-height: 82vh"
      >
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
          <template v-slot:item.supplier="{ item }">
            <v-select
              color="primary"
              :items="get_supplier"
              background-color="white"
              v-model="item.supplier"
              @change="get_supplier_details(item)"
            ></v-select>
          </template>
          <template v-slot:item.supplier_mail_id="{ item }">
            <v-text-field
              color="primary"
              background-color="white"
              v-model="item.supplier_mail_id"
            ></v-text-field>
          </template>
          <template v-slot:item.hotels="{ item }">
            <v-simple-checkbox
              v-model="item.hotels"
            ></v-simple-checkbox>
          </template>
          <template v-slot:item.spots="{ item }">
            <v-simple-checkbox
              v-model="item.spots"
            ></v-simple-checkbox>
          </template>
          <template v-slot:item.vehicle="{ item }">
            <v-simple-checkbox
              v-model="item.vehicle"
            ></v-simple-checkbox>
          </template>
          <template v-slot:item.optional_costs="{ item }">
            <v-simple-checkbox
              v-model="item.optional_costs"
            ></v-simple-checkbox>
          </template>
          <template v-slot:item.others="{ item }">
            <v-simple-checkbox
              v-model="item.others"
            ></v-simple-checkbox>
          </template>
          <template v-slot:item.cruise="{ item }">
            <v-simple-checkbox
              v-model="item.cruise"
            ></v-simple-checkbox>
          </template>
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
                    New Supplier
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
                          <v-select
                            dense
                            color="primary"
                            :label="frappe._('Supplier')"
                            :items="get_supplier"
                            background-color="white"
                            v-model="SuppliereditedItem.supplier"
                            @change="get_supplier_details(SuppliereditedItem)"
                          ></v-select>
                        </v-col>
                        <!-- <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-text-field
                            dense
                            color="primary"
                            :label="frappe._('Supplier Name')"
                            background-color="white"
                            v-model="SuppliereditedItem.supplier_name"
                          ></v-text-field>
                        </v-col> -->
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-text-field
                            dense
                            color="primary"
                            :label="frappe._('Supplier Mail ID')"
                            background-color="white"
                            v-model="SuppliereditedItem.supplier_mail_id"
                          ></v-text-field>
                        </v-col>
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-checkbox
                            dense
                            color="primary"
                            :label="frappe._('Hotels')"
                            background-color="white"
                            v-model="SuppliereditedItem.hotels"
                          ></v-checkbox>
                        </v-col>
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-checkbox
                            dense
                            color="primary"
                            :label="frappe._('Spots')"
                            background-color="white"
                            v-model="SuppliereditedItem.spots"
                          ></v-checkbox>
                        </v-col>
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-checkbox
                            dense
                            color="primary"
                            :label="frappe._('Vehicle')"
                            background-color="white"
                            v-model="SuppliereditedItem.vehicle"
                          ></v-checkbox>
                        </v-col>
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-checkbox
                            dense
                            color="primary"
                            :label="frappe._('Optional Costs')"
                            background-color="white"
                            v-model="SuppliereditedItem.optional_costs"
                          ></v-checkbox>
                        </v-col>
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-checkbox
                            dense
                            color="primary"
                            :label="frappe._('Others')"
                            background-color="white"
                            v-model="SuppliereditedItem.others"
                          ></v-checkbox>
                        </v-col>
                        <v-col 
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-checkbox
                            dense
                            color="primary"
                            :label="frappe._('Cruise')"
                            background-color="white"
                            v-model="SuppliereditedItem.cruise"
                          ></v-checkbox>
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
                  <v-select
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Supplier')"
                    background-color="white"
                    hide-details
                    :items="get_supplier"
                    v-model="item.supplier"
                    @change="get_supplier_details(item)"
                  ></v-select>
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
                    :label="frappe._('Supplier Mail ID')"
                    background-color="white"
                    hide-details
                    v-model="item.supplier_mail_id"
                  ></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Hotels')"
                    background-color="white"
                    hide-details
                    v-model="item.hotels"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Spots')"
                    background-color="white"
                    hide-details
                    v-model="item.spots"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Vehicle')"
                    background-color="white"
                    hide-details
                    v-model="item.vehicle"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Optional Costs')"
                    background-color="white"
                    hide-details
                    v-model="item.optional_costs"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Others')"
                    background-color="white"
                    hide-details
                    v-model="item.others"
                  ></v-checkbox>
                </v-col>
                <v-col cols="4">
                  <v-checkbox
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Cruise')"
                    background-color="white"
                    hide-details
                    v-model="item.cruise"
                  ></v-checkbox>
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
            <v-icon
              small
              @click="SupplieremailsendItemConfirm(item)"
            >
              mdi-email-send
            </v-icon>
          </template>
        </v-data-table>
        
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
          <template v-slot:item.destination="{ item }">
            <v-select
              v-model="item.destination"
              :items="get_destination"
            ></v-select>
          </template>
          <template v-slot:item.supplier="{ item }">
            <v-select
              v-model="item.supplier"
              :items="get_supplier"
              @change="get_supplier_details(item,'supplier')"
            ></v-select>
          </template>
          <template v-slot:item.supplier_mail_id="{ item }">
            <v-text-field
              v-model="item.supplier_mail_id"
            ></v-text-field>
          </template>
          <template v-slot:item.travel_from_dates="{ item }">
            <v-menu
              v-model="item.check_travel_from_datess"
              :close-on-content-click="false"
              transition="scale-transition"
              dense
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="item.travel_from_dates"
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
                v-model="item.travel_from_dates"
                color="primary"
                no-title
                scrollable
                @input="item.check_travel_from_datess= false"
              >
              </v-date-picker>
            </v-menu>
          </template>
          <template v-slot:item.travel_to_dates="{ item }">
            <v-menu
              v-model="item.check_travel_to_datess"
              :close-on-content-click="false"
              transition="scale-transition"
              dense
            >
              <template v-slot:activator="{ on, attrs }">
                <v-text-field
                  v-model="item.travel_to_dates"
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
                v-model="item.travel_to_dates"
                color="primary"
                no-title
                scrollable
                @input="item.check_travel_to_datess = false"
              >
              </v-date-picker>
            </v-menu>
          </template>
          <template v-slot:item.duration_of_stay_in_destination="{ item }">
            <v-text-field
              v-model="item.duration_of_stay_in_destination"
            ></v-text-field>
          </template>
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
                    New Visa Supplier
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
                          <v-select
                            v-model="visaSuppliereditedItem.destination"
                            :items="get_destination"
                            label="Destination"
                          ></v-select>
                        </v-col>
                        <v-col
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-select
                            @change="get_supplier_details(visaSuppliereditedItem,'supplier')"
                            v-model="visaSuppliereditedItem.supplier"
                            :items="get_supplier"
                            label="Supplier"
                          ></v-select>
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
                          <v-menu
                            ref="check_travel_from_dates"
                            v-model="visaSuppliereditedItem.check_travel_from_dates"
                            :close-on-content-click="false"
                            transition="scale-transition"
                            dense
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="visaSuppliereditedItem.travel_from_dates"
                                readonly
                                label="Travel From dates"
                                dense
                                clearable
                                hide-details
                                v-bind="attrs"
                                v-on="on"
                                color="primary"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              v-model="visaSuppliereditedItem.travel_from_dates"
                              color="primary"
                              no-title
                              scrollable
                              @input="visaSuppliereditedItem.check_travel_from_dates = false"
                            >
                            </v-date-picker>
                          </v-menu>
                        </v-col>
                        <v-col
                          cols="12"
                          sm="6"
                          md="4"
                        >
                          <v-menu
                            v-model="visaSuppliereditedItem.check_travel_to_dates"
                            :close-on-content-click="false"
                            transition="scale-transition"
                            dense
                          >
                            <template v-slot:activator="{ on, attrs }">
                              <v-text-field
                                v-model="visaSuppliereditedItem.travel_to_dates"
                                readonly
                                label="Travel To dates"
                                dense
                                clearable
                                hide-details
                                v-bind="attrs"
                                v-on="on"
                                color="primary"
                              ></v-text-field>
                            </template>
                            <v-date-picker
                              v-model="visaSuppliereditedItem.travel_to_dates"
                              color="primary"
                              no-title
                              scrollable
                              @input="visaSuppliereditedItem.check_travel_to_dates = false"
                            >
                            </v-date-picker>
                          </v-menu>
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
                          sm="12"
                          md="12"
                        >
                          <v-textarea
                            v-model="visaSuppliereditedItem.questions"
                            label="Questions"
                            auto-grow
                          ></v-textarea>
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
                  <v-select
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Destination')"
                    :items="get_destination"
                    background-color="white"
                    hide-details
                    v-model="item.destination"
                  ></v-select>
                </v-col>
                <v-col cols="4">
                  <v-select
                    dense
                    outlined
                    @change="get_supplier_details(item,'supplier')"
                    color="primary"
                    :label="frappe._('Supplier')"
                    :items="get_supplier"
                    background-color="white"
                    hide-details
                    v-model="item.supplier"
                  ></v-select>
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
                    readonly
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
                <v-col
                  cols="4"
                >
                  <v-menu
                    v-model="item.check_travel_from_dates"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    dense
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="item.travel_from_dates"
                        readonly
                        label="Travel From dates"
                        dense
                        clearable
                        hide-details
                        outlined
                        v-bind="attrs"
                        v-on="on"
                        color="primary"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="item.travel_from_dates"
                      color="primary"
                      no-title
                      scrollable
                      @input="item.check_travel_from_dates = false"
                    >
                    </v-date-picker>
                  </v-menu>
                </v-col>
                <v-col
                  cols="4"
                >
                  <v-menu
                    v-model="item.check_travel_to_dates"
                    :close-on-content-click="false"
                    transition="scale-transition"
                    dense
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        v-model="item.travel_to_dates"
                        readonly
                        label="Travel To dates"
                        dense
                        clearable
                        hide-details
                        outlined
                        v-bind="attrs"
                        v-on="on"
                        color="primary"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="item.travel_to_dates"
                      color="primary"
                      no-title
                      scrollable
                      @input="item.check_travel_to_dates = false"
                    >
                    </v-date-picker>
                  </v-menu>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Duration of stay in Destination')"
                    background-color="white"
                    hide-details
                    v-model="item.duration_of_stay_in_destination"
                  ></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('No of Adults')"
                    background-color="white"
                    hide-details
                    v-model="item.no_of_adults"
                  ></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('No of Child')"
                    background-color="white"
                    hide-details
                    v-model="item.no_of_child"
                  ></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Child Ages')"
                    background-color="white"
                    hide-details
                    v-model="item.child_ages"
                  ></v-text-field>
                </v-col>
                <v-col cols="4">
                  <v-text-field
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Visa type')"
                    background-color="white"
                    hide-details
                    v-model="item.visa_type"
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-textarea
                    dense
                    outlined
                    color="primary"
                    :label="frappe._('Questions')"
                    background-color="white"
                    hide-details
                    v-model="item.questions"
                    auto-grow
                  ></v-textarea>
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
            <v-icon
              small
              @click="visaSupplieremailsendItemConfirm(item)"
            >
              mdi-email-send
            </v-icon>
          </template>
        </v-data-table>
      </v-card>
    </v-card>
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
        // { text: 'Supplier Name', value: 'supplier_name' },
        { text: 'Supplier Mail ID', value: 'supplier_mail_id' },
        { text: 'Travel From dates ', value: 'travel_from_dates' },
        { text: 'Travel To dates ', value: 'travel_to_dates' },
        { text: 'Duration of stay in Destination', value: 'duration_of_stay_in_destination' },
        // { text: 'No of Adults', value: 'no_of_adults' },
        // { text: 'No of Child', value: 'no_of_child' },
        // { text: 'Child Ages', value: 'child_ages' },
        // { text: 'Visa type', value: 'visa_type' },
        // { text: 'Questions', value: 'questions' },
        // { text: 'Send mail', value: 'no_of_adults',sortable: false },
        { text: 'Actions', value: 'actions', sortable: false },
      ],
      visaSupplier: [],
      visaSuppliereditedIndex: -1,
      visaSuppliereditedItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '', travel_from_dates: '',travel_to_dates: '',duration_of_stay_in_destination: '',no_of_adults: '',no_of_child: '',child_ages: '',visa_type: '',questions: '',
      },
      visaSuppliereddefaultItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '', travel_from_dates: '',travel_to_dates: '',duration_of_stay_in_destination: '',no_of_adults: '',no_of_child: '',child_ages: '',visa_type: '',questions: '',
      },


      Supplierdialog: false,
      Supplierexpanded: [],
      SuppliersingleExpand: false,

      SupplierHeaders: [
        { text: 'Supplier', value: 'supplier' },
        // { text: 'Supplier Name', value: 'supplier_name' },
        { text: 'Supplier Mail ID', value: 'supplier_mail_id' },
        { text: 'Hotels', value: 'hotels', },
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
        name: '',supplier: '',supplier_name: '',supplier_mail_id: '',hotels: '',spots: '',vehicle: '',optional_costs: '',others: '',cruise: '',
      },
      SuppliereddefaultItem: {
        name: '',supplier: '',supplier_name: '',supplier_mail_id: '',hotels: '',spots: '',vehicle: '',optional_costs: '',others: '',cruise: '',
      },


      get_supplier: [],
      get_destination: [],

      check_travel_from_dates : false,

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
      async visaSupplieremailsendItemConfirm (item){
        const { message } = await frappe.call({
            method: "frappe.email.doctype.email_template.email_template.get_email_template",
            args: {
                template_name: "Detailing Page Visa",
                doc: item,
            },
        });
        frappe.call({
          method: 'juzgo.api.detailing.get_attach',
          args:{
            detailing_detail:this.detailing_detail
          },
          callback: function (r) {
            if (r.message) {
              const args = {
                subject: message.subject,
                recipients: item.supplier_mail_id,
                attach_document_print: false, 
                message: message.message,
                attachments: r.message,
              };

              new frappe.views.CommunicationComposer(args);
            }
          },
        });
      },
      async SupplieremailsendItemConfirm (item){
        const vm = this
        frappe.call({
          method: 'juzgo.api.detailing.get_mailing_details',
          args:{
            detailing_detail:vm.detailing_detail,
            item:item,
          },
          callback: async function (r) {
            if (r.message) {
              console.log(r.message)
              const { message } = await frappe.call({
                method: "frappe.email.doctype.email_template.email_template.get_email_template",
                args: {
                    template_name: "Supplier",
                    doc: r.message,
                },
            });
            frappe.call({
              method: 'juzgo.api.detailing.get_attach',
              args:{
                detailing_detail:vm.detailing_detail
              },
              callback: function (ra) {
                if (ra.message) {
                  const args = {
                    subject: message.subject,
                    recipients: item.supplier_mail_id,
                    attach_document_print: false, 
                    message: message.message,
                    attachments: ra.message,
                  };

                  new frappe.views.CommunicationComposer(args);
                }
              },
            });
            }
          },
        });
        
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

      async get_supplier_details(item,only_supplier=null){
        frappe.db.get_value('Supplier', item.supplier, ['email_id','supplier_name'], (r) => {
          Vue.set(item, "supplier_mail_id", r.email_id);
          Vue.set(item, "supplier_name", r.supplier_name);
        })
        if(only_supplier){
          frappe.db.get_value('CA Form', this.detailing_detail.ca_form, ['travel_start_date','travel_end_date', 'no_of_adult', 'no_of_childrens', 'child_without_bed', 'no_of_infant'], (r) => {
            Vue.set(item, "travel_from_dates", r.travel_start_date);
            Vue.set(item, "travel_to_dates", r.travel_end_date);
            Vue.set(item, "no_of_adults", r.no_of_adult);
            Vue.set(item, "no_of_child", r.no_of_childrens + r.child_without_bed + r.no_of_infant);
            console.log(this.detailing_detail,r)
          })
        }
        
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

      name_list_order(){
        this.get_supplier = this.get_list("Supplier",this.get_supplier)
        this.get_destination = this.get_list("Destination",this.get_destination)
        evntBus.$emit('send_destination_list', this.detailing_detail);
      },

      get_list(doctype,list){
        frappe.db
          .get_list(doctype, {
            fields: ['name'],
            limit: 10000,
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
          if(data){
            this.visaSupplier = data.visa_supplier
            this.detailing_detail = data
            this.Supplier = data.supplier
            this.Supplier.forEach(ele => {
              ele.page_row_id = this.makeid(20)
            });
            this.visaSupplier.forEach(ele => {
              ele.page_row_id = this.makeid(20)
            });
            this.name_list_order()
          }
        });
      });
    },
  }
</script>