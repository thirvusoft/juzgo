<template>
  <div>
    <v-row>
      <v-col col="12">
        <v-textarea 
          dense
          clearable
          outlined
          color="primary"
          :label="frappe._('Notes for Our Reference')"
          v-model="data.notes_for_our_reference"
          background-color="white"
        ></v-textarea>
      </v-col>
      <v-col col="12">
        <v-textarea 
          dense
          clearable
          outlined
          color="primary"
          :label="frappe._('Common Features')"
          v-model="data.common_features"
          background-color="white"
        ></v-textarea>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { evntBus } from '../../bus';

export default {
  data() {
    return {
      data:[]
    };
  },

  methods: {
    
  },

  created() {
    this.$nextTick(() => {
      evntBus.$on('send_detailing_detail', (data) => {
        this.data = data
      });
    });
  },

  watch:{
  
  }
};

</script>
