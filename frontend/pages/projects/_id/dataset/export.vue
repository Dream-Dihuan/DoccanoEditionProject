<template>
  <v-container fluid class="pt-6">
    <v-row justify="center">
      <v-col cols="12" md="8" lg="6">
        <v-card class="elevation-8" :class="{ 'dark-mode-card': $vuetify.theme.dark }">
          <v-toolbar color="primary" dark flat class="rounded-t-lg">
            <v-toolbar-title>
              {{ $t('dataset.exportDataTitle') }}
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text class="mt-5">
            <v-overlay :value="isProcessing">
              <v-progress-circular indeterminate size="64" />
            </v-overlay>
            <v-form ref="form" v-model="valid">
              <v-select
                v-model="selectedFormat"
                :items="formats"
                hide-details="auto"
                item-text="name"
                :label="$t('generic.type')"
                outlined
                :rules="fileFormatRules($t('rules.fileFormatRules'))"
              />
              <v-sheet
                v-if="selectedFormat"
                :dark="!$vuetify.theme.dark"
                :light="$vuetify.theme.dark"
                class="mt-2 pa-5"
              >
                <pre>{{ example }}</pre>
              </v-sheet>
              <v-checkbox 
                v-model="exportApproved" 
                :label="$t('dataset.exportApprovedOnly')" 
                hide-details 
                class="mt-4"
              />
            </v-form>
          </v-card-text>
          
          <v-card-actions class="px-6 pb-6">
            <v-spacer></v-spacer>
            <v-btn 
              class="text-capitalize primary" 
              :disabled="!valid" 
              depressed
              @click="downloadRequest"
            >
              {{ $t('generic.export') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { fileFormatRules } from '@/rules/index'
import { Format } from '~/domain/models/download/format'

export default Vue.extend({
  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      exportApproved: false,
      file: null,
      fileFormatRules,
      formats: [] as Format[],
      isProcessing: false,
      polling: null,
      selectedFormat: null as any,
      taskId: '',
      valid: false
    }
  },

  computed: {
    projectId() {
      return this.$route.params.id
    },

    example(): string {
      const item = this.formats.find((item: Format) => item.name === this.selectedFormat)
      return item!.example.trim()
    }
  },

  async created() {
    this.formats = await this.$repositories.downloadFormat.list(this.projectId)
  },

  beforeDestroy() {
    // @ts-ignore
    clearInterval(this.polling)
  },

  methods: {
    reset() {
      ;(this.$refs.form as HTMLFormElement).reset()
      this.taskId = ''
      this.exportApproved = false
      this.selectedFormat = null
      this.isProcessing = false
    },

    async downloadRequest() {
      this.isProcessing = true
      this.taskId = await this.$repositories.download.prepare(
        this.projectId,
        this.selectedFormat,
        this.exportApproved
      )
      this.pollData()
    },

    pollData() {
      // @ts-ignore
      this.polling = setInterval(async () => {
        if (this.taskId) {
          const res = await this.$repositories.taskStatus.get(this.taskId)
          if (res.ready) {
            this.$repositories.download.download(this.projectId, this.taskId)
            this.reset()
          }
        }
      }, 1000)
    }
  }
})
</script>
