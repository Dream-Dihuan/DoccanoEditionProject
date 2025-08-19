<template>
  <v-app>
    <the-header />
    <v-main>
      <div class="projects-layout">
        <nuxt />
      </div>
    </v-main>
  </v-app>
</template>

<script>
import TheHeader from '~/components/layout/TheHeader'

export default {
  components: {
    TheHeader
  }
}
</script>

<style scoped>
.projects-layout {
  background-color: var(--background);
  min-height: calc(100vh - 64px);
  padding: 0;
}

.theme--dark .projects-layout {
  background-color: var(--background);
}

/* Add smooth transitions */
.projects-layout {
  transition: background-color 0.3s ease;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .projects-layout {
    min-height: calc(100vh - 56px);
  }
}
</style>