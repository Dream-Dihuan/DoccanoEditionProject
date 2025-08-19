<template>
  <div class="members-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('members.members') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('members.actions') }}
              </p>
            </div>
            
            <div class="mt-4 mt-sm-0">
              <v-btn 
                class="text-capitalize font-weight-medium" 
                color="primary" 
                rounded
                @click.stop="dialogCreate = true"
              >
                {{ $t('generic.add') }}
              </v-btn>
              <v-btn
                class="text-capitalize font-weight-medium ms-2"
                :disabled="!canDelete"
                outlined
                rounded
                @click.stop="dialogDelete = true"
              >
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
              <member-list 
                v-model="selected" 
                :items="items" 
                :is-loading="isLoading" 
                @edit="editItem" 
              />
            </template>
          </base-card>
        </v-col>
      </v-row>
      
      <v-dialog v-model="dialogCreate" max-width="500">
        <v-card elevation="8">
          <v-toolbar flat dark color="primary">
            <v-toolbar-title>{{ $t('members.addMember') }}</v-toolbar-title>
          </v-toolbar>
          <form-create
            v-model="editedItem"
            :error-message="errorMessage"
            @cancel="close"
            @save="save"
          />
        </v-card>
      </v-dialog>
      
      <v-dialog v-model="dialogDelete" max-width="500">
        <v-card elevation="8">
          <v-toolbar flat dark color="primary">
            <v-toolbar-title>{{ $t('members.removeMember') }}</v-toolbar-title>
          </v-toolbar>
          <form-delete :selected="selected" @cancel="dialogDelete = false" @remove="remove" />
        </v-card>
      </v-dialog>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import FormDelete from '@/components/member/FormDelete.vue'
import MemberList from '@/components/member/MemberList.vue'
import FormCreate from '~/components/member/FormCreate.vue'
import { MemberItem } from '~/domain/models/member/member'
import BaseCard from '@/components/utils/BaseCard.vue'

export default Vue.extend({
  components: {
    MemberList,
    FormCreate,
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
      dialogCreate: false,
      dialogDelete: false,
      editedIndex: -1,
      editedItem: {
        user: -1,
        role: -1,
        username: '',
        rolename: 'annotator'
      } as MemberItem,
      defaultItem: {
        user: -1,
        role: -1,
        username: '',
        rolename: 'annotator'
      } as MemberItem,
      items: [] as MemberItem[],
      selected: [] as MemberItem[],
      isLoading: false,
      errorMessage: ''
    }
  },

  async fetch() {
    this.isLoading = true
    try {
      this.items = await this.$repositories.member.list(this.projectId)
    } catch (e) {
      this.$router.push(`/projects/${this.projectId}`)
    } finally {
      this.isLoading = false
    }
  },

  computed: {
    canDelete(): boolean {
      return this.selected.length > 0
    },
    projectId(): string {
      return this.$route.params.id
    }
  },

  methods: {
    async create() {
      try {
        await this.$repositories.member.create(this.projectId, this.editedItem)
        this.close()
        this.$fetch()
      } catch (e: any) {
        this.errorMessage = e.response.data.detail
      }
    },

    async update() {
      try {
        await this.$repositories.member.update(this.projectId, this.editedItem)
        this.close()
        this.$fetch()
      } catch (e: any) {
        this.errorMessage = e.response.data.detail
      }
    },

    save() {
      if (this.editedIndex > -1) {
        this.update()
      } else {
        this.create()
      }
    },

    close() {
      this.dialogCreate = false
      this.errorMessage = ''
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },

    async remove() {
      await this.$repositories.member.bulkDelete(this.projectId, this.selected)
      this.$fetch()
      this.dialogDelete = false
      this.selected = []
    },

    editItem(item: MemberItem) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogCreate = true
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}

.members-page {
  width: 100%;
  height: 100%;
}
</style>