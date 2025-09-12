<template>
  <v-menu :value="opened" :position-x="x" :position-y="y" absolute offset-y @input="close">
    <v-list dense min-width="150" max-height="400" class="overflow-y-auto">
      <v-list-item>
        <v-autocomplete
          ref="autocomplete"
          v-model="value"
          :items="sortedLabels"
          autofocus
          dense
          deletable-chips
          hide-details
          item-text="text"
          item-value="id"
          label="Select a label"
          small-chips
        />
      </v-list-item>
      <v-list-item v-for="(label, i) in sortedLabels" :key="i" @click="onLabelSelected(label.id)">
        <v-list-item-action v-if="hasAnySuffixKey">
          <v-chip
            v-if="label.suffixKey"
            :color="label.backgroundColor"
            outlined
            small
            v-text="label.suffixKey"
          />
          <span v-else class="mr-8" />
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title style="white-space: normal; word-break: break-word;">{{ label.text }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    opened: {
      type: Boolean,
      default: false,
      required: true
    },
    selectedLabel: {
      type: Object,
      default: null,
      required: false
    },
    x: {
      type: Number,
      default: 0,
      required: true
    },
    y: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      startOffset: 0,
      endOffset: 0,
      entity: null as any,
      fromEntity: null as any,
      toEntity: null as any,
      favoriteLabels: [] as number[],
      labelUsageHistory: [] as number[]
    }
  },

  computed: {
    hasAnySuffixKey(): boolean {
      return this.labels.some((label: any) => label.suffixKey !== null)
    },

    value: {
      get() {
        return this.selectedLabel
      },
      set(labelId: number) {
        this.onLabelSelected(labelId)
      }
    },

    sortedLabels() {
      // 获取标签使用频率和最近使用位置
      const usageCount: {[key: number]: number} = {}
      const lastUsedIndex: {[key: number]: number} = {}
      
      this.labelUsageHistory.forEach((id, index) => {
        usageCount[id] = (usageCount[id] || 0) + 1
        // 记录最后一次使用的位置（索引越小表示越近）
        if (lastUsedIndex[id] === undefined || index < lastUsedIndex[id]) {
          lastUsedIndex[id] = index
        }
      })
      
      // 分别收集三类标签
      const favoriteLabels: any[] = [] // 置顶标签
      const usedLabels: any[] = []     // 使用过的非置顶标签
      const unusedLabels: any[] = []   // 未使用过的标签
      
      // 将标签分类
      this.labels.forEach((label: any) => {
        if (this.favoriteLabels.includes(label.id)) {
          favoriteLabels.push(label)
        } else if (usageCount[label.id] > 0) {
          usedLabels.push(label)
        } else {
          unusedLabels.push(label)
        }
      })
      
      // 对使用过的标签按频率和最近使用时间排序
      usedLabels.sort((a: any, b: any) => {
        const aUsageCount = usageCount[a.id] || 0
        const bUsageCount = usageCount[b.id] || 0
        
        // 使用频率不同，频率高的排在前面
        if (aUsageCount > bUsageCount) return -1
        if (aUsageCount < bUsageCount) return 1
        
        // 使用频率相同，最近使用的排在前面
        const aLastUsed = lastUsedIndex[a.id] !== undefined ? lastUsedIndex[a.id] : Infinity
        const bLastUsed = lastUsedIndex[b.id] !== undefined ? lastUsedIndex[b.id] : Infinity
        return aLastUsed - bLastUsed
      })
      
      // 合并三类标签：置顶标签 + 使用过的标签 + 未使用过的标签
      const result = [...favoriteLabels, ...usedLabels, ...unusedLabels]
      
      return result
    }
  },

  mounted() {
    // 组件挂载时加载置顶标签和使用历史
    this.loadFavoriteLabels()
    this.loadLabelUsageHistory()
    
    // 调试信息
    console.log('Mounted - Favorite labels:', this.favoriteLabels)
    console.log('Mounted - Label usage history:', this.labelUsageHistory)
  },

  methods: {
    close() {
      // Todo: a bit hacky. I want to fix this problem.
      // https://github.com/vuetifyjs/vuetify/issues/10765
      this.$nextTick(() => {
        if (this.$refs.autocomplete) {
          ;(this.$refs.autocomplete as any).selectedItems = []
        }
      })
      this.$emit('close')
    },

    onLabelSelected(labelId: number) {
      // 记录标签使用历史
      this.recordLabelUsage(labelId)
      this.$emit('click:label', labelId)
      this.close()
    },
    
    // 记录标签使用历史
    recordLabelUsage(labelId: number) {
      // 添加到历史记录开头
      this.labelUsageHistory.unshift(labelId)
      
      // 保持最多30条记录
      if (this.labelUsageHistory.length > 30) {
        this.labelUsageHistory = this.labelUsageHistory.slice(0, 30)
      }
      
      // 保存到localStorage
      const projectId = (this.$route as any)?.params?.id
      if (projectId) {
        try {
          let storageKey = ''
          if (this.labels && this.labels.length > 0) {
            const firstLabel: any = this.labels[0]
            if (Object.prototype.hasOwnProperty.call(firstLabel, 'prefixKey') && 
                Object.prototype.hasOwnProperty.call(firstLabel, 'suffixKey')) {
              // 关系标签
              storageKey = `labelUsageHistory_${projectId}_relation`
            } else {
              // 实体标签（默认）
              storageKey = `labelUsageHistory_${projectId}_span`
            }
          }
          
          localStorage.setItem(storageKey, JSON.stringify(this.labelUsageHistory))
        } catch (e) {
          console.warn('Failed to save label usage history to localStorage', e)
        }
      }
    },
    
    // 加载标签使用历史
    loadLabelUsageHistory() {
      const projectId = (this.$route as any)?.params?.id
      if (!projectId) return
      
      try {
        let storageKey = ''
        if (this.labels && this.labels.length > 0) {
          const firstLabel: any = this.labels[0]
          if (Object.prototype.hasOwnProperty.call(firstLabel, 'prefixKey') && 
              Object.prototype.hasOwnProperty.call(firstLabel, 'suffixKey')) {
            // 关系标签
            storageKey = `labelUsageHistory_${projectId}_relation`
          } else {
            // 实体标签（默认）
            storageKey = `labelUsageHistory_${projectId}_span`
          }
        }
        
        const saved = localStorage.getItem(storageKey)
        if (saved) {
          this.labelUsageHistory = JSON.parse(saved)
        }
      } catch (e) {
        console.warn('Failed to load label usage history from localStorage', e)
        this.labelUsageHistory = []
      }
    },
    
    // 加载置顶标签
    loadFavoriteLabels() {
      // 从路由参数中获取项目ID
      const projectId = (this.$route as any)?.params?.id
      if (!projectId) return
      
      try {
        // 根据标签类型确定存储键名
        let storageKey = ''
        if (this.labels && this.labels.length > 0) {
            // 实体标签（默认）
            storageKey = `favoriteLabels_${projectId}_span`
        }
        
        console.log('Loading favorite labels from storage key:', storageKey)
        const saved = localStorage.getItem(storageKey)
        console.log('Favorite labels from localStorage:', saved)
        if (saved) {
          this.favoriteLabels = JSON.parse(saved)
        }
        console.log('Favorite labels loaded:', this.favoriteLabels)
      } catch (e) {
        console.warn('Failed to load favorite labels from localStorage', e)
        this.favoriteLabels = []
      }
    }
  }
})
</script>