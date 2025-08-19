<template>
  <div class="project-creation-container">
    <v-card class="project-creation-card" elevation="6">
      <v-toolbar flat class="project-creation-toolbar">
        <v-toolbar-title class="text-h5 font-weight-bold">
          {{ $t('overview.createProjectTitle') }}
        </v-toolbar-title>
      </v-toolbar>
      
      <v-card-text class="project-creation-content">
        <v-form v-model="valid" ref="form">
          <v-row>
            <v-col cols="12">
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
              <v-card outlined class="settings-card">
                <v-card-text>
                  <v-row>
                    <v-col cols="12" md="6">
                      <v-checkbox
                        v-if="showExclusiveCategories"
                        v-model="editedItem.exclusiveCategories"
                        :label="$t('overview.allowSingleLabel')"
                        hide-details
                      />
                      <v-checkbox
                        v-if="_canDefineLabel"
                        v-model="editedItem.allowMemberToCreateLabelType"
                        :label="$t('overview.allowMemberToCreateLabelType')"
                        hide-details
                      />
                      <random-order-field v-model="editedItem.enableRandomOrder" />
                      <sharing-mode-field v-model="editedItem.enableSharingMode" />
                    </v-col>
                    
                    <template v-if="isSequenceLabelingProject">
                      <v-col cols="12" md="6">
                        <v-checkbox 
                          v-model="editedItem.allowOverlappingSpans" 
                          :label="$t('projects.overview.allowOverlappingSpans')"
                          hide-details
                        />
                        <v-checkbox 
                          v-model="editedItem.useRelation" 
                          :label="$t('projects.overview.useRelationLabeling')"
                          hide-details
                        />
                        <v-checkbox v-model="editedItem.enableGraphemeMode" hide-details>
                          <template #label>
                            <div>
                              {{ $t('overview.countGraphemeClusters') }}
                              <v-tooltip bottom>
                                <template #activator="{ on }">
                                  <a
                                    target="_blank"
                                    href="https://unicode.org/reports/tr29/"
                                    @click.stop
                                    v-on="on"
                                    class="text-decoration-none"
                                  >
                                    grapheme clusters
                                  </a>
                                </template>
                                {{ $t('overview.graphemeClustersDesc') }}
                              </v-tooltip>
                              as one character
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
          @click="create"
          x-large
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
  canDefineLabel
} from '~/domain/models/project/project'

const initializeProject = () => {
  return {
    name: '',
    description: '',
    projectType: DocumentClassification,
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
}

.project-creation-card {
  border-radius: 12px;
  width: 100%;
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
}

.theme--dark .settings-card {
  background-color: #1E1E1E;
}

.theme--dark .section-title {
  color: #64B5F6;
}

.project-creation-toolbar ::v-deep .v-toolbar__title {
  color: white;
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
  }
}
</style>