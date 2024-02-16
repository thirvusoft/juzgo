<template>
    <div>
      <v-data-table
        :headers="AirTicketHeaders"
        :items="AirTicket"
        :single-expand="AirTicketsingleExpand"
        :expanded.sync="AirTicketexpanded"
        item-key="page_row_id"
        show-expand
        sort-by="destination"
        class="elevation-1"
      >
        <template v-slot:top>
          <v-toolbar
            flat
          >
            <v-toolbar-title>AirTicket</v-toolbar-title>
            <v-divider
              class="mx-4"
              inset
              vertical
            ></v-divider>
            <v-spacer></v-spacer>
            <v-dialog
              v-model="AirTicketdialog"
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
                          v-model="AirTicketeditedItem.destination"
                          label="Destination"
                        ></v-text-field>
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="AirTicketeditedItem.supplier"
                          label="Supplier"
                        ></v-text-field>
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="AirTicketeditedItem.supplier_name"
                          label="Supplier Name"
                        ></v-text-field>
                      </v-col>
                      <v-col
                        cols="12"
                        sm="6"
                        md="4"
                      >
                        <v-text-field
                          v-model="AirTicketeditedItem.supplier_mail_id"
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
                    @click="AirTicketclose"
                  >
                    Cancel
                  </v-btn>
                  <v-btn
                    color="blue darken-1"
                    text
                    @click="AirTicketsave"
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
            @click="AirTicketdeleteItemConfirm"
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
        AirTicketdialog: false,
        dialogDelete: false,
        AirTicketexpanded: [],
        AirTicketsingleExpand: false,
  
        AirTicketHeaders: [
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
        AirTicket: [],
        AirTicketeditedIndex: -1,
        AirTicketeditedItem: {
          name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '',
        },
        AirTicketeddefaultItem: {
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
  
        AirTicketdeleteItemConfirm () {
          this.AirTicket.splice(this.AirTicketeditedIndex, 1)
        },
  
        AirTicketclose () {
          this.AirTicketdialog = false
          this.$nextTick(() => {
            this.AirTicketeditedItem = Object.assign({}, this.AirTicketdefaultItem)
            this.AirTicketeditedIndex = -1
          })
        },
  
        AirTicketsave () {
          if (this.AirTicketeditedIndex > -1) {
            Object.assign(this.AirTicket[this.AirTicketeditedIndex], this.AirTicketeditedItem)
          } else {
            this.AirTicketeditedItem.page_row_id = this.makeid(20)
            this.AirTicket.push(this.AirTicketeditedItem)
          }
          this.AirTicketclose()
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
        AirTicketdialog (val) {
          val || this.AirTicketclose()
        },
      },
  
      created () {
        this.$nextTick(function () {
          evntBus.$on('send_detailing_detail', (data) => {
            this.AirTicket = data.AirTicket
            this.AirTicket.forEach(ele => {
              ele.page_row_id = this.makeid(20)
            });
          });
        });
      },
    }
  </script>