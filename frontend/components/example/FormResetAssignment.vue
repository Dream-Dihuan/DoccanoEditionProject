<template>
  <confirm-form
    :title="$t('examples.resetTitle')"
    :message="$t('examples.resetMessage')"
    @ok="$emit('reset')"
    @cancel="$emit('cancel')"
  />
</template>

<script lang="ts">
import Vue from 'vue'
import ConfirmForm from '@/components/utils/ConfirmForm.vue'

export default Vue.extend({
  components: {
    ConfirmForm
  }
})
</script>