<template>
  <div class="dataset-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row v-if="isProjectAdmin" class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('dataset.dataset') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('dataset.actions') }}
              </p>
            </div>
            
            <div class="mt-4 mt-sm-0">
              <action-menu
                @upload="$router.push('dataset/import')"
                @download="$router.push('dataset/export')"
                @assign="dialogAssignment = true"
                @reset="dialogReset = true"
              />
              <v-btn
                class="text-capitalize font-weight-medium ms-2"
                :disabled="!canDelete"
                color="primary"
                rounded
                @click.stop="dialogDelete = true"
              >
                <v-icon left small>{{ mdiDelete }}</v-icon>
                {{ $t('generic.delete') }}
              </v-btn>
              <v-btn
                :disabled="!item.count"
                class="text-capitalize font-weight-medium ms-2"
                color="error"
                rounded
                @click="dialogDeleteAll = true"
              >
                <v-icon left small>{{ mdiDelete }}</v-icon>
                {{ $t('generic.deleteAll') }}
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12">
          <base-card class="elevation-8">
            <template #content>
              <div class="dataset-list-wrapper">
                <image-list
                  v-if="project.isImageProject"
                  v-model="selected"
                  :items="item.items"
                  :is-admin="user.isProjectAdmin"
                  :is-loading="isLoading"
                  :members="members"
                  :total="item.count"
                  @update:query="updateQuery"
                  @click:labeling="movePage"
                  @assign="assign"
                  @unassign="unassign"
                />
                <audio-list
                  v-else-if="project.isAudioProject"
                  v-model="selected"
                  :items="item.items"
                  :is-admin="user.isProjectAdmin"
                  :is-loading="isLoading"
                  :members="members"
                  :total="item.count"
                  @update:query="updateQuery"
                  @click:labeling="movePage"
                  @assign="assign"
                  @unassign="unassign"
                />
                <document-list
                  v-else
                  v-model="selected"
                  :items="item.items"
                  :is-admin="user.isProjectAdmin"
                  :is-loading="isLoading"
                  :members="members"
                  :total="item.count"
                  @update:query="updateQuery"
                  @click:labeling="movePage"
                  @edit="editItem"
                  @assign="assign"
                  @unassign="unassign"
                />
              </div>
            </template>
          </base-card>
        </v-col>
      </v-row>
      
      <v-dialog v-model="dialogDelete" max-width="500">
        <v-card elevation="8">
          <v-toolbar flat dark color="primary">
            <v-toolbar-title>{{ $t('dataset.deleteDocumentsTitle') }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pt-5">
            <p>{{ $t('dataset.deleteDocumentsMessage', { number: selected.length }) }}</p>
            <v-list v-if="selected.length > 0">
              <v-list-item v-for="(selItem, i) in selected.slice(0, 10)" :key="i">
                <v-list-item-content>
                  <v-list-item-title>{{ selItem[itemKey] }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-if="selected.length > 10">
                <v-list-item-content>
                  <v-list-item-title>... and {{ selected.length - 10 }} more</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="dialogDelete = false">
              {{ $t('generic.cancel') }}
            </v-btn>
            <v-btn color="primary" @click="remove">
              {{ $t('generic.yes') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogDeleteAll" max-width="500">
        <v-card elevation="8">
          <v-toolbar flat dark color="primary">
            <v-toolbar-title>{{ $t('dataset.deleteBulkDocumentsTitle') }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pt-5">
            {{ $t('dataset.deleteBulkDocumentsMessage') }}
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text @click="dialogDeleteAll = false">
              {{ $t('generic.cancel') }}
            </v-btn>
            <v-btn color="primary" @click="removeAll">
              {{ $t('generic.yes') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogAssignment" max-width="500">
        <v-card elevation="8">
          <form-assignment @cancel="dialogAssignment = false" @assigned="assigned" />
        </v-card>
      </v-dialog>
      <v-dialog v-model="dialogReset" max-width="500">
        <v-card elevation="8">
          <form-reset-assignment @cancel="dialogReset = false" @reset="resetAssignment" />
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script lang="ts">
import _ from 'lodash'
import { mapGetters } from 'vuex'
import Vue from 'vue'
import { NuxtAppOptions } from '@nuxt/types'
import { mdiDelete } from '@mdi/js'
import DocumentList from '@/components/example/DocumentList.vue'
import FormAssignment from '~/components/example/FormAssignment.vue'
import FormResetAssignment from '~/components/example/FormResetAssignment.vue'
import ActionMenu from '~/components/example/ActionMenu.vue'
import AudioList from '~/components/example/AudioList.vue'
import ImageList from '~/components/example/ImageList.vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'
import { ExampleDTO, ExampleListDTO } from '~/services/application/example/exampleData'
import { MemberItem } from '~/domain/models/member/member'

export default Vue.extend({
  components: {
    ActionMenu,
    AudioList,
    DocumentList,
    ImageList,
    FormAssignment,
    FormResetAssignment,
    BaseCard
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, query }: NuxtAppOptions) {
    return /^\d+$/.test(params.id) && /^\d+|$/.test(query.limit) && /^\d+|$/.test(query.offset)
  },

  data() {
    return {
      dialogDelete: false,
      dialogDeleteAll: false,
      dialogAssignment: false,
      dialogReset: false,
      item: {} as ExampleListDTO,
      selected: [] as ExampleDTO[],
      members: [] as MemberItem[],
      user: {} as MemberItem,
      isLoading: false,
      isProjectAdmin: false,
      mdiDelete
    }
  },

  async fetch() {
    this.isLoading = true
    this.item = await this.$services.example.list(this.projectId, this.$route.query)
    this.user = await this.$repositories.member.fetchMyRole(this.projectId)
    if (this.user.isProjectAdmin) {
      this.members = await this.$repositories.member.list(this.projectId)
    }
    this.isLoading = false
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    itemKey(): string {
      if (this.project.isImageProject || this.project.isAudioProject) {
        return 'filename'
      } else {
        return 'text'
      }
    }
  },

  watch: {
    '$route.query': _.debounce(function () {
      // @ts-ignore
      this.$fetch()
    }, 1000)
  },

  async created() {
    const member = await this.$repositories.member.fetchMyRole(this.projectId)
    this.isProjectAdmin = member.isProjectAdmin
  },

  methods: {
    async remove() {
      await this.$services.example.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    async removeAll() {
      await this.$services.example.bulkDelete(this.projectId, [])
      this.$fetch()
      this.dialogDeleteAll = false
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
    },

    editItem(item: ExampleDTO) {
      this.$router.push(`dataset/${item.id}/edit`)
    },

    async assign(exampleId: number, userId: number) {
      await this.$repositories.assignment.assign(this.projectId, exampleId, userId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async unassign(assignmentId: string) {
      await this.$repositories.assignment.unassign(this.projectId, assignmentId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async assigned() {
      this.dialogAssignment = false
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    },

    async resetAssignment() {
      this.dialogReset = false
      await this.$repositories.assignment.reset(this.projectId)
      this.item = await this.$services.example.list(this.projectId, this.$route.query)
    }
  }
})
</script>

<style scoped>
.dataset-page {
  background-color: var(--background);
  min-height: 100%;
  width: 100%;
  padding: 0;
}

.theme--dark .dataset-page {
  background-color: var(--background);
}
</style>