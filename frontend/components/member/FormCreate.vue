<template>
  <div>
    <v-card-text class="pt-5">
      <v-form v-model="valid">
        <v-autocomplete
          v-model="user"
          :items="users"
          :loading="isLoading"
          :search-input.sync="username"
          hide-no-data
          item-text="username"
          :label="$t('members.userSearchAPIs')"
          :placeholder="$t('members.userSearchPrompt')"
          :prepend-icon="mdiAccount"
          :rules="[rules.userRequired]"
          return-object
        />
        <v-select
          v-model="role"
          :items="roles"
          item-text="name"
          item-value="id"
          :label="$t('members.role')"
          :rules="[rules.roleRequired]"
          return-object
          :prepend-icon="mdiCreditCardOutline"
        >
          <template #item="props">
            {{ $translateRole(props.item.name, $t('members.roles')) }}
          </template>
          <template #selection="props">
            {{ $translateRole(props.item.name, $t('members.roles')) }}
          </template>
        </v-select>
        <v-alert v-show="errorMessage" prominent type="error">
          <v-row align="center">
            <v-col class="grow">
              {{ errorMessage }}
            </v-col>
          </v-row>
        </v-alert>
      </v-form>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="$emit('cancel')">
        {{ $t('generic.cancel') }}
      </v-btn>
      <v-btn color="primary" :disabled="!valid" @click="$emit('save')">
        {{ $t('generic.save') }}
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import { mdiAccount, mdiCreditCardOutline } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { MemberItem } from '~/domain/models/member/member'
import { RoleItem } from '~/domain/models/role/role'
import { UserItem } from '~/domain/models/user/user'

export default Vue.extend({
  props: {
    value: {
      type: Object as PropType<MemberItem>,
      required: true
    },
    errorMessage: {
      type: String,
      default: ''
    }
  },

  data() {
    return {
      isLoading: false,
      valid: false,
      users: [] as UserItem[],
      roles: [] as RoleItem[],
      username: '',
      rules: {
        userRequired: (v: UserItem) => (!!v && !!v.username) || 'Required',
        roleRequired: (v: RoleItem) => (!!v && !!v.name) || 'Required'
      },
      mdiAccount,
      mdiCreditCardOutline
    }
  },

  async fetch() {
    this.isLoading = true
    this.users = await this.$repositories.user.list(this.username)
    this.isLoading = false
  },

  computed: {
    user: {
      get(): UserItem {
        return {
          id: this.value.user,
          username: this.value.username,
          isStaff: false,
          isSuperuser: false
        }
      },
      set(val: MemberItem) {
        if (val === undefined) return
        const user = { user: val.id, username: val.username }
        this.$emit('input', { ...this.value, ...user })
      }
    },
    role: {
      get(): RoleItem {
        return {
          id: this.value.role,
          name: this.value.rolename
        }
      },
      set(val: RoleItem) {
        const role = { role: val.id, rolename: val.name }
        this.$emit('input', { ...this.value, ...role })
      }
    }
  },

  watch: {
    username() {
      // Items have already been loaded
      if (this.users.length > 0) return

      // Items have already been requested
      if (this.isLoading) return

      this.$fetch()
    }
  },

  async created() {
    this.roles = await this.$repositories.role.list()
  }
})
</script>