<template>
  <div fluid>
    
    <v-row>
      <v-col xl="3" lg="3" md="3" sm="3" cols="12">
        <InternalOperations></InternalOperations>
      </v-col>
      <v-col xl="9" lg="9" md="9" sm="9" cols="12">
        <Invoice></Invoice>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { evntBus } from '../../bus';
import Invoice from './Invoice.vue';
import InternalOperations from './InternalOperations.vue';

export default {
  data: function () {
    return {
      detailing_detail:''
    };
  },

  components: {
    Invoice,
    InternalOperations
  },

  methods: {
    
  },

  created: function () {
    
  },
};
</script>

<style scoped></style>
