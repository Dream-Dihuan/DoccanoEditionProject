<template>
  <v-stepper-content step="3">
    <v-card>
      <v-card-text class="pa-0">
        <h4 class="text-h6">{{ $t('autoLabeling.setMappingTemplate') }}</h4>
        <p class="font-weight-regular body-1">
          {{ $t('autoLabeling.setMappingTemplateDescription') }}
        </p>
        <h4 class="text-h6">{{ $t('autoLabeling.response') }}</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ JSON.stringify(response, null, 4) }}</pre>
        </v-sheet>
        <h4 class="text-h6">{{ $t('autoLabeling.doccanoFormat') }}</h4>
        <v-sheet :dark="!$vuetify.theme.dark" :light="$vuetify.theme.dark" class="mb-5 pa-5">
          <pre>{{ $t('autoLabeling.textClassification') }}</pre>
          <pre>[{ "label": "Cat" }, ...]</pre>
          <br />
          <pre>{{ $t('autoLabeling.sequenceLabeling') }}</pre>
          <pre>[{ "label": "Cat", "start_offset": 0, "end_offset": 5 }, ...]</pre>
          <br />
          <pre>{{ $t('autoLabeling.sequenceToSequence') }}</pre>
          <pre>[{ "text": "Cat" }, ...]</pre>
        </v-sheet>
        <h4 class="text-h6">{{ $t('autoLabeling.mappingTemplate') }}</h4>
        <p class="font-weight-regular body-1">
          {{ $t('autoLabeling.mappingTemplateDescription1') }}
          <a href="https://jinja.palletsprojects.com/en/2.11.x/">Jinja2</a>
          {{ $t('autoLabeling.mappingTemplateDescription2') }}
          <strong>{{ $t('autoLabeling.inputVariable') }}</strong>
          {{ $t('autoLabeling.mappingTemplateDescription3') }}
        </p>
        <v-textarea
          :value="value"
          outlined
          :label="$t('autoLabeling.mappingTemplate')"
          @change="$emit('input', $event)"
        />
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
        <v-btn v-show="isPassed" color="primary" class="text-capitalize" @click="$emit('next')">
          {{ $t('generic.next') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-stepper-content>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    value: {
      type: String,
      default: '',
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
  }
})
</script>
