<template>
  <div class="settings-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('settings.settings') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('settings.description') }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <base-card class="elevation-8">
            <template #content>
              <v-tabs v-model="tab">
                <v-tabs-slider color="primary" />
                <v-tab href="#tab-project" class="text-capitalize"> {{ $t('settings.project') }} </v-tab>
                <!-- <v-tab href="#tab-auto-labeling" class="text-capitalize"> {{ $t('settings.autoLabeling') }} </v-tab> -->
              </v-tabs>
              <v-divider />

              <v-tabs-items v-model="tab">
                <v-tab-item value="tab-project">
                  <form-update />
                </v-tab-item>
                <v-tab-item value="tab-auto-labeling">
                  <config-list />
                </v-tab-item>
              </v-tabs-items>
            </template>
          </base-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import FormUpdate from '@/components/project/FormUpdate.vue'
import ConfigList from '@/components/configAutoLabeling/ConfigList.vue'

export default Vue.extend({
  components: {
    BaseCard,
    ConfigList,
    FormUpdate
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      tab: null
    }
  }
})
</script>

<style scoped>
.settings-page {
  width: 100%;
  height: 100%;
}
</style>