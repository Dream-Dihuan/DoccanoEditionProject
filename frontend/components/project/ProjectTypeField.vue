<template>
  <v-item-group v-model="selected" mandatory @change="$emit('input', allProjectTypes[selected])">
    <v-row no-gutters>
      <v-col v-for="(item, i) in allProjectTypes" :key="i" cols="12" sm="6" md="4">
        <v-item v-slot="{ active, toggle }">
          <v-card 
            class="project-type-card mb-4" 
            :class="{ 'active': active }"
            outlined
            @click="toggle"
          >
            <v-img
              :src="require(`~/assets/images/tasks/${images[i]}`)"
              height="150"
              contain
            />
            <v-card-title class="project-type-title">
              <v-icon v-if="active" color="primary" class="me-2">
                {{ mdiCheckBold }}
              </v-icon>
              {{ translateTypeName(item, $t('overview.projectTypes')) }}
            </v-card-title>
          </v-card>
        </v-item>
      </v-col>
    </v-row>
  </v-item-group>
</template>

<script lang="ts">
import { mdiCheckBold } from '@mdi/js'
import Vue from 'vue'
import {
  allProjectTypes,
  DocumentClassification,
  ProjectType
} from '~/domain/models/project/project'

export default Vue.extend({
  props: {
    value: {
      type: String,
      default: DocumentClassification,
      required: true
    }
  },

  data() {
    return {
      mdiCheckBold,
      allProjectTypes,
      selected: 0
    }
  },

  computed: {
    images() {
      return [
        'text_classification.png',
        'sequence_labeling.png',
        'seq2seq.png',
        'intent_detection.png',
        'image_classification.png',
        'image_captioning.jpg',
        'object_detection.jpg',
        'segmentation.jpg',
        'speech_to_text.png'
      ]
    }
  },

  mounted() {
    // 修复TypeScript类型错误，通过类型断言确保类型兼容
    this.selected = allProjectTypes.indexOf(this.value as ProjectType)
  },

  methods: {
    translateTypeName(type: ProjectType, types: any): string {
      const index = allProjectTypes.indexOf(type)
      return types[index]
    }
  }
})
</script>

<style scoped>
.project-type-card {
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
}

.project-type-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
  border-color: #1976D2;
}

.project-type-card.active {
  border-color: #1976D2;
  box-shadow: 0 5px 15px rgba(25, 118, 210, 0.3);
}

.project-type-title {
  font-size: 1rem;
  font-weight: 500;
  padding: 10px 16px;
  display: flex;
  align-items: center;
}

.theme--dark .project-type-card {
  border-color: #424242;
  background-color: #1E1E1E;
}

.theme--dark .project-type-card:hover {
  border-color: #64B5F6;
}

.theme--dark .project-type-card.active {
  border-color: #64B5F6;
}
</style>