<template>
  <div class="document-tabs">
    <div class="document-tabs__header">
      <div class="document-tabs__nav">
        <v-tabs
          v-model="activeTab"
          vertical
          class="document-tabs__tabs"
          active-class="document-tabs__tab--active"
        >
          <v-tab
            v-for="tab in tabs"
            :key="tab.id"
            :href="`#${tab.id}`"
            class="document-tabs__tab"
            @click="switchDocument(tab)"
          >
            <span class="document-tabs__title">{{ truncateText(tab.title, 15) }}</span>
            <v-btn
              icon
              x-small
              class="document-tabs__close"
              @click.stop="closeTab(tab)"
            >
              <v-icon>{{ mdiClose }}</v-icon>
            </v-btn>
          </v-tab>
          
          <v-tab class="document-tabs__add" @click="goToDataset">
            <v-icon>{{ mdiPlus }}</v-icon>
          </v-tab>
        </v-tabs>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { mdiClose, mdiPlus } from '@mdi/js'
import Vue from 'vue'

interface DocumentTab {
  id: string
  title: string
  documentId: string | number | null
}

export default Vue.extend({
  name: 'DocumentTabs',
  
  props: {
    projectId: {
      type: [String, Number],
      required: true
    },
    currentDocumentId: {
      type: [String, Number],
      default: null
    }
  },

  data() {
    return {
      tabs: [] as DocumentTab[],
      activeTab: null as string | null,
      mdiClose,
      mdiPlus
    }
  },

  watch: {
    // 监听路由变化，自动添加标签
    '$route': {
      handler() {
        const page = this.$route.query.page
        // if (page && typeof page === 'string') {
        //   this.addDocumentTab(page)
        // } else if (page && Array.isArray(page) && page.length > 0) {
        //   this.addDocumentTab(page[0])
        // }
      },
      immediate: true
    }
  },

  mounted() {
    // 如果没有标签，但当前在标注页面，则添加当前文档标签
    // if (this.tabs.length === 0 && this.currentDocumentId) {
    //   this.addDocumentTab(String(this.currentDocumentId))
    // } else if (!this.activeTab && this.tabs.length > 0) {
    //   // 如果有标签但没有活动标签，则设置第一个为活动标签
    //   this.activeTab = this.tabs[0].id
    //   this.switchDocument(this.tabs[0])
    // }
  },

  methods: {
    truncateText(text: string, maxLength: number): string {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    },

    addDocumentTab(documentId: string | number) {
      // 检查标签是否已存在
      const existingTab = this.tabs.find(tab => String(tab.documentId) === String(documentId))
      if (existingTab) {
        // 如果标签已存在，激活它
        this.activeTab = existingTab.id
        this.switchDocument(existingTab)
        return
      }

      // 创建新标签
      const newTab: DocumentTab = {
        id: `tab_${Date.now()}`,
        title: `Document ${documentId}`,
        documentId
      }
      
      this.tabs.push(newTab)
      this.activeTab = newTab.id
      this.switchDocument(newTab)
    },

    goToDataset() {
      // 跳转到数据集页面
      this.$router.push(this.localePath(`/projects/${this.projectId}/dataset`))
    },

    closeTab(tab: DocumentTab) {
      const tabIndex = this.tabs.findIndex(t => t.id === tab.id)
      if (tabIndex === -1) return

      // 如果关闭的是当前活动标签
      if (this.activeTab === tab.id) {
        // 如果有下一个标签，则切换到下一个
        if (tabIndex + 1 < this.tabs.length) {
          this.activeTab = this.tabs[tabIndex + 1].id
          this.switchDocument(this.tabs[tabIndex + 1])
        } 
        // 如果有上一个标签，则切换到上一个
        else if (tabIndex > 0) {
          this.activeTab = this.tabs[tabIndex - 1].id
          this.switchDocument(this.tabs[tabIndex - 1])
        } 
        // 如果没有其他标签，则跳转到数据集页面
        else {
          this.goToDataset()
        }
      }

      // 从标签数组中移除
      this.tabs.splice(tabIndex, 1)
    },

    switchDocument(tab: DocumentTab) {
      this.activeTab = tab.id
      
      // 触发事件通知父组件切换文档
      this.$emit('switch-document', tab)
      
      // 如果标签有关联的文档ID，则跳转到该文档
      if (tab.documentId) {
        const query: any = this.$services.option.findOption(String(this.projectId))
        query.page = String(tab.documentId)
        this.$router.push({
          query
        })
      }
    },

    updateTabTitle(tabId: string, title: string) {
      const tab = this.tabs.find(t => t.id === tabId)
      if (tab) {
        tab.title = title
      }
    },

    updateTabDocumentId(tabId: string, documentId: string | number) {
      const tab = this.tabs.find(t => t.id === tabId)
      if (tab) {
        tab.documentId = documentId
      }
    }
  }
})
</script>

<style scoped>
.document-tabs {
  padding: 16px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.theme--dark .document-tabs {
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.document-tabs__tabs {
  width: 100%;
}

.document-tabs__tab {
  display: flex !important;
  justify-content: space-between;
  align-items: center;
  min-height: 36px;
  padding: 4px 12px !important;
  margin-bottom: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
  text-transform: none;
}

.document-tabs__tab:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.theme--dark .document-tabs__tab:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.document-tabs__tab--active {
  background-color: rgba(25, 118, 210, 0.1);
  color: #1976D2 !important;
}

.theme--dark .document-tabs__tab--active {
  background-color: rgba(25, 118, 210, 0.15);
}

.document-tabs__title {
  flex: 1;
  text-align: left;
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.document-tabs__close {
  margin-left: 8px !important;
}

.document-tabs__add {
  min-height: 36px !important;
  padding: 4px 12px !important;
}
</style>