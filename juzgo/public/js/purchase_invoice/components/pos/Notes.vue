<template>
  <div v-if="AirTicket.length > 0">
    <v-card
      class="selection mx-auto grey lighten-5 mt-3 overflow-y-auto"
      style="max-height: 80vh; height: 80vh"
    >
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
            auto-grow
            row-height="50"
          ></v-textarea>
        </v-col>
      </v-row>
      <v-row>
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
          
          <template v-slot:item.airticket="{ item }">
            <v-text-field
              v-model="item.airticket"
              readonly
            ></v-text-field>
          </template>
          <template v-slot:item.airticket_file="{ item }">
            <v-file-input
              @change="fileupload(item.airticket_file,item)"
              v-model="item.airticket_file"
            ></v-file-input>
          </template>
          <template v-slot:item.notes="{ item }">
            <v-text-field
              v-model="item.notes"
            >
            </v-text-field>
          </template>
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
                    New Airticket
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5">{{ formTitle }}</span>
                  </v-card-title>
    
                  <v-card-text>
                    <v-container>
                      <v-row class="ma-0 pa-0">
                        <v-col cols="12">
                          <v-file-input
                            v-model="AirTicketeditedItem.airticket_file"
                            placeholder="Upload your documents"
                            label="File input"
                            @change="fileupload(AirTicketeditedItem.airticket_file,AirTicketeditedItem)"
                            prepend-icon="mdi-paperclip"
                          ></v-file-input>
                        </v-col>
                        <v-col cols="12">
                          <v-textarea
                            dense
                            color="primary"
                            label="Notes"
                            v-model="AirTicketeditedItem.notes"
                            background-color="white"
                            hide-details
                            auto-grow
                          >
                          </v-textarea>
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
                <!-- <v-col cols="6">
                  <v-file-input
                    v-model="item.airticket_file"
                    placeholder="Upload your documents"
                    label="File input"
                    @change="fileupload(item.airticket_file,item)"
                    prepend-icon="mdi-paperclip"
                  ></v-file-input>
                </v-col> -->
                <v-col cols="12">
                  <v-text-field
                    v-model="item.airticket"
                    readonly
                  ></v-text-field>
                </v-col>
                <v-col cols="12">
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
      </v-row>
    </v-card>
  </div>
  <div v-else>
    <H1>Click Again Notes & Comman Features</H1>
  </div>
</template>
   
<script>
import { evntBus } from '../../bus';

export default {
  data() {
    return {
      data:[],

      AirTicketdialog: false,
      dialogDelete: false,
      AirTicketexpanded: [],
      AirTicketsingleExpand: false,

      AirTicketHeaders: [
        { text: 'Airticket', align: 'start',value: 'airticket' },
        { text: 'Notes', value: 'notes' },
        { text: 'Actions', value: 'actions', sortable: false }
      ],
      AirTicket: [],
      AirTicketeditedIndex: -1,
      AirTicketeditedItem: {
        name: '',airticket_file: '',airticket: '',notes: '',
      },
      AirTicketeddefaultItem: {
        name: '',airticket_file: '',airticket: '',notes: '',
      },
      airticket_file :'',
      folder : 'Home/Attachments',
    };
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
    fileupload(airticket,item){
      const vm = this      
      var file ={
        doc:{
          attached_to_doctype: vm.data.doctype,
          attached_to_name: vm.data.name,
          doctype: "File",
          file_name: airticket.name,
          file_url: "/files/"+airticket.name,
          folder: "Home/Attachments",
          is_attachments_folder: 0,
          is_folder: 1,
          is_home_folder: 0,
          is_private: 0,
        },
        file_obj:airticket,
        name: airticket.name,
        optimize: false,
        private: false,
      }
			return new Promise((resolve, reject) => {
				let xhr = new XMLHttpRequest();
				xhr.upload.addEventListener("loadstart", (e) => {
					file.uploading = true;
				});
				xhr.upload.addEventListener("progress", (e) => {
					if (e.lengthComputable) {
						file.progress = e.loaded;
						file.total = e.total;
					}
				});
				xhr.upload.addEventListener("load", (e) => {
					file.uploading = false;
					resolve();
				});
				xhr.addEventListener("error", (e) => {
					file.failed = true;
					reject();
				});
				xhr.onreadystatechange = () => {
					if (xhr.readyState == XMLHttpRequest.DONE) {
						if (xhr.status === 200) {
							file.request_succeeded = true;
							let r = null;
							let file_doc = null;
							try {
								r = JSON.parse(xhr.responseText);
								if (r.message.doctype === "File") {
									file_doc = r.message;
								}
							} catch (e) {
								r = xhr.responseText;
							}

							file.doc = file_doc;

							if (this.on_success) {
								this.on_success(file_doc, r);
							}
						} else if (xhr.status === 403) {
							file.failed = true;
							let response = JSON.parse(xhr.responseText);
							file.error_message = `Not permitted. ${response._error_message || ""}`;
						} else if (xhr.status === 413) {
							file.failed = true;
							file.error_message = "Size exceeds the maximum allowed file size.";
						} else {
							file.failed = true;
							file.error_message =
								xhr.status === 0
									? "XMLHttpRequest Error"
									: `${xhr.status} : ${xhr.statusText}`;

							let error = null;
							try {
								error = JSON.parse(xhr.responseText);
							} catch (e) {
								// pass
							}
							frappe.request.cleanup({}, error);
						}
					}
				};
				xhr.open("POST", "/api/method/upload_file", true);
				xhr.setRequestHeader("Accept", "application/json");
				xhr.setRequestHeader("X-Frappe-CSRF-Token", frappe.csrf_token);

				let form_data = new FormData();
				if (file.file_obj) {
					form_data.append("file", file.file_obj, file.name);
				}
				form_data.append("is_private", +file.private);
				form_data.append("folder", this.folder);

				if (file.file_url) {
					form_data.append("file_url", file.file_url);
				}

				if (file.file_name) {
					form_data.append("file_name", file.file_name);
				}

				if (file.library_file_name) {
					form_data.append("library_file_name", file.library_file_name);
				}

				if (this.doctype && this.docname) {
					form_data.append("doctype", this.doctype);
					form_data.append("docname", this.docname);
				}

				if (this.fieldname) {
					form_data.append("fieldname", this.fieldname);
				}

				if (this.method) {
					form_data.append("method", this.method);
				}

				if (file.optimize) {
					form_data.append("optimize", true);
				}

				if (this.attach_doc_image) {
					form_data.append("max_width", 200);
					form_data.append("max_height", 200);
				}

				xhr.send(form_data);
        Vue.set(item, "airticket", "/files/"+airticket.name);
			});
    }
  },

  computed: {
    formTitle () {
      return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
    },
  },

  created() {
    this.$nextTick(() => {
      evntBus.$on('send_detailing_detail', (data) => {
        this.data = data
        this.AirTicket = data.common_features
        this.AirTicket.forEach(ele => {
          ele.page_row_id = this.makeid(20)
        });
      });
    });
  },

  watch:{
    AirTicketdialog (val) {
      val || this.AirTicketclose()
    },
  }
};

</script>
