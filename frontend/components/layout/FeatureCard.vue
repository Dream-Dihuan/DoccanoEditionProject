<template>
  <div></div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    title: {
      type: String,
      default: '',
      required: false
    },
    text: {
      type: String,
      default: '',
      required: false
    },
    imageSrc: {
      type: String,
      default: '',
      required: false
    }
  }
})
</script>

<style scoped>
.feature-card {
  transition: all 0.3s ease-in-out;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.feature-card:hover {
  transform: translateY(-10px);
}
</style>