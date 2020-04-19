<template>
  <div id="app">

    <transition name="fade">
      <router-view></router-view>
    </transition>

  </div>
</template>

<style>
  /*#app{
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align center
    color: #2c3e50;
    margin-top 60px
  }
  body, html {
    padding: 0;
    margin: 0;
    width: 100%;
    min-height: 100vh;
  }*/

  body {
    margin: 0px;
    padding: 0px;
    /*background: url(assets/bg1.jpg) center !important;
     background-size: cover;*/
    font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, SimSun, sans-serif;
    font-size: 14px;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
  }
  #app {
    position: absolute;
    top: 0px;
    bottom: 0px;
    width: 100%;
  }

  .fade-enter-active, .fade-leave-active {
    transition: opacity .5s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
  }


</style>
