<template>
  <v-container fluid class="pt-6">
    <v-row justify="center">
      <v-col cols="12">
        <v-card class="elevation-8" :class="{ 'dark-mode-card': $vuetify.theme.dark }">
          <v-toolbar color="primary" dark flat class="rounded-t-lg">
            <v-toolbar-title>
              {{ $t('labels.importLabels') }}
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text class="mt-5">
            <form-import :error-message="errorMessage" @clear="clearErrorMessage" @upload="upload" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import FormImport from '~/components/label/FormImport.vue'

export default Vue.extend({
  components: {
    FormImport
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params, query, store }) {
    if (!['category', 'span', 'relation'].includes(query.type as string)) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project']
      return project.canDefineLabel
    }
    return false
  },

  data() {
    return {
      errorMessage: ''
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

  methods: {
    async upload(file: File) {
      try {
        await this.service.upload(this.projectId, file)
        this.$router.push(`/projects/${this.projectId}/labels`)
      } catch (e: any) {
        this.errorMessage = e.message
      }
    },

    clearErrorMessage() {
      this.errorMessage = ''
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