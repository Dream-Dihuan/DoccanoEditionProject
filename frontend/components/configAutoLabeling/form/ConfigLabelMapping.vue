<template>
  <v-stepper-content step="4">
    <v-card>
      <v-card-text class="pa-0">
        <h4 class="text-h6">{{ $t('autoLabeling.configureLabelMappings') }}</h4>
        <p class="font-weight-regular body-1">
          {{ $t('autoLabeling.configureLabelMappingsDescription') }}
        </p>
        <h4 class="text-h6">{{ $t('autoLabeling.response') }}</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(response, null, 4) }}</pre>
        </v-sheet>
        <label-mapping v-model="mapping" />
        <v-alert v-for="(error, index) in errorMessages" :key="index" prominent type="error">
          <v-row align="center">
            <v-col class="grow">
              {{ error }}
            </v-col>
          </v-row>
        </v-alert>
        <h4 class="text-h6">{{ $t('autoLabeling.result') }}</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(result, null, 4) }}</pre>
        </v-sheet>
      </v-card-text>
      <v-card-actions class="pa-0">
        <v-spacer />
        <v-btn text class="text-capitalize" @click="$emit('prev')"> {{ $t('generic.prev') }} </v-btn>
        <v-btn v-show="!isPassed" color="primary" class="text-capitalize" @click="$emit('onTest')">
          {{ $t('generic.test') }}
        </v-btn>
        <v-btn v-show="isPassed" color="success" class="text-capitalize" @click="$emit('next')">
          {{ $t('autoLabeling.finish') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'
import LabelMapping from './LabelMapping.vue'

export default Vue.extend({
  components: {
    LabelMapping
  },

  props: {
    value: {
      type: Array,
      default: () => [],
      required: true
    },
    errorMessages: {
      type: Array,
      default: () => [],
      required: true
    },
    isPassed: {
      type: Boolean,
      default: false,
      required: true
    },
    response: {
      type: [String, Object, Array],
      default: () => [],
      required: true
    },
    result: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  computed: {
    mapping: {
      get() {
        // @ts-ignore
        return this.value
      },
      set(newVal) {
        // @ts-ignore
        this.$emit('input', newVal)
      }
    }
  }
})
</script>
