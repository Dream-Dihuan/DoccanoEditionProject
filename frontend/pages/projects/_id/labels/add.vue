<template>
  <v-container fluid class="pt-6">
    <v-row justify="center">
      <v-col cols="12">
        <v-card class="elevation-8" :class="{ 'dark-mode-card': $vuetify.theme.dark }">
          <v-toolbar color="primary" dark flat class="rounded-t-lg">
            <v-toolbar-title>
              {{ $t('labels.createLabelType') }}
            </v-toolbar-title>
          </v-toolbar>
          
          <v-card-text class="mt-5">
            <form-create v-slot="slotProps" v-bind.sync="editedItem" :items="items" :type="labelType" ref="formCreate">
              <div class="d-flex flex-wrap">
                <v-btn 
                  :disabled="!slotProps.valid" 
                  color="primary" 
                  class="text-capitalize font-weight-medium mr-2 mb-2" 
                  rounded
                  @click="save"
                >
                  {{ $t('generic.save') }}
                </v-btn>

                <v-btn
                  :disabled="!slotProps.valid"
                  color="primary"
                  class="text-capitalize font-weight-medium mr-2 mb-2"
                  rounded
                  outlined
                  @click="saveAndAnother"
                >
                  {{ $t('labels.saveAndAddAnother') }}
                </v-btn>
              </div>
            </form-create>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import FormCreate from '~/components/label/FormCreate.vue'
import { Project } from '~/domain/models/project/project'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  components: {
    FormCreate
  },

  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params, query, store }) {
    if (!['category', 'span', 'relation'].includes(query.type as string)) {
      return false
    }
    if (/^\d+$/.test(params.id)) {
      const project = store.getters['projects/project'] as Project
      return project.canDefineLabel
    }
    return false
  },

  data() {
    return {
      editedItem: {
        text: '',
        source: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#73D8FF',
        textColor: '#ffffff'
      } as LabelDTO & { source: string },
      defaultItem: {
        text: '',
        source: '',
        prefixKey: null,
        suffixKey: null,
        backgroundColor: '#73D8FF',
        textColor: '#ffffff'
      } as LabelDTO & { source: string },
      items: [] as LabelDTO[]
    }
  },

  computed: {
    projectId(): string {
      return this.$route.params.id
    },

    labelType(): string {
      return this.$route.query.type as string
    },

    service(): any {
      const type = this.$route.query.type
      if (type === 'category') {
        return this.$services.categoryType
      } else if (type === 'span') {
        return this.$services.spanType
      } else {
        return this.$services.relationType
      }
    }
  },

  async created() {
    this.items = await this.service.list(this.projectId)
  },

  methods: {
    prepareLabelData(suffixKeyValue: string | null = null, textValue: string | null = null) {
      const labelData = { ...this.editedItem }
      // 如果传入了suffixKeyValue参数，则使用该值
      if (suffixKeyValue !== null) {
        labelData.suffixKey = suffixKeyValue
      }
      // 如果传入了textValue参数，则使用该值
      if (textValue !== null) {
        labelData.text = textValue
      } else if (labelData.source) {
        labelData.text = `${labelData.source} - ${labelData.text}`
      }
      // 删除source属性，因为它不是LabelDTO的一部分
      delete (labelData as any).source
      return labelData
    },

    async save() {
      // 检查suffixKey是否为"真假值"
      if (this.editedItem.suffixKey === this.$t('labels.booleanValue')) {
        // 创建"真"标签，保持"内容来源 - 标签名称"格式
        let trueText = this.editedItem.text;
        if (this.editedItem.source) {
          trueText = `${this.editedItem.source} - ${this.editedItem.text}`
        }
        const trueLabelData = this.prepareLabelData('真', `${trueText}(${this.$t('labels.true')})`)
        await this.service.create(this.projectId, trueLabelData)
        
        // 创建"假"标签，保持"内容来源 - 标签名称"格式
        let falseText = this.editedItem.text;
        if (this.editedItem.source) {
          falseText = `${this.editedItem.source} - ${this.editedItem.text}`
        }
        const falseLabelData = this.prepareLabelData('假', `${falseText}(${this.$t('labels.false')})`)
        await this.service.create(this.projectId, falseLabelData)
      } else {
        // 正常创建标签
        const labelData = this.prepareLabelData()
        await this.service.create(this.projectId, labelData)
      }
      
      this.$router.push(`/projects/${this.projectId}/labels`)
    },

    async saveAndAnother() {
      // 检查suffixKey是否为"真假值"
      if (this.editedItem.suffixKey === this.$t('labels.booleanValue')) {
        // 创建"真"标签，保持"内容来源 - 标签名称"格式
        let trueText = this.editedItem.text;
        if (this.editedItem.source) {
          trueText = `${this.editedItem.source} - ${this.editedItem.text}`
        }
        const trueLabelData = this.prepareLabelData('真', `${trueText}(${this.$t('labels.true')})`)
        await this.service.create(this.projectId, trueLabelData)
        
        // 创建"假"标签，保持"内容来源 - 标签名称"格式
        let falseText = this.editedItem.text;
        if (this.editedItem.source) {
          falseText = `${this.editedItem.source} - ${this.editedItem.text}`
        }
        const falseLabelData = this.prepareLabelData('假', `${falseText}(${this.$t('labels.false')})`)
        await this.service.create(this.projectId, falseLabelData)
      } else {
        // 正常创建标签
        const labelData = this.prepareLabelData()
        await this.service.create(this.projectId, labelData)
      }
      
      this.editedItem = Object.assign({}, this.defaultItem)
      this.items = await this.service.list(this.projectId)
    }
  }
})
</script>

<style scoped>
.dark-mode-card {
  background-color: var(--card-bg) !important;
  border: 2px solid var(--card-border) !important;
}
</style>