<template>
  <div class="comments-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('comments.comments') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('comments.management') || 'Manage project comments' }}
              </p>
            </div>
            
            <div class="mt-4 mt-sm-0">
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
              <div class="comments-list-wrapper">
                <comment-list
                  v-model="selected"
                  :items="item.items"
                  :is-loading="isLoading"
                  :total="item.count"
                  @update:query="updateQuery"
                  @click:labeling="movePage"
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
import { mapGetters } from 'vuex'
import Vue from 'vue'
import { mdiDelete } from '@mdi/js'
import CommentList from '@/components/comment/CommentList.vue'
import FormDelete from '~/components/comment/FormDelete.vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { CommentItem } from '~/domain/models/comment/comment'
import { Page } from '~/domain/models/page'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'

export default Vue.extend({
  components: {
    CommentList,
    FormDelete,
    BaseCard
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject', 'isProjectAdmin'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      dialogDelete: false,
      item: {} as Page<CommentItem>,
      selected: [] as CommentItem[],
      isLoading: false,
      mdiDelete
    }
  },

  async fetch() {
    this.isLoading = true
    this.item = await this.$repositories.comment.listAll(this.projectId, this.$route.query)
    this.isLoading = false
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
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
      await this.$repositories.comment.deleteBulk(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },
    updateQuery(query: object) {
      this.$router.push(query)
    },
    movePage(query: object) {
      const link = getLinkToAnnotationPage(this.projectId, this.project.projectType)
      this.updateQuery({
        path: this.localePath(link),
        query
      })
    }
  }
})
</script>

<style scoped>
.comments-page {
  background-color: var(--background);
  min-height: 100%;
  width: 100%;
  padding: 0;
}

.theme--dark .comments-page {
  background-color: var(--background);
}

.comments-list-wrapper {
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