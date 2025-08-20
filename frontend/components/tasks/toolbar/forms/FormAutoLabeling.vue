<template>
  <base-card :cancel-text="$t('generic.close')" @cancel="$emit('click:cancel')">
    <template #content>
      <h3>{{ $t('annotation.autoLabeling') }}</h3>
      <p>
        {{ $t('annotation.autoLabelingDescription1') }}
      </p>
      <p>
        {{ $t('annotation.autoLabelingDescription2') }}
      </p>
      <v-switch
        :value="isEnabled"
        :error-messages="errorMessage"
        @change="$emit('input', $event)"
      />
    </template>
  </base-card>
</template>

<script lang="ts">
import Vue from 'vue'
import BaseCard from '@/components/utils/BaseCard.vue'

export default Vue.extend({
  components: {
    BaseCard
  },

  props: {
    isEnabled: {
      type: Boolean,
      default: false,
      required: true
    },
    errorMessage: {
      type: String,
      default: '',
      required: true
    }
  }
})
</script>