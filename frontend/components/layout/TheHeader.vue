<template>
  <v-app-bar app clipped-left class="header-app-bar" elevate-on-scroll>
    <slot name="leftDrawerIcon" />
    
    <nuxt-link v-if="!isAuthenticated" to="/" class="header-logo-link">
      <img src="~/assets/icon.png" height="42" class="header-logo" />
    </nuxt-link>
    
    <v-toolbar-title v-if="!isAuthenticated" class="header-title ml-2 d-none d-sm-flex">
      成都大学标注平台
    </v-toolbar-title>
    
    <v-btn
      v-if="isAuthenticated && isIndividualProject"
      text
      class="project-name-btn d-none d-sm-flex"
    >
      <v-icon small class="mr-2">
        {{ mdiHexagonMultiple }}
      </v-icon>
      <span class="project-name-text"> {{ currentProject.name }}</span>
    </v-btn>
    
    <div class="flex-grow-1" />
    
    <div class="header-actions">
      <the-color-mode-switcher class="header-action-item" />
      <locale-menu class="header-action-item" />
      
      <v-btn
        v-if="isAuthenticated"
        text
        class="header-nav-btn"
        @click="$router.push(localePath('/projects'))"
      >
        {{ $t('header.projects') }}
      </v-btn>
      
      <!-- <v-menu v-if="!isAuthenticated" open-on-hover offset-y>
        <template #activator="{ on }">
          <v-btn text class="header-nav-btn" v-on="on">
            {{ $t('home.demoDropDown') }}
            <v-icon small class="ml-1">{{ mdiMenuDown }}</v-icon>
          </v-btn>
        </template>
        <v-list class="demo-menu-list">
          <v-list-item
            v-for="(item, index) in items"
            :key="index"
            @click="$router.push('/demo/' + item.link)"
            class="demo-menu-item"
          >
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu> -->
      
      <v-btn 
        v-if="!isAuthenticated" 
        outlined 
        class="login-btn"
        @click="$router.push(localePath('/auth'))"
      >
        {{ $t('user.login') }}
      </v-btn>
      
      <v-menu v-if="isAuthenticated" offset-y z-index="200" left nudge-bottom="10">
        <template #activator="{ on }">
          <v-btn icon class="user-menu-btn" v-on="on">
            <v-avatar size="36" color="primary lighten-1" class="white--text">
              {{ getUsername ? getUsername.charAt(0).toUpperCase() : 'U' }}
            </v-avatar>
          </v-btn>
        </template>
        <v-card class="user-menu-card">
          <v-list>
            <v-list-item class="user-info-item">
              <v-list-item-avatar>
                <v-avatar size="40" color="primary lighten-1" class="white--text">
                  {{ getUsername ? getUsername.charAt(0).toUpperCase() : 'U' }}
                </v-avatar>
              </v-list-item-avatar>
              <v-list-item-content>
                <v-list-item-title class="user-name">{{ getUsername }}</v-list-item-title>
                <!-- <v-list-item-subtitle class="user-email">user@example.com</v-list-item-subtitle> -->
              </v-list-item-content>
            </v-list-item>
            
            <v-divider></v-divider>
            
            <v-list-item class="rtl-switch-item">
              <v-list-item-content>
                <v-switch 
                  :input-value="isRTL" 
                  :label="direction" 
                  class="ms-1" 
                  @change="toggleRTL" 
                  color="primary"
                />
              </v-list-item-content>
            </v-list-item>
            
            <v-divider></v-divider>
            
            <v-list-item @click="signout" class="signout-item">
              <v-list-item-icon class="signout-icon">
                <v-icon>{{ mdiLogout }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title class="signout-text">
                  {{ $t('user.signOut') }}
                </v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card>
      </v-menu>
    </div>
  </v-app-bar>
</template>

<script>
import { mdiLogout, mdiDotsVertical, mdiMenuDown, mdiHexagonMultiple } from '@mdi/js'
import { mapGetters, mapActions } from 'vuex'
import TheColorModeSwitcher from './TheColorModeSwitcher'
import LocaleMenu from './LocaleMenu'

export default {
  components: {
    TheColorModeSwitcher,
    LocaleMenu
  },

  data() {
    return {
      items: [
        { title: this.$t('home.demoNER'), link: 'named-entity-recognition' },
        { title: this.$t('home.demoSent'), link: 'sentiment-analysis' },
        { title: this.$t('home.demoTranslation'), link: 'translation' },
        {
          title: this.$t('home.demoIntenDetectSlotFil'),
          link: 'intent-detection-and-slot-filling'
        },
        { title: this.$t('home.demoTextToSQL'), link: 'text-to-sql' },
        { title: this.$t('home.demoImageClas'), link: 'image-classification' },
        { title: this.$t('home.demoImageCapt'), link: 'image-caption' },
        { title: this.$t('home.demoObjDetect'), link: 'object-detection' },
        { title: this.$t('home.demoPolygSegm'), link: 'segmentation' },
        { title: this.$t('home.demoSTT'), link: 'speech-to-text' }
      ],
      mdiLogout,
      mdiDotsVertical,
      mdiMenuDown,
      mdiHexagonMultiple
    }
  },

  computed: {
    ...mapGetters('auth', ['isAuthenticated', 'getUsername']),
    ...mapGetters('projects', ['currentProject']),
    ...mapGetters('config', ['isRTL']),

    isIndividualProject() {
      return this.$route.name && this.$route.name.startsWith('projects-id')
    },

    direction() {
      return this.isRTL ? this.$t('header.rtl') : this.$t('header.ltr')
    }
  },

  methods: {
    ...mapActions('auth', ['logout']),
    ...mapActions('config', ['toggleRTL']),
    signout() {
      this.logout()
      this.$router.push(this.localePath('/'))
    }
  }
}
</script>

<style scoped>
.header-app-bar {
  padding: 0 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.theme--dark .header-app-bar {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.header-logo-link {
  line-height: 0;
  text-decoration: none;
}

.header-title {
  font-weight: 600;
  font-size: 1.5rem;
  letter-spacing: 0.5px;
}

.project-name-btn {
  text-transform: none;
  background-color: rgba(0, 0, 0, 0.04);
  border-radius: 20px;
  padding: 0 16px;
  margin-right: 16px;
}

.theme--dark .project-name-btn {
  background-color: rgba(255, 255, 255, 0.08);
}

.project-name-text {
  font-weight: 500;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-action-item {
  margin: 0 4px;
}

.header-nav-btn {
  text-transform: none;
  font-weight: 500;
  letter-spacing: 0.5px;
  margin: 0 4px;
  border-radius: 4px;
  min-width: 40px;
}

.header-nav-btn:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.theme--dark .header-nav-btn:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

.login-btn {
  border-radius: 20px;
  font-weight: 600;
  letter-spacing: 0.5px;
  margin-left: 8px;
  text-transform: none;
  border: 2px solid currentColor;
}

.user-menu-btn {
  margin-left: 8px;
}

.user-menu-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  margin-top: 8px;
}

.theme--dark .user-menu-card {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}

.user-info-item {
  min-height: 64px;
}

.user-name {
  font-weight: 600;
  font-size: 1rem;
}

.user-email {
  font-size: 0.85rem;
}

.rtl-switch-item {
  min-height: 56px;
}

.signout-item {
  min-height: 48px;
}

.signout-text {
  color: #f44336;
  font-weight: 500;
}

.demo-menu-list {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  padding: 4px 0;
}

.theme--dark .demo-menu-list {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.demo-menu-item {
  min-height: 40px;
}

.demo-menu-item:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.theme--dark .demo-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.08);
}

@media (max-width: 960px) {
  .header-app-bar {
    padding: 0 12px;
  }
  
  .header-title {
    font-size: 1.3rem;
  }
  
  .project-name-btn {
    margin-right: 8px;
    padding: 0 12px;
  }
  
  .header-actions {
    gap: 4px;
  }
}

@media (max-width: 600px) {
  .header-app-bar {
    padding: 0 8px;
  }
  
  .header-title {
    display: none;
  }
  
  .project-name-btn {
    max-width: 120px;
  }
  
  .project-name-text {
    max-width: 90px;
  }
}
</style>