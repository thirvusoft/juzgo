<template>
  <v-card>
    <v-tabs
      v-model="tab"
      align-with-title
    >
      <v-tabs-slider color="primary"></v-tabs-slider>
      <v-tab value="supplier_mail_details">Supplier Mail Details</v-tab>
      <v-tab value="inclusion" @click="pass_detailing_detail()">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <span v-on="on">Inclusion</span>
          </template>
          <span>Double Click</span>
        </v-tooltip>
      </v-tab>
      <v-tab value="notes" @click="pass_detailing_detail()">
        <v-tooltip bottom>
          <template v-slot:activator="{ on }">
            <span v-on="on">Notes & Common Features</span>
          </template>
          <span>Double Click</span>
        </v-tooltip>
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <SupplierMail></SupplierMail>
          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <Inclusion></Inclusion>
          </v-card-text>
        </v-card>
      </v-tab-item>
      <v-tab-item>
        <v-card flat>
          <v-card-text>
            <Notes></Notes>
          </v-card-text>
        </v-card>
      </v-tab-item>
    </v-tabs-items>
  </v-card>
</template>

<script>
  import SupplierMail from './SupplierMail.vue'
  import Inclusion from './Inclusion.vue'
  import Notes from './Notes.vue';
  import { evntBus } from '../../bus';
  export default {
    data () {
      return {
        tab: null,
        detailing_detail: ''
      }
    },
    components: {
      SupplierMail,
      Inclusion,
      Notes,
    },
  
    computed: {
      
    },

    methods: {
      pass_detailing_detail() {
        this.$nextTick(() => {
          evntBus.$emit('send_detailing_detail', this.detailing_detail);
        });
      },
    },

    created() {
      evntBus.$on('send_detailing_detail', (data) => {
        this.detailing_detail = data
      })
    },
    destroyed() {
      
    },
    watch: {
      
    },
  }
</script>