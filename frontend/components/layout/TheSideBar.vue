<template>
  <v-list dense class="sidebar-wrapper">
    <div class="annotation-section">
      <v-btn 
        color="primary" 
        class="start-annotation-btn" 
        depressed
        block
        large
        @click="toLabeling"
      >
        <v-icon left size="20">
          {{ mdiPlayCircleOutline }}
        </v-icon>
        {{ $t('home.startAnnotation') }}
      </v-btn>
    </div>

    <!-- DocumentTabs组件 -->
    <document-tabs
      v-if="project.id"
      :project-id="project.id"
      :current-document-id="currentDocumentId"
      @switch-document="onSwitchDocument"
    />

    <v-list-item-group v-model="selected" mandatory class="menu-items-group">
      <template v-for="(item, i) in filteredItems">
        <v-list-item
          :key="i"
          class="menu-item"
          active-class="menu-item--active"
          @click="$router.push(localePath(`/projects/${$route.params.id}/${item.link}`))"
        >
          <v-list-item-icon class="menu-item__icon">
            <v-icon :color="selected === i ? 'primary' : 'grey darken-1'">
              {{ item.icon }}
            </v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="menu-item__title">
              {{ item.text }}
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider v-if="item.text === $t('projectHome.home') || item.text === 'Relations'" :key="'divider-' + i" class="menu-divider"></v-divider>
      </template>
    </v-list-item-group>
  </v-list>
</template>

<script>
import {
  mdiAccount,
  mdiBookOpenOutline,
  mdiChartBar,
  mdiCog,
  mdiCommentAccountOutline,
  mdiDatabase,
  mdiHome,
  mdiLabel,
  mdiPlayCircleOutline
} from '@mdi/js'
import DocumentTabs from './DocumentTabs.vue'
// import { getLinkToAnnotationPage } from '~/presenter/linkToAnnotationPage'

export default {
  components: {
    DocumentTabs
  },

  props: {
    isProjectAdmin: {
      type: Boolean,
      default: false,
      required: true
    },
    project: {
      type: Object,
      default: () => {},
      required: true
    }
  },

  data() {
    return {
      selected: 0,
      mdiPlayCircleOutline
    }
  },

  computed: {
    currentDocumentId() {
      return this.$route.query.page || null
    },
    
    filteredItems() {
      const items = [
        {
          icon: mdiHome,
          text: this.$t('projectHome.home'),
          link: '',
          isVisible: true
        },
        {
          icon: mdiDatabase,
          text: this.$t('dataset.dataset'),
          link: 'dataset',
          isVisible: true
        },
        {
          icon: mdiLabel,
          text: this.$t('labels.labels'),
          link: 'labels',
          isVisible:
            (this.isProjectAdmin || this.project.allowMemberToCreateLabelType) &&
            this.project.canDefineLabel
        },
        {
          icon: mdiLabel,
          text: 'Relations',
          link: 'links',
          isVisible:
            (this.isProjectAdmin || this.project.allowMemberToCreateLabelType) &&
            this.project.canDefineRelation
        },
        {
          icon: mdiAccount,
          text: this.$t('members.members'),
          link: 'members',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiCommentAccountOutline,
          text: this.$t('comments.comments'),
          link: 'comments',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiBookOpenOutline,
          text: this.$t('guideline.guideline'),
          link: 'guideline',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiChartBar,
          text: this.$t('statistics.statistics'),
          link: 'metrics',
          isVisible: this.isProjectAdmin
        },
        {
          icon: mdiCog,
          text: this.$t('settings.title'),
          link: 'settings',
          isVisible: this.isProjectAdmin
        }
      ]
      return items.filter((item) => item.isVisible)
    }
  },

  methods: {
    toLabeling() {
      const query = this.$services.option.findOption(this.$route.params.id)
      const link = getLinkToAnnotationPage(this.$route.params.id, this.project.projectType)
      this.$router.push({
        path: this.localePath(link),
        query
      })
    },
    
    onSwitchDocument(tab) {
      // 处理文档切换事件
      // 实际的路由跳转在DocumentTabs组件中处理
      this.$emit('switch-document', tab)
    }
  }
}
</script>

<style scoped>
.sidebar-wrapper {
  padding: 16px 0;
  background-color: transparent;
}

.annotation-section {
  padding: 0 16px 20px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.theme--dark .annotation-section {
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.start-annotation-btn {
  border-radius: 24px !important;
  text-transform: none;
  font-weight: 600;
  letter-spacing: 0.5px;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  height: 48px !important;
}

.start-annotation-btn:hover {
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.25);
  transform: translateY(-1px);
}

.theme--dark .start-annotation-btn {
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.4);
}

.theme--dark .start-annotation-btn:hover {
  box-shadow: 0 5px 12px rgba(0, 0, 0, 0.5);
}

.menu-items-group {
  padding-top: 12px;
}

.menu-item {
  padding: 12px 24px;
  margin: 0;
  border-left: 3px solid transparent;
  transition: all 0.2s ease-in-out;
}

.menu-item:hover {
  background-color: rgba(0, 0, 0, 0.03);
  border-left: 3px solid #1976D2;
}

.theme--dark .menu-item:hover {
  background-color: rgba(255, 255, 255, 0.05);
}

.menu-item--active {
  background-color: rgba(25, 118, 210, 0.08);
  border-left: 3px solid #1976D2;
}

.theme--dark .menu-item--active {
  background-color: rgba(25, 118, 210, 0.15);
}

.menu-item__icon {
  margin-right: 20px;
}

.menu-item__title {
  font-weight: 500;
  font-size: 0.95rem;
  color: rgba(0, 0, 0, 0.87);
}

.theme--dark .menu-item__title {
  color: rgba(255, 255, 255, 0.87);
}

.menu-divider {
  margin: 8px 0;
  border-color: rgba(0, 0, 0, 0.08);
}

.theme--dark .menu-divider {
  border-color: rgba(255, 255, 255, 0.08);
}
</style>