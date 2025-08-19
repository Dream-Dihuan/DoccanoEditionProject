<template>
  <v-text-field
    v-bind="$attrs"
    :value="value"
    :rules="projectNameRules"
    :label="$t('overview.projectName')"
    required
    filled
    rounded
    @input="$emit('input', $event)"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import { validateMinLength, validateNameMaxLength } from '~/domain/models/project/project'

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
      projectNameRules: [
        (text: string) => validateMinLength(text) || this.$t('rules.projectName.required'),
        (text: string) => validateNameMaxLength(text) || this.$t('rules.projectName.maxLength')
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