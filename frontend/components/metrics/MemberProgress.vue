<template>
  <v-card class="member-progress elevation-8">
    <v-card-title>{{ $t('statistics.memberProgress') }}</v-card-title>
    <v-divider />
    <v-card-text>
      <div v-for="(item, index) in stats.progress" :key="index" class="mb-2">
        <span class="font-weight-medium">{{ item.user }}</span>
        <span class="font-weight-medium float-right">{{ item.done }} / {{ stats.total }}</span>
        <v-progress-linear :value="rate(item.done, stats.total)" class="mt-2" />
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { Progress } from '~/domain/models/metrics/metrics'

export default Vue.extend({
  data() {
    return {
      stats: {} as Progress
    }
  },

  async created() {
    // @ts-ignore
    this.stats = await this.$repositories.metrics.fetchMemberProgress(this.$route.params.id)
  },

  methods: {
    rate(done: number, total: number) {
      return (done / total) * 100
    }
  }
})
</script>

<style scoped>
.member-progress {
  border-radius: 12px !important;
}

.theme--dark .member-progress {
  background-color: var(--card-bg) !important;
  border: 2px solid var(--card-border);
}

.member-progress ::v-deep .v-card__title {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
}
</style>