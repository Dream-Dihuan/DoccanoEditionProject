<template>
  <v-container fluid class="pt-6">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="elevation-8" :class="{ 'dark-mode-card': $vuetify.theme.dark }">
          <v-toolbar color="primary" dark flat class="rounded-t-lg">
            <v-toolbar-title>
              {{ $t('dataset.editText') }}
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text class="mt-5">
            <v-form ref="form" v-model="valid">
              <v-textarea
                v-model="editedItem.text"
                autofocus
                auto-grow
                counter
                outlined
                :rules="[rules.required]"
              />
            </v-form>
          </v-card-text>
          
          <v-card-actions class="px-6 pb-6">
            <v-spacer></v-spacer>
            <v-btn 
              :disabled="!valid" 
              color="primary" 
              class="text-capitalize" 
              depressed
              @click="save"
            >
              {{ $t('generic.save') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { Project } from '~/domain/models/project/project'
import { ExampleDTO } from '~/services/application/example/exampleData'

export default Vue.extend({
  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params, store }) {
    if (/^\d+$/.test(params.id) && /^\d+$/.test(params.example_id)) {
      const project = store.getters['projects/project'] as Project
      return project.isTextProject
    }
    return false
  },

  data() {
    return {
      editedItem: {} as ExampleDTO,
      valid: true,
      rules: {
        required: (v: string) => !!v || 'Required'
      }
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    }
  },

  async created() {
    const exampleId = parseInt(this.$route.params.example_id, 10)
    this.editedItem = await this.$services.example.findById(this.projectId, exampleId)
  },

  methods: {
    async save() {
      await this.$services.example.update(this.projectId, this.editedItem)
      this.$router.push(`/projects/${this.projectId}/dataset`)
    }
  }
})
</script>
