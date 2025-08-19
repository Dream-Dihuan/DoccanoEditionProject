<template>
  <div class="metrics-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row>
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('statistics.title') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('statistics.description') }}
              </p>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <member-progress class="elevation-8" />
        </v-col>
        <v-col v-if="!!project.canDefineCategory" cols="12">
          <label-distribution
            :title="$t('statistics.categoryDistribution')"
            :distribution="categoryDistribution"
            :label-types="categoryTypes"
            class="elevation-8"
          />
        </v-col>
        <v-col v-if="!!project.canDefineSpan" cols="12">
          <label-distribution
            :title="$t('statistics.spanDistribution')"
            :distribution="spanDistribution"
            :label-types="spanTypes"
            class="elevation-8"
          />
        </v-col>
        <v-col v-if="!!project.canDefineRelation" cols="12">
          <label-distribution
            :title="$t('statistics.relationDistribution')"
            :distribution="relationDistribution"
            :label-types="relationTypes"
            class="elevation-8"
          />
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import LabelDistribution from '~/components/metrics/LabelDistribution'
import MemberProgress from '~/components/metrics/MemberProgress'

export default {
  components: {
    LabelDistribution,
    MemberProgress
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      categoryTypes: [],
      categoryDistribution: {},
      relationTypes: [],
      relationDistribution: {},
      spanTypes: [],
      spanDistribution: {}
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),

    projectId() {
      return this.$route.params.id
    }
  },

  async created() {
    if (this.project.canDefineCategory) {
      this.categoryTypes = await this.$services.categoryType.list(this.projectId)
      this.categoryDistribution = await this.$repositories.metrics.fetchCategoryDistribution(
        this.projectId
      )
    }
    if (this.project.canDefineSpan) {
      this.spanTypes = await this.$services.spanType.list(this.projectId)
      this.spanDistribution = await this.$repositories.metrics.fetchSpanDistribution(this.projectId)
    }
    if (this.project.canDefineRelation) {
      this.relationTypes = await this.$services.relationType.list(this.projectId)
      this.relationDistribution = await this.$repositories.metrics.fetchRelationDistribution(
        this.projectId
      )
    }
  }
}
</script>

<style scoped>
.metrics-page ::v-deep .v-card {
  border-radius: 12px;
}

.metrics-page ::v-deep .v-card__title {
  font-size: 1.25rem !important;
  font-weight: 600 !important;
}

.theme--dark .metrics-page ::v-deep .v-card {
  background-color: var(--card-bg) !important;
  border: 2px solid var(--card-border);
}
</style>