<template>
  <div class="home">
    <el-container>


      <el-row :gutter="24">
        <el-col :span="1">
          <el-menu default-active="2" class="el-menu-vertical-demo"
                   @open="handleOpen"
                   @close="handleClose"
                   :collapse="isCollapse"
                   @mouseover="isCollapse"
                   background-color="#545c64"
                   text-color="#fff"
                   active-text-color="#ffd04b"
                   style="min-height: 100vh; z-index: 90"
          >
            <img src="../assets/img/logo_svg.svg" width="100%" alt="logo" style="background-color: inherit">
            <el-submenu index="1">
              <template slot="title">
                <i class="el-icon-folder"></i>
                <span slot="title">Folders</span>
              </template>
              <el-menu-item-group>
                <span slot="title">Other folders</span>
                <el-menu-item index="1-1">Bin</el-menu-item>
                <el-menu-item index="1-2">Folder #2</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group title="Settings">
                <el-menu-item index="1-3">Create a new folder</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
            <el-menu-item index="2">
              <i class="el-icon-menu"></i>
              <span slot="title">Inbox</span>
            </el-menu-item>
            <el-menu-item index="3">
              <i class="el-icon-s-promotion"></i>
              <span slot="title">Sent</span>
            </el-menu-item>
            <el-menu-item index="4">
              <i class="el-icon-s-flag"></i>
              <span slot="title">Flagged</span>
            </el-menu-item>
            <el-menu-item index="5">
              <i class="el-icon-document"></i>
              <span slot="title">Drafts</span>
            </el-menu-item>
            <el-menu-item index="6">
              <i class="el-icon-delete"></i>
              <span slot="title">Spam</span>
            </el-menu-item>
            <el-menu-item index="7">
              <i class="el-icon-setting"></i>
              <span slot="title">Settings</span>
            </el-menu-item>



            <el-avatar src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png"
                       class="user-avatar">
            </el-avatar>



          </el-menu>
        </el-col>
        <el-col :span="6" v-loading="loading = false">



          <div id="mail-list" class="flex">
            <div @click="openEmail(index)" class="mail-item" :class="{selected: isSelected(index)}" v-for="(email, index) in emails" :key="index">
              <div class="mail-same-height">
                <div class="mail-item-title-bar flex">
                  <p class="flex center-vertical center-horizontal">{{email.sender.name[0]}}</p>
                </div>
                <div>
                  <p>{{email.sender.name}}</p>
                  <p class="max-lines">{{email.subject}}</p>
                </div>
              </div>
              <div>
                <p>{{email.sent}}</p>
              </div>
            </div>
          </div>




        </el-col>
        <el-col :span="17" class="mail-body-container">

          <div class="tm-wrapper">
            <div class="tm-open-message shadow-lg">
                    <div class="tm-mail-content">

                      <div id="mail-detail">
                        <div id="overlap">
                          <div id="mail-actions" class="flex center-vertical">
                            <div class="flex center-vertical">
                              <p class="flex center-vertical center-horizontal">{{selectedEmail.sender.name[0]}}</p>
                              <div>
                                <p>{{selectedEmail.sender.name}}</p>
                                <p>{{selectedEmail.sender.email}}</p>
                              </div>
                            </div>
                            <div class="flex center-vertical">
                              <button class="btn">
                                <img src="../assets/img/baseline-reply-24px.svg" alt="reply"/>
                                Reply
                              </button>
                              <button class="btn btn-hollow">
                                <img class="img-white" src="../assets/img/baseline-reply_all-24px.svg"/>
                                Forward
                              </button>
                            </div>
                          </div>
                        </div>
                        <div id="mail-content">
                          <div>
                            <p>{{selectedEmail.subject}}</p>
                            <p>{{selectedEmail.sent}}</p>
                          </div>
                          <p>{{selectedEmail.body}}</p>
                        </div>
                      </div>

                    </div>
            </div>

          </div>



        </el-col>
      </el-row>

    </el-container>
  </div>
</template>

<script>

  export default {
    name: 'Home',
    data() {
      return {
        activeIndex2: '1',
        loading: true,
        src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
        isCollapse: true,

        perPage: 5,
        currentPage: 1,
        selectedIndex: -1,

        emails: [
          {
            sender: { name: "Jane Doe", email: "janedoe@gmail.com" },
            subject: "Necessary newspaper",
            body: "Necessary ye contented newspaper zealously breakfast he prevailed. Melancholy middletons yet understood decisively boy law she. Answer him easily are its barton little. Oh no though mother be things simple itself. Dashwood horrible he strictly on as. Home fine in so am good body this hope.",
            sent: '7:11 AM'
          },
          {
            sender: { name: "Jack Doe", email: "jackdoe@gmail.com" },
            subject: "Material expenses",
            body: "Expenses as material breeding insisted building to in. Continual so distrusts pronounce by unwilling listening. Thing do taste on we manor. Him had wound use found hoped. Of distrusts immediate enjoyment curiosity do. Marianne numerous saw thoughts the humoured. ",
            sent: '8:12 AM'
          }
        ]


      }
    },
    mounted() {
      var cookies = this.$cookies.get("isLoggedIn");  // return value

      // check the cookie
      if (cookies == null) {
        console.log("USER NOT LOGGED.");
        //this.$router.push('Login')
      }
    },
    computed: {
      totalPages(){
        return Math.ceil(this.emails.length / this.perPage);
      },
      pagination(){
        return `Page ${this.currentPage} of ${this.totalPages}`;
      },
      hasPrevPage(){
        return this.currentPage - 1 > 0;
      },
      hasNextPage(){
        return this.currentPage < this.totalPages;
      },
      selectedEmail(){
        return this.emails[this.selectedIndex];
      }
    },
    methods: {
      openEmail(index){
        this.selectedIndex = index;
      },
      isSelected(index){
        return this.selectedIndex === index;
      },
      handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    },
    created(){
      this.selectedIndex = 0;
    }
  }
</script>

<style scoped>
  #home {
    overflow-x: hidden;
    font-family: "Poppins", Arial,serif;
  }

  .user-avatar {
    position: absolute;
    left: 19%;
    bottom: 20px;
  }

  #mail-list {
    flex-wrap: wrap;
    margin-top: 16px;
    margin-left: 30px;
    justify-content: space-between;
  }
  #mail-list .mail-item {
    padding: 16px;
    margin-top: 10px;
    border-radius: 10px;
    background: #EEF1F6;
    width: 100%;
    color: black;
  }
  #mail-list .mail-item:hover {
    background: #ddd;
    cursor: pointer;
  }

  .mail-same-height {
    display: inline-block;
    height: auto;
  }

  #mail-list .mail-item .mail-item-title-bar {
    /*justify-content: space-between;*/
  }
  #mail-list .mail-item .mail-item-title-bar p {
    border-radius: 50%;
    width: 36px;
    height: 36px;
    color: black;
    background-color: white;
  }
  #mail-list .mail-item div:nth-child(2) {
    margin-top: 16px;
  }
  #mail-list .mail-item div:nth-child(2) p:nth-child(2) {
    font-size: 14px;
    color: rgba(0, 0, 0, 0.8);
  }
  #mail-list .mail-item div:nth-child(3) p {
    color: rgba(0, 0, 0, 0.54);
    font-size: 12px;
  }




  .mail-body-container {
    height: 100vh;
  }

  .tm-wrapper {
    max-width: 100%;
    height: 100vh;
    margin: 0 0;
    background-color: #EEF1F6;
    max-height: 100%;
    overflow-y: auto;
    background-image: url("https://source.unsplash.com/user/erondu");
    -webkit-background-size: cover;
    -moz-background-size: cover;
    -o-background-size: cover;
    background-size: cover;
  }


  .img-white {
    filter: invert(1);
  }

  .flex {
    display: flex;
  }

  .center-horizontal {
    justify-content: center;
  }

  .center-vertical {
    align-items: center;
  }



  #mail-detail {
    margin-top: 10px;
    width: calc(95%);
    background: white;
    margin-left: 32px;
    border-radius: 10px;
    z-index: 1;
  }
  #mail-detail #overlap {
    height: 150px;
    border-radius: 10px 10px 0px 0px;
    background: #ff4133;
    z-index: 2;
  }
  #mail-detail #overlap #mail-actions {
    justify-content: space-between;
  }
  #mail-detail #overlap #mail-actions > div {
    margin: 24px 16px 0px 16px;
  }
  #mail-detail #overlap #mail-actions > div > p {
    background: white;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    font-size: 20px;
    color: black;
  }
  #mail-detail #overlap #mail-actions > div div {
    margin-left: 16px;
    color: white;
  }
  #mail-detail #overlap #mail-actions > div div p:nth-child(2) {
    font-size: 14px;
    color: rgba(255, 255, 255, 0.54);
  }
  #mail-detail #overlap #mail-actions div:nth-child(2) .btn {
    background: white;
    color: black;
    border: 0px solid transparent;
    padding: 8px 24px;
    border-radius: 30px;
    font-family: 'Poppins';
    display: flex;
    align-items: center;
    font-size: 12px;
  }
  #mail-detail #overlap #mail-actions div:nth-child(2) .btn img {
    margin-right: 8px;
    fill: #ff4133;
  }
  #mail-detail #overlap #mail-actions div:nth-child(2) .btn:hover {
    background: #ddd;
    cursor: pointer;
  }
  #mail-detail #overlap #mail-actions div:nth-child(2) .btn-hollow {
    background: transparent;
    border: 1px solid white;
    color: white;
  }
  #mail-detail #overlap #mail-actions div:nth-child(2) .btn-hollow:hover {
    background: #f45b50;
  }
  #mail-detail #overlap #mail-actions div:nth-child(2) > .btn {
    margin-right: 16px;
  }
  #mail-detail #mail-content {
    z-index: 3;
    margin: 0px 6px;
    position: relative;
    top: -40px;
    background: white;
    border-radius: 10px;
    padding: 16px;
  }
  #mail-detail #mail-content > div > p {
    font-size: 18px;
  }
  #mail-detail #mail-content > div > p + p {
    font-size: 12px;
    color: rgba(0, 0, 0, 0.54);
  }
  #mail-detail #mail-content > div + p {
    margin-top: 24px;
    font-size: 14px;
  }






</style>
