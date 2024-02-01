<template>
  <div>
    <v-data-table
      :headers="SpotsHeaders"
      :items="Spots"
      :single-expand="SpotssingleExpand"
      :expanded.sync="Spotsexpanded"
      item-key="page_row_id"
      show-expand
      sort-by="destination"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-toolbar-title>Spots</v-toolbar-title>
          <v-divider
            class="mx-4"
            inset
            vertical
          ></v-divider>
          <v-spacer></v-spacer>
          <v-dialog
            v-model="Spotsdialog"
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
                        v-model="SpotseditedItem.destination"
                        label="Destination"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="SpotseditedItem.supplier"
                        label="Supplier"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="SpotseditedItem.supplier_name"
                        label="Supplier Name"
                      ></v-text-field>
                    </v-col>
                    <v-col
                      cols="12"
                      sm="6"
                      md="4"
                    >
                      <v-text-field
                        v-model="SpotseditedItem.supplier_mail_id"
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
                  @click="Spotsclose"
                >
                  Cancel
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="Spotssave"
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
          @click="SpotsdeleteItemConfirm"
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
      Spotsdialog: false,
      dialogDelete: false,
      Spotsexpanded: [],
      SpotssingleExpand: false,

      SpotsHeaders: [
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
      Spots: [],
      SpotseditedIndex: -1,
      SpotseditedItem: {
        name: '',destination: '',supplier: '',supplier_name: '',supplier_mail_id: '',
      },
      SpotseddefaultItem: {
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

      SpotsdeleteItemConfirm () {
        this.Spots.splice(this.SpotseditedIndex, 1)
      },

      Spotsclose () {
        this.Spotsdialog = false
        this.$nextTick(() => {
          this.SpotseditedItem = Object.assign({}, this.SpotsdefaultItem)
          this.SpotseditedIndex = -1
        })
      },

      Spotssave () {
        if (this.SpotseditedIndex > -1) {
          Object.assign(this.Spots[this.SpotseditedIndex], this.SpotseditedItem)
        } else {
          this.SpotseditedItem.page_row_id = this.makeid(20)
          this.Spots.push(this.SpotseditedItem)
        }
        this.Spotsclose()
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
      Spotsdialog (val) {
        val || this.Spotsclose()
      },
    },

    created () {
      this.$nextTick(function () {
        evntBus.$on('send_detailing_detail', (data) => {
          this.Spots = data.spots
          this.Spots.forEach(ele => {
            ele.page_row_id = this.makeid(20)
          });
        });
      });
    },
  }
</script>