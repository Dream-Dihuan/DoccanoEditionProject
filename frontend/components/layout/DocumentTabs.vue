<template>
  <div class="document-tabs">
    <h4 style="text-align: center; margin-bottom: 30px;">跨文档快捷切换栏</h4>
    <div class="document-tabs__container">
      <div 
        v-for="(tab, index) in tabs" 
        :key="tab.id"
        :class="['document-tab', { 'document-tab--active': isActive(tab) }]"
        @click="switchToTab(tab)"
      >
        <span class="document-tab__title">{{ truncateText(tab.title, 20) }}</span>
        <v-btn 
          icon 
          x-small 
          class="document-tab__close"
          @click.stop="closeTab(tab, index)"
        >
          <v-icon small>{{ mdiClose }}</v-icon>
        </v-btn>
      </div>
      
      <div 
        class="document-tab document-tab--add"
        @click="goToDataset"
      >
        <div>
          <span class="document-tab__title" style="font-style: italic;">添加文档</span>
          <v-icon small>{{ mdiPlus }}</v-icon>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script>
import { mdiClose, mdiPlus } from '@mdi/js'

export default {
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
      tabs: [],
      mdiClose,
      mdiPlus
    }
  },
  
  watch: {
    currentDocumentId: {
      handler(newId) {
        if (newId) {
          this.addDocumentTab(newId)
        }
      },
      immediate: true
    }
  },
  
  mounted() {
    this.loadTabsFromStorage()
    // 监听自定义事件，用于从其他组件添加标签页
    window.addEventListener('open-document-tab', this.onOpenDocumentTab)
  },
  
  beforeDestroy() {
    // 清理事件监听器
    window.removeEventListener('open-document-tab', this.onOpenDocumentTab)
  },
  
  methods: {
    truncateText(text, maxLength) {
      if (!text) return ''
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
    },
    
    isActive(tab) {
      return String(tab.documentId) === String(this.currentDocumentId)
    },
    
    async addDocumentTab(documentId) {
      // 检查标签是否已存在
      const existingTab = this.tabs.find(tab => String(tab.documentId) === String(documentId))
      
      if (existingTab) {
        // 如果标签已存在，激活它
        this.switchToTab(existingTab)
        return
      }
      
      try {
        // 获取文档信息
        const response = await this.$services.example.fetchOne(
          this.projectId,
          documentId
        )
        
        if (response && response.items && response.items.length > 0) {
          const doc = response.items[0]
          const newTab = {
            id: `tab_${Date.now()}`,
            title: this.getDocumentTitle(doc),
            documentId
          }
          
          this.tabs.push(newTab)
          this.saveTabsToStorage()
        }
      } catch (error) {
        console.error('Failed to fetch document info:', error)
        // 即使获取文档信息失败，也创建一个标签
        const newTab = {
          id: `tab_${Date.now()}`,
          title: `Document ${documentId}`,
          documentId
        }
        
        this.tabs.push(newTab)
        this.saveTabsToStorage()
      }
    },
    
    getDocumentTitle(doc) {
      // 优先使用文件名，如果不存在则使用文档内容
      if (doc.filename) {
        return doc.filename.length > 30 ? doc.filename.substring(0, 30) + '...' : doc.filename
      } else if (doc.text) {
        // 使用文档的前30个字符作为标题
        return doc.text.length > 30 ? doc.text.substring(0, 30) + '...' : doc.text
      }
      return `Document ${doc.id}`
    },
    
    switchToTab(tab) {
      // alert("switchToTab")
      // 触发事件通知父组件切换文档
      this.$emit('switch-document', tab)
      // console.log("迪幻tab= "+ tab);
      // 跳转到文档页面
      const query = { ...this.$route.query, page: String(tab.documentId) }
      this.$router.push({ query })
    },
    
    closeTab(tab, index) {
      this.tabs.splice(index, 1)
      
      // 如果关闭的是当前活动标签且还有其他标签
      if (this.isActive(tab) && this.tabs.length > 0) {
        // 切换到第一个标签
        this.switchToTab(this.tabs[0])
      } else if (this.tabs.length === 0) {
        // 如果没有标签了，跳转到数据集页面
        this.goToDataset()
      }
      
      this.saveTabsToStorage()
    },
    
    goToDataset() {
      this.$router.push(this.localePath(`/projects/${this.projectId}/dataset`))
    },
    
    saveTabsToStorage() {
      try {
        const key = `documentTabs_project_${this.projectId}`
        localStorage.setItem(key, JSON.stringify(this.tabs))
      } catch (e) {
        console.error('Failed to save tabs to localStorage:', e)
      }
    },
    
    loadTabsFromStorage() {
      try {
        const key = `documentTabs_project_${this.projectId}`
        const data = localStorage.getItem(key)
        
        if (data) {
          this.tabs = JSON.parse(data)
        }
      } catch (e) {
        console.error('Failed to load tabs from localStorage:', e)
        this.tabs = []
      }
    },
    
    // 处理自定义事件，从其他组件添加标签页
    onOpenDocumentTab(event) {
      const { id, text, filename } = event.detail
      // 检查标签是否已存在
      const existingTab = this.tabs.find(tab => String(tab.documentId) === String(id))
      
      if (existingTab) {
        // 如果标签已存在，激活它
        this.switchToTab(existingTab)
        return
      }
      
      // 创建新标签，优先使用文件名
      const title = filename || (text ? (text.length > 30 ? text.substring(0, 30) + '...' : text) : `Document ${id}`)
      const newTab = {
        id: `tab_${Date.now()}`,
        title,
        documentId: id
      }
      
      this.tabs.push(newTab)
      this.saveTabsToStorage()
    }
  }
}
</script>

<style scoped>
.document-tabs {
  padding: 16px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.theme--dark .document-tabs {
  border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.document-tabs__container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 0 16px;
}

.document-tab {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  background-color: rgba(0, 0, 0, 0.04);
}

.theme--dark .document-tab {
  background-color: rgba(255, 255, 255, 0.04);
}

.document-tab:hover {
  background-color: rgba(0, 0, 0, 0.08);
}

.theme--dark .document-tab:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.document-tab--active {
  background-color: rgba(25, 118, 210, 0.1);
  color: #1976D2;
}

.theme--dark .document-tab--active {
  background-color: rgba(25, 118, 210, 0.15);
  color: #1976D2;
}

.document-tab__title {
  flex: 1;
  font-size: 0.875rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.document-tab__close {
  margin-left: 8px;
}

.document-tab--add {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
  background-color: transparent;
  border: 1px dashed rgba(0, 0, 0, 0.2);
}

.theme--dark .document-tab--add {
  border: 1px dashed rgba(255, 255, 255, 0.2);
}

.document-tab--add:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.theme--dark .document-tab--add:hover {
  background-color: rgba(255, 255, 255, 0.04);
}
</style>