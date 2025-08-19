<template>
  <v-container fluid class="pt-6">
    <v-row justify="center">
      <v-col cols="12">
        <v-card class="elevation-8" :class="{ 'dark-mode-card': $vuetify.theme.dark }">
          <v-toolbar color="primary" dark flat class="rounded-t-lg">
            <v-toolbar-title>
              {{ $t('labels.createLabelType') }}
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text class="mt-5">
            <form-create v-slot="slotProps" v-bind.sync="editedItem" :items="items">
              <div class="d-flex flex-wrap">
                <v-btn 
                  :disabled="!slotProps.valid" 
                  color="primary" 
                  class="text-capitalize font-weight-medium mr-2 mb-2" 
                  rounded
                  @click="save"
                >
                  {{ $t('generic.save') }}
                </v-btn>

                <v-btn
                  :disabled="!slotProps.valid"
                  color="primary"
                  class="text-capitalize font-weight-medium mr-2 mb-2"
                  rounded
                  outlined
                  @click="saveAndAnother"
                >
                  {{ $t('labels.saveAndAddAnother') }}
                </v-btn>
              </div>
            </form-create>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/label/FormCreate.vue'
import { Project } from '~/domain/models/project/project'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, query, store }) {
    if (!['category', 'span', 'relation'].includes(query.type as string)) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project'] as Project
      return project.canDefineLabel
    }
    return false
  },

  data() {
    return {
      editedItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#73D8FF',
        textColor: '#ffffff'
      } as LabelDTO,
      defaultItem: {
        text: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#73D8FF',
        textColor: '#ffffff'
      } as LabelDTO,
      items: [] as LabelDTO[]
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    service(): any {
      const type = this.$route.query.type
      if (type === 'category') {
        return this.$services.categoryType
      } else if (type === 'span') {
        return this.$services.spanType
      } else {
        return this.$services.relationType
      }
    }
  },

  async created() {
    this.items = await this.service.list(this.projectId)
  },

  methods: {
    async save() {
      await this.service.create(this.projectId, this.editedItem)
      this.$router.push(`/projects/${this.projectId}/labels`)
    },

    async saveAndAnother() {
      await this.service.create(this.projectId, this.editedItem)
      this.editedItem = Object.assign({}, this.defaultItem)
      this.items = await this.service.list(this.projectId)
    }
  }
})
</script>

<style scoped>
.dark-mode-card {
  background-color: var(--card-bg) !important;
  border: 2px solid var(--card-border) !important;
}
</style>