<template>
  <v-combobox
    v-bind="$attrs"
    :value="value"
    :items="value"
    :label="$t('overview.tags')"
    multiple
    chips
    deletable-chips
    hide-selected
    filled
    rounded
    @change="$emit('input', $event)"
  />
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'
export default Vue.extend({
  props: {
    value: {
      type: Array as PropType<string[]>,
      default: () => [],
      required: true
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

::v-deep .v-chip {
  margin: 4px 4px 4px 0;
}
</style>