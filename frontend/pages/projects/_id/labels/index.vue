<template>
  <div class="labels-page">
    <v-container fluid class="py-8 px-4 px-sm-6">
      <v-row class="mb-6">
        <v-col cols="12">
          <div class="d-flex align-center justify-space-between flex-wrap">
            <div>
              <h1 class="text-h4 font-weight-bold primary--text mb-2">
                {{ $t('labels.labels') }}
              </h1>
              <p class="text--secondary mb-0">
                {{ $t('labels.manageLabels') }}
              </p>
            </div>
            
            <div class="mt-4 mt-sm-0">
              <action-menu
                :add-only="canOnlyAdd"
                @create="$router.push('labels/add?type=' + labelType)"
                @upload="$router.push('labels/import?type=' + labelType)"
                @download="download"
              />
              <v-btn
                v-if="!canOnlyAdd"
                :disabled="!canDelete"
                class="text-capitalize font-weight-medium ms-2"
                color="primary"
                rounded
                outlined
                @click.stop="dialogDelete = true"
              >
                <v-icon left small>{{ mdiDelete }}</v-icon>
                {{ $t('generic.delete') }}
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-tabs v-if="hasMultiType" v-model="tab" class="mb-6">
        <template v-if="isIntentDetectionAndSlotFilling">
          <v-tab class="text-capitalize">{{ $t('labels.category') }}</v-tab>
          <v-tab class="text-capitalize">{{ $t('labels.span') }}</v-tab>
        </template>
        <template v-else>
          <v-tab class="text-capitalize">{{ $t('labels.span') }}</v-tab>
          <v-tab class="text-capitalize">{{ $t('labels.relation') }}</v-tab>
        </template>
      </v-tabs>

      <v-row>
        <v-col cols="12">
          <base-card class="elevation-8">
            <template #content>
              <label-list
                v-model="selected"
                :items="items"
                :is-loading="isLoading"
                :disable-edit="canOnlyAdd"
                :favorite-labels="favoriteLabels"
                :label-type="labelType"
                @edit="editItem"
                @toggle-favorite="toggleFavorite"
              />
            </template>
          </base-card>
        </v-col>
      </v-row>
      
      <v-dialog v-model="dialogDelete" max-width="500">
        <v-card elevation="8">
          <v-toolbar flat dark color="primary">
            <v-toolbar-title>{{ $t('labels.deleteLabelsTitle') }}</v-toolbar-title>
          </v-toolbar>
          <v-card-text class="pt-5">
            <p>{{ $t('labels.deleteLabelsMessage', { number: selected.length }) }}</p>
            <v-list v-if="selected.length > 0">
              <v-list-item v-for="(selItem, i) in selected.slice(0, 10)" :key="i">
                <v-list-item-content>
                  <v-list-item-title>{{ selItem.text }}</v-list-item-title>
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
    </v-container>
  </div>
</template>

<script lang="ts">
import { mapGetters } from 'vuex'
import Vue from 'vue'
import { mdiDelete } from '@mdi/js'
import ActionMenu from '@/components/label/ActionMenu.vue'
import LabelList from '@/components/label/LabelList.vue'
import BaseCard from '@/components/utils/BaseCard.vue'
import { LabelDTO } from '~/services/application/label/labelData'
import { MemberItem } from '~/domain/models/member/member'

export default Vue.extend({
  components: {
    ActionMenu,
    LabelList,
    BaseCard
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, app, store }) {
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project']
      if (!project.canDefineLabel) {
        return false
      }
      return app.$repositories.member.fetchMyRole(params.id).then((member: MemberItem) => {
        if (member.isProjectAdmin) {
          return true
        }
        return project.allowMemberToCreateLabelType
      })
    }
    return false
  },

  data() {
    return {
      dialogDelete: false,
      items: [] as LabelDTO[],
      selected: [] as LabelDTO[],
      isLoading: false,
      tab: 0,
      member: {} as MemberItem,
      mdiDelete,
      favoriteLabels: [] as number[]
    }
  },

  computed: {
    ...mapGetters('projects', ['project']),

    canOnlyAdd(): boolean {
      if (this.member.isProjectAdmin) {
        return false
      }
      const project = this.$store.getters['projects/project']
      return project.allowMemberToCreateLabelType
    },

    canDelete(): boolean {
      return this.selected.length > 0
    },

    projectId(): string {
      return this.$route.params.id
    },

    hasMultiType(): boolean {
      const project = this.$store.getters['projects/project']
      if ('projectType' in project) {
        return this.isIntentDetectionAndSlotFilling || !!project.useRelation
      } else {
        return false
      }
    },

    isIntentDetectionAndSlotFilling(): boolean {
      const project = this.$store.getters['projects/project']
      return project.projectType === 'IntentDetectionAndSlotFilling'
    },

    labelType(): string {
      const project = this.$store.getters['projects/project']
      if (this.hasMultiType) {
        if (this.isIntentDetectionAndSlotFilling) {
          return ['category', 'span'][this.tab!]
        } else {
          return ['span', 'relation'][this.tab!]
        }
      } else if (project.canDefineCategory) {
        return 'category'
      } else {
        return 'span'
      }
    },

    service(): any {
      const project = this.$store.getters['projects/project']
      if (!('projectType' in project)) {
        return
      }
      if (this.hasMultiType) {
        if (this.isIntentDetectionAndSlotFilling) {
          return [this.$services.categoryType, this.$services.spanType][this.tab!]
        } else {
          return [this.$services.spanType, this.$services.relationType][this.tab!]
        }
      } else if (project.canDefineCategory) {
        return this.$services.categoryType
      } else {
        return this.$services.spanType
      }
    }
  },

  watch: {
    tab() {
      this.list()
      // 当标签类型切换时，重新加载该类型的置顶标签
      this.loadFavoriteLabels()
    },
    
    // 监听labelType变化，确保在计算属性更新后重新加载置顶标签
    labelType: {
      handler() {
        this.$nextTick(() => {
          this.loadFavoriteLabels()
        })
      },
      immediate: true
    }
  },

  async created() {
    this.member = await this.$repositories.member.fetchMyRole(this.projectId)
    await this.list()
    this.loadFavoriteLabels()
  },

  methods: {
    async list() {
      this.isLoading = true
      this.items = await this.service.list(this.projectId)
      this.isLoading = false
    },

    async remove() {
      await this.service.bulkDelete(this.projectId, this.selected)
      this.list()
      this.dialogDelete = false
      this.selected = []
    },

    async download() {
      await this.service.export(this.projectId)
    },

    editItem(item: LabelDTO) {
      this.$router.push(`labels/${item.id}/edit?type=${this.labelType}`)
    },

    toggleFavorite(item: LabelDTO) {
      const index = this.favoriteLabels.indexOf(item.id)
      if (index > -1) {
        // 取消置顶
        this.favoriteLabels.splice(index, 1)
      } else {
        // 置顶标签
        this.favoriteLabels.push(item.id)
      }
      this.saveFavoriteLabels()
    },

    loadFavoriteLabels() {
      try {
        const saved = localStorage.getItem(`favoriteLabels_${this.projectId}_${this.labelType}`)
        if (saved) {
          this.favoriteLabels = JSON.parse(saved)
        } else {
          // 如果没有保存的数据，则初始化为空数组
          this.favoriteLabels = []
        }
      } catch (e) {
        console.warn('Failed to load favorite labels from localStorage', e)
        this.favoriteLabels = []
      }
    },

    saveFavoriteLabels() {
      try {
        localStorage.setItem(
          `favoriteLabels_${this.projectId}_${this.labelType}`, 
          JSON.stringify(this.favoriteLabels)
        )
      } catch (e) {
        console.warn('Failed to save favorite labels to localStorage', e)
      }
    }
  }
})
</script>

<style scoped>
::v-deep .v-dialog {
  width: 800px;
}
</style>