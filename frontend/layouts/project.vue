<template>
  <v-app>
    <the-header>
      <template #leftDrawerIcon>
        <v-app-bar-nav-icon @click="drawerLeft = !drawerLeft" />
      </template>
    </the-header>

    <v-navigation-drawer v-model="drawerLeft" app clipped color="">
      <the-side-bar :is-project-admin="isProjectAdmin" :project="currentProject" />
    </v-navigation-drawer>

    <v-main class="pb-0">
      <v-container fluid class="pa-0 fill-height">
        <v-row no-gutters class="fill-height">
          <v-col class="fill-height">
            <div class="content-wrapper">
              <nuxt />
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import TheHeader from '~/components/layout/TheHeader'
import TheSideBar from '~/components/layout/TheSideBar'

export default {
  components: {
    TheSideBar,
    TheHeader
  },

  data() {
    return {
      drawerLeft: null,
      isProjectAdmin: false
    }
  },

  computed: {
    ...mapGetters('projects', ['currentProject'])
  },

  async created() {
    const member = await this.$repositories.member.fetchMyRole(this.$route.params.id)
    this.isProjectAdmin = member.isProjectAdmin
  }
}
</script>

<style scoped>
.content-wrapper {
  padding: 20px;
  height: 100%;
  width: 100%;
}

@media (max-width: 960px) {
  .content-wrapper {
    padding: 15px;
  }
}

@media (max-width: 600px) {
  .content-wrapper {
    padding: 10px;
  }
}
</style>