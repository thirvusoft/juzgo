<template>
  <v-app class="container1">
    <v-main>
      <Navbar @changePage="setPage($event)"></Navbar>
      <keep-alive>
        <component v-bind:is="page" class="mx-4 md-4"></component>
      </keep-alive>
    </v-main>
  </v-app>
</template>

<script>
import { evntBus } from './bus';
import Navbar from './components/Navbar.vue';
import DetailingMain from './components/pos/DetailingMain.vue';
import QuotationCompareMain from './components/pos/QuotationCompareMain.vue';

export default {
  data: function () {
    return {
      detailing_detail:'',
      page: 'DetailingMain',
    };
  },
  components: {
    Navbar,
    DetailingMain,
    QuotationCompareMain
  },
  methods: {
    setPage(page_name) {
      this.page = page_name;
      if(page_name == "Home"){
        const win = window.open(
          '/app',
          '_blank'
        );
        win.focus();
      }
      if(page_name == "CA Form"){
        const win = window.open(
          '/app/ca-form',
          '_blank'
        );
        win.focus();
      }
      if(page_name == "Project"){
        const win = window.open(
          '/app/project',
          '_blank'
        );
        win.focus();
      }
      if(page_name == "Quotation Comparission"){
        this.page = "QuotationCompareMain";
      }
      if(page_name == "Detailing"){
        this.page = "DetailingMain";
      }
      
    },
    
  },
  mounted() {
  },
  updated() {},
  created: function () {
   
  },
};
</script>

<style scoped>
.container1 {
  margin-top: 0px;
}
</style>