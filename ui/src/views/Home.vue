<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <HelloWorld msg="Welcome to Your Vue.js App"/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Home',
  components: {
    HelloWorld
  },
  mounted() {
    var cookies = this.$cookies.get("isLoggedIn");  // return value

    // check the cookie
    if (cookies == null) {
      console.log("USER NOT LOGGED.");
      //this.$router.push('Login')
    }
  }
}
</script>
