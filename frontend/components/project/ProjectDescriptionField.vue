<template>
  <v-text-field
    v-bind="$attrs"
    :value="value"
    :rules="descriptionRules"
    :label="$t('generic.description')"
    required
    filled
    rounded
    @input="$emit('input', $event)"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import { validateMinLength } from '~/domain/models/project/project'

export default Vue.extend({
  props: {
    value: {
      type: String,
      default: '',
      required: true
    }
  },
  data() {
    return {
      descriptionRules: [
        (text: string) => validateMinLength(text) || this.$t('rules.description.required')
      ]
    }
  }
})
</script>

<style scoped>
::v-deep .v-input__control {
  min-height: 56px;
}

::v-deep .v-text-field--filled .v-text-field__prefix,
::v-deep .v-text-field--filled .v-text-field__suffix,
::v-deep .v-text-field--filled .v-label {
  padding-top: 18px;
}

::v-deep .v-text-field--filled:not(.v-text-field--single-line) .v-text-field__prefix,
::v-deep .v-text-field--filled:not(.v-text-field--single-line) .v-text-field__suffix,
::v-deep .v-text-field--filled:not(.v-text-field--single-line) input {
  padding-top: 22px;
  padding-bottom: 10px;
}
</style>