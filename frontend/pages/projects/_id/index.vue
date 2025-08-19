<template>
  <v-card class="project-home-card" flat elevation="8">
    <v-toolbar flat class="project-home-toolbar">
      <v-toolbar-title class="text-h5 font-weight-bold">
        {{ $t('projectHome.welcome') }}
      </v-toolbar-title>
    </v-toolbar>
    
    <v-divider></v-divider>
    
    <v-card-text class="project-home-content">
      <v-stepper v-model="e6" vertical non-linear class="elevation-0">
        <div v-for="(item, index) in items" :key="index">
          <v-stepper-step :complete="e6 > index + 1" :step="index + 1" editable class="stepper-step">
            {{ item.title }}
          </v-stepper-step>
          <v-stepper-content :step="index + 1" class="stepper-content">
            <!-- 隐藏卡片 -->
            <!-- <v-card v-if="e6 === index + 1" class="mb-12" width="560" height="315">
              <youtube ref="youtube" :video-id="item.videoId" />
            </v-card> -->
            <div class="d-flex flex-wrap">
              <v-btn color="primary" class="mt-5 mr-2 text-capitalize" @click="next">
                {{ $t('generic.continue') }}
              </v-btn>
              <v-btn class="mt-5 text-capitalize" text @click="prev">
                {{ $t('generic.cancel') }}
              </v-btn>
            </div>
          </v-stepper-content>
        </div>
      </v-stepper>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  layout: 'project',

  middleware: ['check-auth', 'auth', 'setCurrentProject'],

  validate({ params }) {
    return /^\d+$/.test(params.id)
  },

  data() {
    return {
      e6: 1,
      items: [
        { title: this.$t('projectHome.importData'), videoId: 'dA4ID1DSxCE' },
        { title: this.$t('projectHome.createLabels'), videoId: '1bSML270quU' },
        { title: this.$t('projectHome.addMembers'), videoId: 'NI09dcBz-qA' },
        {
          title: this.$t('projectHome.defineGuideline'),
          videoId: 'AvvX3Xs32nA'
        },
        {
          title: this.$t('projectHome.annotateDataset'),
          videoId: 'F3XoSdyiMhA'
        },
        {
          title: this.$t('projectHome.viewStatistics'),
          videoId: 'kfRpa0mNQMY'
        },
        { title: this.$t('projectHome.exportDataset'), videoId: 'Pfy_QcHEeQ4' }
      ]
    }
  },

  methods: {
    next() {
      this.e6 = Math.max(1, (this.e6 + 1) % (this.items.length + 1))
    },
    prev() {
      this.e6 = Math.max(1, this.e6 - 1)
    }
  }
}
</script>

<style scoped>
.project-home-card {
  border-radius: 12px;
  background: var(--card-bg);
  border: 2px solid var(--card-border);
  overflow: hidden;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  width: calc(100% - 40px);
  max-width: 100%;
  margin: 20px;
}

.project-home-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.theme--dark .project-home-card {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
  border: 2px solid var(--card-border);
}

.theme--dark .project-home-card:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
}

.project-home-toolbar {
  padding: 16px 24px;
  background: linear-gradient(120deg, #1976D2, #42A5F5) !important;
  color: white !important;
}

.project-home-content {
  padding: 24px;
}

.v-toolbar__title {
  color: white;
}

.stepper-step ::v-deep .v-stepper__label {
  font-weight: 500;
}

.stepper-content ::v-deep .v-stepper__content {
  padding: 16px 24px 24px;
}

/* Responsive adjustments */
@media (max-width: 960px) {
  .project-home-content {
    padding: 20px;
  }
  
  .project-home-toolbar {
    padding: 14px 20px;
  }
  
  .stepper-content ::v-deep .v-stepper__content {
    padding: 16px 20px 20px;
  }
  
  .project-home-card {
    width: calc(100% - 30px);
    margin: 15px;
  }
}

@media (max-width: 600px) {
  .project-home-content {
    padding: 16px;
  }
  
  .project-home-toolbar {
    padding: 12px 16px;
  }
  
  .v-toolbar__title {
    font-size: 1.25rem;
  }
  
  .stepper-content ::v-deep .v-stepper__content {
    padding: 16px;
  }
  
  .project-home-card {
    width: calc(100% - 20px);
    margin: 10px;
  }
}
</style>