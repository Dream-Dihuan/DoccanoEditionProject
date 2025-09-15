<template>
  <div class="project-list">
    <v-data-table
      :value="value"
      :headers="headers"
      :items="items"
      :options.sync="options"
      :server-items-length="total"
      :search="search"
      :loading="isLoading"
      :loading-text="$t('generic.loading')"
      :no-data-text="$t('vuetify.noDataAvailable')"
      :footer-props="{
        showFirstLastPage: true,
        'items-per-page-options': [10, 25, 50, 100],
        'items-per-page-text': $t('vuetify.itemsPerPageText'),
        'page-text': $t('dataset.pageText')
      }"
      item-key="id"
      show-select
      class="project-data-table elevation-0"
      @input="$emit('input', $event)"
    >
      <template #top>
        <div class="d-flex align-center mb-4">
          <v-text-field
            v-model="search"
            :prepend-inner-icon="mdiMagnify"
            :label="$t('generic.search')"
            single-line
            hide-details
            filled
            rounded
            dense
            clearable
            class="search-field"
          />
        </div>
      </template>
      
      <template #[`item.name`]="{ item }">
        <nuxt-link :to="localePath(`/projects/${item.id}/dataset?limit=10&offset=0`)" class="project-link">
          <div class="d-flex align-center">
            <v-avatar size="40" class="mr-3" color="primary lighten-1">
              <span class="white--text text-h6">{{ item.name.charAt(0).toUpperCase() }}</span>
            </v-avatar>
            <div>
              <div class="font-weight-medium text--primary">{{ item.name }}</div>
              <div class="caption text--secondary text-truncate" style="max-width: 300px">
                {{ item.description || $t('projects.noDescription') }}
              </div>
            </div>
          </div>
        </nuxt-link>
      </template>
      
      <template #[`item.projectType`]="{ item }">
        <v-chip small outlined label class="project-type-chip">
          {{ getProjectTypeName(item.projectType) }}
        </v-chip>
      </template>
      
      <template #[`item.createdAt`]="{ item }">
        <span class="text--secondary">{{ formatDate(item.createdAt) }}</span>
      </template>
      
      <template #[`item.tags`]="{ item }">
        <div class="tags-container">
          <v-chip 
            v-for="tag in item.tags.slice(0, 3)" 
            :key="tag.id" 
            small 
            outlined 
            class="tag-chip mr-1 mb-1"
          >
            {{ tag.text }}
          </v-chip>
          <v-chip 
            v-if="item.tags.length > 3" 
            small 
            outlined 
            class="tag-chip mr-1 mb-1"
          >
            +{{ item.tags.length - 3 }}
          </v-chip>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { mdiMagnify } from '@mdi/js'
import { dateFormat } from '@vuejs-community/vue-filter-date-format'
import { dateParse } from '@vuejs-community/vue-filter-date-parse'
import type { PropType } from 'vue'
import Vue from 'vue'
import { DataOptions } from 'vuetify/types'
import { Project, allProjectTypes, ProjectType } from '~/domain/models/project/project'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<Project[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<Project[]>,
      default: () => [],
      required: true
    },
    total: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      search: this.$route.query.q,
      options: {} as DataOptions,
      mdiMagnify,
      dateFormat,
      dateParse
    }
  },

  computed: {
    headers(): { text: any; value: string; sortable?: boolean }[] {
      return [
        { text: this.$t('generic.name'), value: 'name' },
        { text: this.$t('generic.description'), value: 'description', sortable: false },
        // { text: this.$t('generic.type'), value: 'projectType' },
        { text: this.$t('projects.created'), value: 'createdAt' },
        { text: this.$t('projects.author'), value: 'author' },
        { text: this.$t('projects.tags'), value: 'tags', sortable: false }
      ]
    }
  },

  watch: {
    options: {
      handler() {
        this.updateQuery({
          query: {
            limit: this.options.itemsPerPage.toString(),
            offset: ((this.options.page - 1) * this.options.itemsPerPage).toString(),
            q: this.search
          }
        })
      },
      deep: true
    },
    search() {
      this.updateQuery({
        query: {
          limit: this.options.itemsPerPage.toString(),
          offset: '0',
          q: this.search
        }
      })
      this.options.page = 1
    }
  },

  methods: {
    updateQuery(payload: any) {
      const { sortBy, sortDesc } = this.options
      if (sortBy.length === 1 && sortDesc.length === 1) {
        payload.query.sortBy = sortBy[0]
        payload.query.sortDesc = sortDesc[0]
      } else {
        payload.query.sortBy = 'createdAt'
        payload.query.sortDesc = true
      }
      this.$emit('update:query', payload)
    },
    
    getProjectTypeName(type: string): string {
      const index = allProjectTypes.indexOf(type as ProjectType)
      if (index >= 0) {
        const projectTypes = this.$t('overview.projectTypes') as unknown as string[]
        return projectTypes[index]
      }
      return type
    },
    
    formatDate(dateString: string): string {
      try {
        return dateFormat(dateParse(dateString, 'YYYY-MM-DDTHH:mm:ss'), 'YYYY/MM/DD HH:mm')
      } catch {
        return dateString
      }
    }
  }
})
</script>

<style scoped>
.project-list {
  background: transparent;
}

.project-data-table {
  background: var(--card-bg) !important;
}

.search-field {
  max-width: 400px;
}

.project-link {
  text-decoration: none;
  color: inherit;
  display: block;
  padding: 8px 0;
  transition: background-color 0.2s ease;
  border-radius: 4px;
}

.project-link:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.theme--dark .project-link:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.project-type-chip {
  background-color: var(--primary-light) !important;
  opacity: 0.9;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  max-width: 250px;
}

.tag-chip {
  background-color: var(--toolbar-bg) !important;
}

/* Table header styles */
.project-data-table ::v-deep .v-data-table-header th {
  color: var(--text-primary) !important;
  font-weight: 600 !important;
}

.project-data-table ::v-deep .v-data-table-header th.sortable:hover {
  background-color: rgba(0, 0, 0, 0.02) !important;
}

.theme--dark .project-data-table ::v-deep .v-data-table-header th.sortable:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
}

/* Row styles */
.project-data-table ::v-deep tbody tr {
  transition: background-color 0.2s ease;
}

.project-data-table ::v-deep tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.02) !important;
}

.theme--dark .project-data-table ::v-deep tbody tr:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
}

/* Pagination styles */
.project-data-table ::v-deep .v-data-footer {
  border-top: 1px solid var(--card-border) !important;
}

/* Fix for project type text color */
.project-type-chip ::v-deep .v-chip__content {
  color: white;
}

.theme--light .project-type-chip ::v-deep .v-chip__content {
  color: black;
}
</style>