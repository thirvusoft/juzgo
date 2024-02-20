<template>
  <div>
    <v-card
      class="selection mx-auto grey lighten-5 mt-3"
      style="max-height: 80vh; height: 80vh"
    >
      <div class="text-center d-flex pb-4">
        <v-btn @click="all">
          Expand ALL
        </v-btn>
        <v-btn @click="none">
          Collapse ALL
        </v-btn>
      </div>

      <v-expansion-panels
        class="overflow-y-auto" style="max-height: 75vh"
        v-model="panel"
        multiple
      >
        <v-expansion-panel>
          <v-expansion-panel-header>Hotels</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                  <table class="custom-table" v-for="item_ids in Hotel_ids" :key="item_ids">
                    <tr>
                      <th>Options</th>
                      <th v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            {{ item.options }}
                            <button v-if="'Option 1' !== item.options" @click="copyTonext(item,Hotel)"><v-icon color="white" small>mdi-content-copy</v-icon></button>
                            <button @click="clearRow(item,Hotel)"><v-icon color="white" small>mdi-trash-can-outline</v-icon></button>
                          </v-col>
                        </v-row>
                      </th>
                      <th>
                        <button @click="copyAll(item_ids,Hotel)"><v-icon color="white">mdi-content-copy</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Hotel Name</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.hotel_name"
                              :items="get_hotel"
                              background-color="white"
                              :no-data-text="__('Hotel not found')"
                              hide-details
                              required
                              @change="fetch_hotel_category(item)"
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                      <th>
                        <button @click="deleteRow(item_ids,Hotel,Hotel_ids)"><v-icon color="white">mdi-delete-circle</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Hotel Category</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.hotel_category"
                              :items="get_hotel_category"
                              background-color="white"
                              :no-data-text="__('Hotel not found')"
                              hide-details
                              required
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>No of nights</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model.number="item.no_of_nights"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>No of Days</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model.number="item.no_of_days"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Number of pax</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model.number="item.number_of_pax"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Room category</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-select
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              :items="['','Suite Room','Deluxe Room','Interconnected Rooms']"
                              v-model="item.room_category"
                              menu-props="auto"
                            ></v-select>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Meal Preference</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-select
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              :items="['','CP','AP','MAP']"
                              v-model="item.meal_preference"
                              menu-props="auto"
                            ></v-select>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Any Others</th>
                      <td v-for="item in Hotel" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-textarea
                              auto-grow
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.any_other"
                            ></v-textarea>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                  </table>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddHotel()"
                  >
                    Add Hotels
                  </v-btn>
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
                  <table class="custom-table" v-for="item_ids in Spots_ids" :key="item_ids">
                    <tr>
                      <th>Options</th>
                      <th v-for="item in Spots" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            {{ item.options }}
                            <button v-if="'Option 1' !== item.options" @click="copyTonext(item,Spots)"><v-icon color="white" small>mdi-content-copy</v-icon></button>
                            <button @click="clearRow(item,Spots)"><v-icon color="white" small>mdi-trash-can-outline</v-icon></button>
                          </v-col>
                        </v-row>
                      </th>
                      <th>
                        <button @click="copyAll(item_ids,Spots)"><v-icon color="white">mdi-content-copy</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Spots</th>
                      <td v-for="item in Spots" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.spots"
                              :items="get_spots"
                              background-color="white"
                              :no-data-text="__('Spots not found')"
                              hide-details
                              required
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                      <th>
                        <button @click="deleteRow(item_ids,Spots,Spots_ids)"><v-icon color="white">mdi-delete-circle</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Transfer Type</th>
                      <td v-for="item in Spots" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-select
                              dense
                              hide-details
                              color="primary"
                              background-color="white"
                              :items="['','Private','SIC']"
                              v-model="item.transfer_type"
                              menu-props="auto"
                            ></v-select>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                  </table>
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
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Optional cost needed for</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                  <table class="custom-table" v-for="item_ids in OptionalcostDetailing_ids" :key="item_ids">
                    <tr>
                      <th>Options</th>
                      <th v-for="item in OptionalcostDetailing" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            {{ item.options }}
                            <button v-if="'Option 1' !== item.options" @click="copyTonext(item,OptionalcostDetailing)"><v-icon color="white" small>mdi-content-copy</v-icon></button>
                            <button @click="clearRow(item,OptionalcostDetailing)"><v-icon color="white" small>mdi-trash-can-outline</v-icon></button>
                          </v-col>
                        </v-row>
                      </th>
                      <th>
                        <button @click="copyAll(item_ids,OptionalcostDetailing)"><v-icon color="white">mdi-content-copy</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Spots</th>
                      <td v-for="item in OptionalcostDetailing" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.spots"
                              :items="get_spots"
                              background-color="white"
                              :no-data-text="__('Spots not found')"
                              hide-details
                              required
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                      <th>
                        <button @click="deleteRow(item_ids,OptionalcostDetailing,OptionalcostDetailing_ids)"><v-icon color="white">mdi-delete-circle</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Transfer Type</th>
                      <td v-for="item in OptionalcostDetailing" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-select
                              dense
                              hide-details
                              color="primary"
                              background-color="white"
                              :items="['','Private','SIC']"
                              v-model="item.transfer_type"
                              menu-props="auto"
                            ></v-select>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                  </table>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddOptionalcostDetailing()"
                  >
                    Add Optional Cost Detailing
                  </v-btn>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Others</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                    
                  <table class="custom-table" v-for="item_ids in Other_ids" :key="item_ids">
                    <tr>
                      <th>Options</th>
                      <th v-for="item in Others" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            {{ item.options }}
                            <button v-if="'Option 1' !== item.options" @click="copyTonext(item,Others)"><v-icon color="white" small>mdi-content-copy</v-icon></button>
                            <button @click="clearRow(item,Others)"><v-icon color="white" small>mdi-trash-can-outline</v-icon></button>
                          </v-col>
                        </v-row>
                      </th>
                      <th>
                        <button @click="copyAll(item_ids,Others)"><v-icon color="white">mdi-content-copy</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Others</th>
                      <td v-for="item in Others" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-textarea
                              dense
                              color="primary"
                              v-model="item.others"
                              background-color="white"
                              hide-details
                              required
                              auto-grow
                            >
                            </v-textarea>
                          </v-col>
                        </v-row>
                      </td>
                      <th>
                        <button @click="deleteRow(item_ids,Others,Other_ids)"><v-icon color="white">mdi-delete-circle</v-icon></button>
                      </th>
                    </tr>
                  </table>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddOther()"
                  >
                    Add Others
                  </v-btn>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Vehicle</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                    
                  <table class="custom-table" v-for="item_ids in Vehicle_ids" :key="item_ids">
                    <tr>
                      <th>Options</th>
                      <th v-for="item in Vehicle" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            {{ item.options }}
                            <button v-if="'Option 1' !== item.options" @click="copyTonext(item,Vehicle)"><v-icon color="white" small>mdi-content-copy</v-icon></button>
                            <button @click="clearRow(item,Vehicle)"><v-icon color="white" small>mdi-trash-can-outline</v-icon></button>
                          </v-col>
                        </v-row>
                      </th>
                      <th>
                        <button @click="copyAll(item_ids,Vehicle)"><v-icon color="white">mdi-content-copy</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Vehicle</th>
                      <td v-for="item in Vehicle" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.vehicle"
                              :items="get_vehicle"
                              background-color="white"
                              :no-data-text="__('Vehicle not found')"
                              hide-details
                              required
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                      <th>
                        <button @click="deleteRow(item_ids,Vehicle,Vehicle_ids)"><v-icon color="white">mdi-delete-circle</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Transfer type</th>
                      <td v-for="item in Vehicle" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.transfer_type"
                              :items="get_transfer_type"
                              background-color="white"
                              :no-data-text="__('Transfer Type not found')"
                              hide-details
                              required
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Notes</th>
                      <td v-for="item in Vehicle" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-textarea
                              dense
                              color="primary"
                              v-model="item.notes"
                              background-color="white"
                              hide-details
                              auto-grow
                            >
                            </v-textarea>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                  </table>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddVehicle()"
                  >
                    Add Vehicle
                  </v-btn>
                </v-col>
              </v-row>
            </template>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header>Cruise</v-expansion-panel-header>
          <v-expansion-panel-content>
            <template>
              <v-row>
                <v-col>
                    
                  <table class="custom-table" v-for="item_ids in Cruise_ids" :key="item_ids">
                    <tr>
                      <th>Options</th>
                      <th v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            {{ item.options }}
                            <button v-if="'Option 1' !== item.options" @click="copyTonext(item,Cruise)"><v-icon color="white" small>mdi-content-copy</v-icon></button>
                            <button @click="clearRow(item,Cruise)"><v-icon color="white" small>mdi-trash-can-outline</v-icon></button>
                          </v-col>
                        </v-row>
                      </th>
                      <th>
                        <button @click="copyAll(item_ids,Cruise)"><v-icon color="white">mdi-content-copy</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Check In Date</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-menu
                              ref="check_in_date_menu"
                              v-model="item.check_in_date_menu"
                              :close-on-content-click="false"
                              transition="scale-transition"
                              dense
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="item.check_in_date"
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
                                v-model="item.check_in_date"
                                color="primary"
                                no-title
                                scrollable
                                @input="item.check_in_date_menu = false"
                              >
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                        </v-row>
                      </td>
                      <th>
                        <button @click="deleteRow(item_ids,Cruise,Cruise_ids)"><v-icon color="white">mdi-delete-circle</v-icon></button>
                      </th>
                    </tr>
                    <tr>
                      <th>Check Out Date</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-menu
                              ref="check_out_date_menu"
                              v-model="item.check_out_date_menu"
                              :close-on-content-click="false"
                              transition="scale-transition"
                              dense
                            >
                              <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                  v-model="item.check_out_date"
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
                                v-model="item.check_out_date"
                                color="primary"
                                no-title
                                scrollable
                                @input="item.check_out_date_menu = false"
                              >
                              </v-date-picker>
                            </v-menu>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>No of Adults</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model.number="item.no_of_adults"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>No of Child</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model.number="item.no_of_child"
                              type="number"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Child Ages</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.child_ages"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>No of Rooms Required</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.no_of_rooms_required"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Room type</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-autocomplete
                              dense
                              auto-select-first
                              color="primary"
                              v-model="item.room_type"
                              :items="get_room_type"
                              background-color="white"
                              :no-data-text="__('Room Type not found')"
                              hide-details
                            >
                            </v-autocomplete>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Cabin Size</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.cabin_size"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>View From Rooms</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.view_from_rooms"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Max no Beds Cabin Possible To Be Accomodated</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.max_no_of_beds_in_this_cabin_possible_to_be_accomodated"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Room spec & Amenities</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.room_spec_and_amenities"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                    <tr>
                      <th>Cost per Pax Detail</th>
                      <td v-for="item in Cruise" :key="item.det_idx" v-if="item_ids === item.det_id">
                        <v-row>
                          <v-col class="text-left">
                            <v-text-field
                              dense
                              color="primary"
                              background-color="white"
                              hide-details
                              v-model="item.cost_per_pax_in_detail"
                            ></v-text-field>
                          </v-col>
                        </v-row>
                      </td>
                    </tr>
                  </table>
                  <v-btn
                    color="primary"
                    dark
                    class="mb-2"
                    @click="AddCruise()"
                  >
                    Add Cruise
                  </v-btn>
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

      panel: [],
      items: 6,

      Spots: [],
      Spots_ids:[],

      Hotel: [],
      Hotel_ids:[],

      OptionalcostDetailing: [],
      OptionalcostDetailing_ids:[],

      Others: [],
      Other_ids:[],
      
      Vehicle: [],
      Vehicle_ids:[],

      Cruise:[],
      Cruise_ids:[],

      get_hotel:[],
      get_spots:[],
      get_hotel_category:[],
      get_vehicle:[],
      get_transfer_type:[],
      get_room_type:[],
    };
  },

  methods: {
    AddSpots(){
      var id = this.makeid(20)
      for(var i=1;i<6;i++){
        this.Spots.push({
          options: "Option "+i, 
          det_id: id, 
          det_idx: this.makeid(20), 
          spots:'', 
          transfer_type:''
        })
      }
      this.Spots_ids.push(id)
    },

    AddHotel(){
      var id = this.makeid(20)
      for(var i=1;i<6;i++){
        this.Hotel.push({
          options: "Option "+i,
          det_id: id, 
          det_idx: this.makeid(20), 
          hotel_name: '', 
          no_of_nights: '', 
          no_of_days: '', 
          number_of_pax: '',
          room_category: '',
          meal_preference: '',
          any_other: '',
          hotel_category: '',
        })
      }
      this.Hotel_ids.push(id)
    },

    AddOptionalcostDetailing(){
      var id = this.makeid(20)
      for(var i=1;i<2;i++){
        this.OptionalcostDetailing.push({
          options: "Comman",
          det_id: id, 
          det_idx: this.makeid(20), 
          spots:'', 
          transfer_type:'',
        })
      }
      this.OptionalcostDetailing_ids.push(id)
    },

    AddOther(){
      var id = this.makeid(20)
      for(var i=1;i<2;i++){
        this.Others.push({
          options: "Comman",
          det_id: id, 
          det_idx: this.makeid(20), 
          others:'', 
        })
      }
      this.Other_ids.push(id)
    },

    AddVehicle(){
      var id = this.makeid(20)
      for(var i=1;i<6;i++){
        this.Vehicle.push({
          options: "Option "+i,
          det_id: id, 
          det_idx: this.makeid(20), 
          vehicle:'', 
          transfer_type:'',
          notes:''
        })
      }
      this.Vehicle_ids.push(id)
    },

    AddCruise(){
      var id = this.makeid(20)
      for(var i=1;i<6;i++){
        this.Cruise.push({
          options: "Option "+i,
          det_id: id, 
          det_idx: this.makeid(20), 
          check_in_date:'',
          check_out_date:'',
          no_of_adults:'',
          no_of_child:'',
          child_ages:'',
          no_of_rooms_required:'',
          room_type:'',
          cabin_size:'',
          view_from_rooms:'',
          max_no_of_beds_in_this_cabin_possible_to_be_accomodated:'',
          room_spec_and_amenities:'',
          cost_per_pax_in_detail:'',
          check_in_date_menu: false,
          check_out_date_menu: false,
        })
      }
      this.Cruise_ids.push(id)
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
      this.get_spots = this.get_list("Spots",this.get_spots)
      this.get_hotel = this.get_list("Hotel Details",this.get_hotel)
      this.get_hotel_category = this.get_list("Hotel Category",this.get_hotel_category)
      this.get_transfer_type = this.get_list("Transfers",this.get_transfer_type)
      this.get_vehicle = this.get_list("Vehicle Detail",this.get_vehicle)
      this.get_room_type = this.get_list("Room Type",this.get_room_type)
    },

    get_list(doctype,list){
      if (list.length > 0) return;
      frappe.db
        .get_list(doctype, {
          fields: ['name'],
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

    copyAll(item_ids,field_name){
      let non_changable = ['name', 'owner', 'det_id', 'det_idx', 'creation', "modified", "modified_by", "docstatus", "idx", "parent", "parentfield", "parenttype", "doctype", "options"]
      for(var i=0;i<field_name.length;i++){
        if(field_name[i].det_id == item_ids && field_name[i].options == "Option 1"){
          for(var j=0;j<field_name.length;j++){
            if(field_name[j].det_id == item_ids && field_name[j].options != "Option 1"){
              for (const key in field_name[j]) {
                if (field_name[j].hasOwnProperty(key) && !non_changable.includes(key)) {
                  Vue.set(field_name[j], key, field_name[i][key]);
                }
              }
            }
          }
        }
      }
    },
    copyTonext(item,field_name){
      let non_changable = ['name', 'owner', 'det_id', 'det_idx', 'creation', "modified", "modified_by", "docstatus", "idx", "parent", "parentfield", "parenttype", "doctype", "options"]
      for (var i = 0; i < field_name.length; i++) {
        if (field_name[i].det_idx == item.det_idx) {
          for (const key in field_name[(i - 1)]) {
            if (field_name[(i - 1)].hasOwnProperty(key) && !non_changable.includes(key)) {
              Vue.set(item, key, field_name[(i - 1)][key]);
            }
          }
        }
      }
    },
    clearRow(item,field_name){
      let non_changable = ['name', 'owner', 'det_id', 'det_idx', 'creation', "modified", "modified_by", "docstatus", "idx", "parent", "parentfield", "parenttype", "doctype", "options"]
      for (var i = 0; i < field_name.length; i++) {
        if (field_name[i].det_idx == item.det_idx) {
          for (const key in field_name[i]) {
            if (field_name[(i)].hasOwnProperty(key) && !non_changable.includes(key)) {
              Vue.set(item, key, '');
            }
          }
        }
      }
    },
    deleteRow(item_ids,field_name,item_ids_list){
      let ids = []
      for(var i=0;i<field_name.length;i++){
        if(field_name[i].det_id == item_ids){
          ids.push(i)
        }
      }
      ids.reverse();
      ids.forEach((ele) => {
        field_name.splice(ele, 1)
      })
      for(var i=0;i<item_ids_list.length;i++){
        if(item_ids_list[i] == item_ids){
          item_ids_list.splice(i, 1)
        }
      }
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
    fetch_hotel_category(item){
      frappe.db.get_value('Hotel Details', item.hotel_name, ['hotel_category'], (r) => {
        Vue.set(item, "hotel_category", r.hotel_category);
      })
    },
  },

  created() {
    this.$nextTick(() => {
      evntBus.$on('send_detailing_detail', (data) => {
        this.data = data
        this.Spots = data.spots
        this.push_ids_list(this.Spots,this.Spots_ids)
        this.Hotel = data.hotels
        this.push_ids_list(this.Hotel,this.Hotel_ids)
        this.OptionalcostDetailing = data.optional_cost_needed_for
        this.push_ids_list(this.OptionalcostDetailing,this.OptionalcostDetailing_ids)
        this.Others = data.others
        this.push_ids_list(this.Others,this.Other_ids)
        this.Vehicle = data.vehicle
        this.push_ids_list(this.Vehicle,this.Vehicle_ids)
        this.Cruise = data.cruise
        this.push_ids_list(this.Cruise,this.Cruise_ids)
      });
      this.name_list_order()
    });
  },

  watch:{
  
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
