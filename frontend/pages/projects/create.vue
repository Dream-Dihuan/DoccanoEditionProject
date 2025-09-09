<template>
  <div class="project-creation-container">
    <v-card class="project-creation-card" elevation="8">
      <v-toolbar flat class="project-creation-toolbar">
        <v-toolbar-title class="text-h5 font-weight-bold">
          {{ $t('overview.createProjectTitle') }}
        </v-toolbar-title>
      </v-toolbar>
      
      <v-card-text class="project-creation-content">
        <v-form ref="form" v-model="valid">
          <v-row>
            <!-- 隐藏项目类型选项 -->
            <v-col cols="12" style="display: none;">
              <div class="section-title">{{ $t('overview.projectType') }}</div>
              <project-type-field v-model="editedItem.projectType" />
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12" md="6">
              <div class="section-title">{{ $t('overview.projectName') }}</div>
              <project-name-field v-model="editedItem.name" outlined autofocus />
            </v-col>
            
            <v-col cols="12" md="6">
              <div class="section-title">{{ $t('generic.description') }}</div>
              <project-description-field v-model="editedItem.description" outlined />
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12">
              <div class="section-title">{{ $t('overview.tags') }}</div>
              <tag-list v-model="editedItem.tags" outlined />
            </v-col>
          </v-row>
          
          <v-row>
            <v-col cols="12">
              <div class="section-title">{{ $t('settings.title') }}</div>
              <v-card outlined class="settings-card" elevation="2">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-checkbox
                        v-if="showExclusiveCategories"
                        v-model="editedItem.exclusiveCategories"
                        :label="$t('overview.allowSingleLabel')"
                        hide-details
                        class="mb-2"
                      />
                      <v-checkbox
                        v-if="_canDefineLabel"
                        v-model="editedItem.allowMemberToCreateLabelType"
                        :label="$t('overview.allowMemberToCreateLabelType')"
                        hide-details
                        class="mb-2"
                      />
                      <random-order-field v-model="editedItem.enableRandomOrder" />
                      <sharing-mode-field v-model="editedItem.enableSharingMode" />
                    </v-col>
                    
                    <template v-if="isSequenceLabelingProject">
                      <v-col cols="12" md="6">
                        <v-checkbox 
                          v-model="editedItem.allowOverlappingSpans" 
                          :label="$t('overview.allowOverlappingSpans')"
                          hide-details
                          class="mb-2"
                        />
                        <v-checkbox 
                          v-model="editedItem.useRelation" 
                          :label="$t('overview.useRelationLabeling')"
                          hide-details
                          class="mb-2"
                        />
                        <v-checkbox v-model="editedItem.enableGraphemeMode" hide-details class="mb-2">
                          <template #label>
                            <div>
                              {{ $t('overview.countGraphemeClusters') }}
                              <v-tooltip bottom>
                                <template #activator="{ on }">
                                  <a
                                    target="_blank"
                                    href="https://unicode.org/reports/tr29/"
                                    class="text-decoration-none"
                                    @click.stop
                                    v-on="on"
                                  >
                                  </a>
                                </template>
                                {{ $t('overview.graphemeClustersDesc') }}
                              </v-tooltip>
                            </div>
                          </template>
                        </v-checkbox>
                      </v-col>
                    </template>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      
      <v-card-actions class="project-creation-actions">
        <v-spacer></v-spacer>
        <v-btn
          :disabled="!valid"
          color="primary"
          x-large
          class="text-capitalize font-weight-medium"
          @click="create"
        >
          {{ $t('generic.create') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import ProjectDescriptionField from '~/components/project/ProjectDescriptionField.vue'
import ProjectNameField from '~/components/project/ProjectNameField.vue'
import ProjectTypeField from '~/components/project/ProjectTypeField.vue'
import RandomOrderField from '~/components/project/RandomOrderField.vue'
import SharingModeField from '~/components/project/SharingModeField.vue'
import TagList from '~/components/project/TagList.vue'
import {
  DocumentClassification,
  ImageClassification,
  SequenceLabeling,
  IntentDetectionAndSlotFilling,
  canDefineLabel
} from '~/domain/models/project/project'

const initializeProject = () => {
  return {
    name: '',
    description: '',
    projectType: IntentDetectionAndSlotFilling, // 将默认项目类型设置为"意图检测和槽位填充"
    enableRandomOrder: false,
    enableSharingMode: false,
    exclusiveCategories: false,
    allowOverlappingSpans: false,
    enableGraphemeMode: false,
    useRelation: false,
    tags: [] as string[],
    guideline: '',
    allowMemberToCreateLabelType: false
  }
}

export default Vue.extend({
  components: {
    ProjectTypeField,
    ProjectNameField,
    ProjectDescriptionField,
    RandomOrderField,
    SharingModeField,
    TagList
  },

  layout: 'projects',

  middleware: ['check-auth', 'auth'],

  data() {
    return {
      valid: false,
      editedItem: initializeProject()
    }
  },

  computed: {
    showExclusiveCategories(): boolean {
      return [DocumentClassification, ImageClassification].includes(this.editedItem.projectType)
    },
    isSequenceLabelingProject(): boolean {
      return this.editedItem.projectType === SequenceLabeling
    },
    _canDefineLabel(): boolean {
      return canDefineLabel(this.editedItem.projectType as any)
    }
  },

  methods: {
    async create() {
      const project = await this.$services.project.create(this.editedItem)
      this.$router.push(`/projects/${project.id}`)
      this.$nextTick(() => {
        this.editedItem = initializeProject()
      })
    }
  }
})
</script>

<style scoped>
.project-creation-container {
  width: 100%;
  margin: 0 auto;
  padding: 20px;
  max-width: 1400px;
}

.project-creation-card {
  border-radius: 12px;
  width: 100%;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.project-creation-toolbar {
  background: linear-gradient(120deg, #1976D2, #42A5F5) !important;
  border-top-left-radius: 12px !important;
  border-top-right-radius: 12px !important;
  color: white !important;
}

.project-creation-content {
  padding: 30px;
}

.project-creation-actions {
  padding: 20px 30px 30px;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #1976D2;
}

.settings-card {
  border-radius: 8px;
  background-color: #f5f9ff;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.theme--dark .settings-card {
  background-color: #2A2A2A;
}

.theme--dark .section-title {
  color: #64B5F6;
}

.project-creation-toolbar ::v-deep .v-toolbar__title {
  color: white;
}

@media (max-width: 960px) {
  .project-creation-container {
    padding: 15px;
  }
  
  .project-creation-content {
    padding: 20px;
  }
  
  .project-creation-actions {
    padding: 15px 20px 20px;
  }
}

@media (max-width: 600px) {
  .project-creation-container {
    padding: 10px;
  }
  
  .project-creation-content {
    padding: 15px;
  }
  
  .project-creation-actions {
    padding: 15px;
    flex-direction: column;
  }
  
  .v-card-actions .v-btn {
    width: 100%;
  }
}

/* 添加悬停效果 */
.project-creation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.1) !important;
}

.theme--dark .project-creation-card:hover {
  box-shadow: 0 6px 12px rgba(255,255,255,0.1) !important;
}

/* 改善表单元素间距 */
.v-input {
  margin-bottom: 16px;
}

.v-input ::v-deep .v-label {
  font-weight: 500;
}

/* 改善复选框样式 */
.v-input--checkbox ::v-deep .v-input__slot {
  margin-bottom: 0 !important;
}

.v-input--checkbox ::v-deep .v-messages {
  min-height: 0;
}
</style>