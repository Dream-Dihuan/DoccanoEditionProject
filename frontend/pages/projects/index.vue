<template>
  <div class="projects-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('header.projects') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('projects.management') }}
              </p>
            </div>
            
            <div v-if="isStaff" class="mt-4 mt-sm-0">
              <v-btn 
                class="text-capitalize font-weight-medium mr-2" 
                color="primary" 
                depressed
                rounded
                @click.stop="$router.push('projects/create')"
              >
                <v-icon left small>{{ mdiPlus }}</v-icon>
                {{ $t('generic.create') }}
              </v-btn>
              <v-btn 
                class="text-capitalize font-weight-medium mr-2" 
                color="primary" 
                outlined
                rounded
                :disabled="!canClone" 
                @click.stop="clone"
              >
                <v-icon left small>{{ mdiContentCopy }}</v-icon>
                {{ $t('generic.clone') }}
              </v-btn>
              <v-btn
                class="text-capitalize font-weight-medium"
                color="error"
                outlined
                rounded
                :disabled="!canDelete"
                @click.stop="dialogDelete = true"
              >
                <v-icon left small>{{ mdiDelete }}</v-icon>
                {{ $t('generic.delete') }}
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <base-card class="elevation-8">
            <template #content>
              <div class="project-list-wrapper">
                <project-list
                  v-model="selected"
                  :items="projects.items"
                  :is-loading="isLoading"
                  :total="projects.count"
                  @update:query="updateQuery"
                />
              </div>
            </template>
          </base-card>
        </v-col>
      </v-row>

      <v-dialog v-model="dialogDelete" max-width="600px">
        <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
      </v-dialog>
    </v-container>
  </div>
</template>

<script lang="ts">
import _ from 'lodash'
import Vue from 'vue'
import { mapGetters } from 'vuex'
import { mdiPlus, mdiContentCopy, mdiDelete } from '@mdi/js'
import ProjectList from '@/components/project/ProjectList.vue'
import FormDelete from '~/components/project/FormDelete.vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { Page } from '~/domain/models/page'
import { Project } from '~/domain/models/project/project'
import { SearchQueryData } from '~/services/application/project/projectApplicationService'

export default Vue.extend({
  components: {
    FormDelete,
    ProjectList,
    BaseCard
  },
  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      dialogDelete: false,
      projects: {} as Page<Project>,
      selected: [] as Project[],
      isLoading: false,
      mdiPlus,
      mdiContentCopy,
      mdiDelete
    }
  },

  async fetch() {
    this.isLoading = true
    this.projects = await this.$services.project.list(
      this.$route.query as unknown as SearchQueryData
    )
    this.isLoading = false
  },

  computed: {
    ...mapGetters('auth', ['isStaff']),
    canDelete(): boolean {
      return this.selected.length > 0
    },

    canClone(): boolean {
      return this.selected.length === 1
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  methods: {
    async remove() {
      await this.$services.project.bulkDelete(this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    async clone() {
      const project = await this.$services.project.clone(this.selected[0])
      this.selected = []
      this.$router.push(`/projects/${project.id}/settings`)
    },

    updateQuery(query: object) {
      this.$router.push(query)
    }
  }
})
</script>

<style scoped>
.projects-page {
  background-color: var(--background);
  min-height: 100%;
  width: 100%;
  padding: 0;
}

.theme--dark .projects-page {
  background-color: var(--background);
}

.project-list-wrapper {
  background: transparent;
}

/* Responsive adjustments */
@media (max-width: 600px) {
  .v-btn {
    margin-bottom: 8px;
  }
  
  .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
  }
  
  .v-container {
    padding: 16px !important;
  }
}

/* Add smooth transitions */
.v-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.v-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
}

.theme--dark .v-card:hover {
  box-shadow: 0 6px 12px rgba(255,255,255,0.15) !important;
}
</style>