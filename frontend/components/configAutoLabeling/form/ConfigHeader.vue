<template>
  <v-stepper-header>
    <v-stepper-step :complete="step > 1" step="1"> {{ $t('autoLabeling.selectTemplate') }} </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 2" step="2"> {{ $t('autoLabeling.setParameters') }} </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 3" step="3"> {{ $t('autoLabeling.setTemplate') }} </v-stepper-step>
    <v-divider />
    <v-stepper-step :complete="step > 4" step="4"> {{ $t('autoLabeling.setMappings') }} </v-stepper-step>
  </v-stepper-header>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    step: {
      type: Number,
      default: 1,
      required: true
    }
  }
})
</script>
