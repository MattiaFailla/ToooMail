<template>
    <div class="home">
        <el-container v-loading.fullscreen.lock="fullscreenLoading">


            <el-row class="row-bg" type="flex">
                <el-col :span="1">
                    <el-menu :collapse="isCollapse" @close="handleClose"
                             @mouseover="isCollapse"
                             @open="handleOpen"
                             active-text-color="#ffd04b"
                             background-color="#545c64"
                             class="el-menu-vertical-demo"
                             default-active="2"
                             style="min-height: 100vh; z-index: 90"
                             text-color="#fff"
                    >
                        <img alt="logo" src="../assets/img/logo_svg.svg" style="background-color: inherit" width="100%">
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
                            <el-badge :max="99" :value="numberUnread" type="info">
                                <i class="el-icon-menu"></i>
                                <span slot="title">Inbox</span>
                            </el-badge>
                        </el-menu-item>


                        <el-menu-item @click="isWriting = true" index="-1">
                            <i class="el-icon-edit-outline"></i>
                            <span slot="title">Write an email</span>
                        </el-menu-item>
                        <el-menu-item @click="requireNewMailRow('sent')" index="3">
                            <i class="el-icon-s-promotion"></i>
                            <span slot="title">Sent</span>
                        </el-menu-item>
                        <el-menu-item @click="requireNewMailRow('flagged')" index="4">
                            <i class="el-icon-s-flag"></i>
                            <span slot="title">Flagged</span>
                        </el-menu-item>
                        <el-menu-item @click="requireNewMailRow('drafts')" index="5">
                            <i class="el-icon-document"></i>
                            <span slot="title">Drafts</span>
                        </el-menu-item>
                        <el-menu-item @click="requireNewMailRow('spam')" index="6">
                            <i class="el-icon-delete"></i>
                            <span slot="title">Spam</span>
                        </el-menu-item>
                        <el-menu-item index="7">
                            <i class="el-icon-setting"></i>
                            <span slot="title">Settings</span>
                        </el-menu-item>
                        <el-menu-item @click="lockTheSession()" index="8">
                            <i class="el-icon-lock"></i>
                            <span slot="title">Lock the session</span>
                        </el-menu-item>


                        <el-avatar class="user-avatar"
                                   src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png">
                        </el-avatar>


                    </el-menu>
                </el-col>
                <el-col :span="7" class="mail-row-col" v-loading="isLoadingMailsRow" element-loading-text="We are getting the latest emails.. 🚀">

                    <div class="tm-search-bar">
                        <input id="search_bar" placeholder="Search..." type="text" v-model="search">
                        <span><i class="fas fa-search"></i></span>
                    </div>


                    <div class="flex-column" id="mail-list" v-if="!isLoadingMailsRow">
                        <div :class="{selected: isSelected(index)}" :key="index"
                             @click="openEmail(index)"
                             class="mail-itemm"
                             v-for="(email, index) in emails.filter(data => !search || data.subject.toLowerCase().includes(search.toLowerCase()))">


                            <div class="Email dark" v-if="emails.length > 0">
                                <div class="ImgWrapper notif">
                                    <img :src="email.profilePic" class="img">

                                    <!--<div class="img notif">
                                    </div>-->
                                </div>
                                <div class="EmailTitle">
                                    <p class="EmailTime">{{email.sent|datetime}}</p>
                                    <h1 class="EmailSenderName">{{email.sender.name}}</h1>
                                    <h2 class="EmailSubject">{{email.subject}}</h2>
                                    <!--<p class="EmailPreview">Hi Matt! Are you available for...</p>-->
                                </div>
                            </div>


                        </div>
                    </div>


                </el-col>
                <el-col :span="20" class="mail-body-container">

                    <div class="tm-wrapper" id="tm-wrapper">


                        <div class="tm-open-message shadow-lg">
                            <div class="tm-mail-content">

                                <div id="mail-detail">
                                    <div id="overlap">
                                        <div class="flex center-vertical" id="mail-actions">
                                            <div class="flex center-vertical">
                                                <p class="flex center-vertical center-horizontal">
                                                    {{selectedEmail.sender.name[0]}}</p>
                                                <div>
                                                    <p>{{selectedEmail.sender.name}}</p>
                                                    <p>{{selectedEmail.sender.email}}</p>
                                                </div>
                                            </div>
                                            <div class="flex center-vertical">
                                                <button class="btn">
                                                    <img alt="reply" src="../assets/img/baseline-reply-24px.svg"/>
                                                    Reply
                                                </button>
                                                <button class="btn btn-hollow">
                                                    <img class="img-white"
                                                         src="../assets/img/baseline-reply_all-24px.svg"/>
                                                    Forward
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                    <div id="mail-content">
                                        <div>


                                            <el-row>
                                                <el-col :span="12">
                                                    <p>{{selectedEmail.subject}}</p>
                                                    <p>{{selectedEmail.sent}}</p>
                                                </el-col>
                                                <el-col :span="12">
                                                    <el-button icon="el-icon-search" circle></el-button>
                                                    <el-button type="primary" icon="el-icon-edit" circle></el-button>
                                                    <el-button type="success" icon="el-icon-check" circle></el-button>
                                                    <el-button type="info" icon="el-icon-message" circle></el-button>
                                                    <el-button type="warning" icon="el-icon-star-off" circle></el-button>
                                                    <el-button type="danger" icon="el-icon-delete" circle></el-button>

                                                </el-col>
                                            </el-row>
                                        </div>
                                        <p v-html="selectedEmail.body"></p>
                                    </div>
                                </div>

                            </div>
                        </div>

                    </div>


                </el-col>


            </el-row>


            <el-dialog
                    :before-close="handleClose"
                    :visible.sync="isWriting"
                    title="Write a new email"
                    width="60%">

        <span>
          <el-form :model="form" ref="form">
            <el-form-item label="Recipient email">
              <el-input v-model="form.name"></el-input>
            </el-form-item>

            <el-form-item label="Instant delivery">
              <el-switch v-model="form.delivery"></el-switch>
            </el-form-item>
            <el-form-item label="Select an automatic delivery date" v-if="!form.delivery">
              <el-col :span="5">
                <el-date-picker placeholder="Pick a date" style="width: 100%;" type="date"
                                v-model="form.date1"></el-date-picker>
              </el-col>
              <el-col :span="2" class="line">-</el-col>
              <el-col :span="5">
                <el-time-picker placeholder="Pick a time" style="width: 100%;" v-model="form.date2"></el-time-picker>
              </el-col>
            </el-form-item>
            <el-form-item label="Add attachments"><br>
              <el-upload
                      :file-list="form.files"
                      class="upload-demo"
                      drag
                      multiple>
                <i class="el-icon-upload"></i>
                <div class="el-upload__text">Drop file here or <em>click to upload</em></div>
                <div class="el-upload__tip" slot="tip">Files with a size less than 500mb</div>
              </el-upload>
            </el-form-item>
            <el-form-item label="Mail">
              <el-input type="textarea" v-model="form.desc"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button @click="isWriting = false" type="primary">Save for later</el-button>
            </el-form-item>
          </el-form>
        </span>

                <span class="dialog-footer" slot="footer">


          <el-button @click="dialogVisible = false">Cancel</el-button>
    <el-button @click="dialogVisible = false" type="primary">Confirm</el-button>


  </span>
            </el-dialog>

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
                fullscreenLoading: false,
                src: 'https://cube.elemecdn.com/6/94/4d3ea53c084bad6931a56d5158a48jpeg.jpeg',
                isCollapse: true,
                form: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: true,
                    type: [],
                    files: [],
                    resource: '',
                    desc: ''
                },
                perPage: 5,
                currentPage: 1,
                selectedIndex: -1,

                search: '',

                isWriting: false,

                emails: [
                    {
                        sender: {name: "Next Blu", email: "hello@nextblu.com"},
                        subject: "Some exciting news",
                        body: "Necessary ye contented newspaper zealously breakfast he prevailed. Melancholy middletons yet understood decisively boy law she. Answer him easily are its barton little. Oh no though mother be things simple itself. Dashwood horrible he strictly on as. Home fine in so am good body this hope.",
                        sent: '7:11 AM',
                        profilePic: 'https://eu.ui-avatars.com/api/?name=Next Blu'
                    }/*,
          {
            sender: { name: "Jack Doe", email: "jackdoe@gmail.com" },
            subject: "Material expenses",
            body: "Expenses as material breeding insisted building to in. Continual so distrusts pronounce by unwilling listening. Thing do taste on we manor. Him had wound use found hoped. Of distrusts immediate enjoyment curiosity do. Marianne numerous saw thoughts the humoured. ",
            sent: '8:12 AM'
          },*/
                ],

                // SAVING THE TYPE OF PAGE TO SHOW
                isMainApp: true,
                isSettingsPage: false,
                isWriteEmailPage: false,
                isProfilePage: false,

                // USER INFOS
                username: '',

                // MAIL HELPER
                numberUnread: 0,
                isLoadingMailsRow: false
            }
        },

        mounted() {
            var cookies = this.$cookies.get("isLoggedIn");  // return value
            // check the cookie
            if (cookies == null) {
                console.log("USER NOT LOGGED.");
                //this.$router.push('Login')
            }
            this.onPageLoad();
        },
        computed: {
            totalPages() {
                return Math.ceil(this.emails.length / this.perPage);
            },
            pagination() {
                return `Page ${this.currentPage} of ${this.totalPages}`;
            },
            hasPrevPage() {
                return this.currentPage - 1 > 0;
            },
            hasNextPage() {
                return this.currentPage < this.totalPages;
            },
            selectedEmail() {
                return this.emails[this.selectedIndex];
            }
        },
        methods: {
            // Core functions
            lockTheSession() {
                /**
                 * Locking the session by setting the 'isSessionValid' to false
                 * and redirecting to Locked page
                 */

                // @todo: saving in the cookie the logged status
                this.$router.push({name: 'Locked', params: {fromHome: 'yep'}})
            },
            onPageLoad() {
                /**
                 *  Loading data on page lod when the DOM is ready
                 *  for changes
                 *
                 *  Loading following data:
                 *  + username
                 *  + number of unread emails
                 *  + row of the inbox
                 *  */
                    // Getting the background image
                let max = 30;
                let min = 1;
                let randInt = Math.floor(Math.random() * (+max - +min)) + +min;
                console.info("Random background id: " + randInt)
                document.getElementById("tm-wrapper").style.backgroundImage = 'url(https://dir1.nextblu.com/tooomail/assets/wallpaper/' + randInt + '.jpg)';

                // Getting user info and pong status


                eel.get_username()((username) => {
                    vm.username = username;
                })

                eel.get_number_unread()((number) => {
                    vm.numberUnread = number;
                })

                this.requireNewMailRow();

            },
            openLoadingFullScreen() {
                /**
                 * Showing a full screen loader
                 */

                let vm = this;
                this.fullscreenLoading = true;

                setTimeout(() => {
                    this.fullscreenLoading = false;
                    vm.$message.info("Hey " + vm.username + " welcome back!")
                }, 2000);
            },
            openEmail(index) {
                /**
                 * Opening the mail on the right side by selecting the right emails[] id
                 */
                this.selectedIndex = index;
            },
            isSelected(index) {
                return this.selectedIndex === index;
            },
            requireNewMailRow(rowType = "inbox") {
                // Getting the new mail row from the backend
                /**
                 * This function will reload the mail row.
                 * @param {string} rowType     Indicates the page to load.
                 *
                 * The mail row is saved in data [emails]
                 */
                this.logger("Getting mail data for " + rowType)
                this.isLoadingMailsRow = true;
                let vm = this;
                let maildata;
                switch (rowType) {
                    default:
                    case "inbox":
                        eel.get_mails(50)((data) => {
                            maildata = data;
                            vm.updateMailData(data);
                            console.log(data)
                        });
                        break;
                    case "unread":
                        eel.get_unread()((data) => {
                            maildata = data;
                            vm.updateMailData(data);
                            console.log(data)
                        });
                        break;
                    case "sent":
                        eel.get_sent()((data) => {
                            maildata = data;
                            vm.updateMailData(data);
                            console.log(data)
                        });
                        break;
                    case "flagged":
                        eel.get_flagged()((data) => {
                            maildata = data;
                            vm.updateMailData(data);
                            console.log(data)
                        });
                        break;
                    case "drafts":
                        eel.get_unread()((data) => {
                            maildata = data;
                            vm.updateMailData(data);
                            console.log(data)
                        });
                        break;
                    case "spam":
                        eel.get_deleted()((data) => {
                            maildata = data;
                            vm.updateMailData(data);
                            console.log(data)
                        });
                        break;
                }

            },
            updateMailData(data) {
                /***
                 * Upgrading the data.emails row with the new data from the backend service
                 * */
                this.logger("Updating the mail row data.");
                /*
                sender: { name: "Jane Doe", email: "janedoe@gmail.com" },
                    subject: "Necessary newspaper",
                    body: "Necessary ye contented newspaper zealously breakfast he prevailed. Melancholy middletons yet understood decisively boy law she. Answer him easily are its barton little. Oh no though mother be things simple itself. Dashwood horrible he strictly on as. Home fine in so am good body this hope.",
                    sent: '7:11 AM'
                    }
                */
                let vm = this;
                let appdata = []
                data.forEach(function (data) {
                    let profilePic = "https://eu.ui-avatars.com/api/?name="+data.From_name
                    appdata.push({
                        "sender": {"name": data.From_name, "email": data.From_mail},
                        "subject": data.Subject,
                        "body": data.bodyHTML,
                        "sent": data.datetimes,
                        "profilePic": profilePic
                    });
                })
                vm.emails = appdata;
                vm.isLoadingMailsRow = false
            },
            logger(message, type = null) {
                /** Logging data back to tentalog and std:log
                 *
                 */
                if (type === "error") {
                    console.error(message);
                    eel.ui_log_error(message);
                }
                console.info(message);
                eel.ui_log(message)();

            },
            // Side menu functions
            handleOpen(key, keyPath) {
                console.log(key, keyPath);
            },
            handleClose(key, keyPath) {
                console.log(key, keyPath);
            },
            handleRemove(file, fileList) {
                console.log(file, fileList);
            },


        },
        created() {
            /**
             * This function will be fired before the DOM creation.
             */
            let vm = this;
            try {
                eel.pong()((val) => {
                    console.info(val);
                })
            }catch (e) {
                console.error(e);
                console.info("Is the server up and running?");
                vm.$message.error({
                    message: "Something really bad happened. Please close and reopen the app.",
                    duration: 0
                }
            )
                return
            }
            this.openLoadingFullScreen()
            this.selectedIndex = 0;
        }
    }
</script>

<style scoped>

    @import url(https://fonts.googleapis.com/css?family=Open+Sans:300|Roboto+Mono);

    #home {
        overflow-x: hidden;
        font-family: "Poppins", Arial, serif;
    }

    /* scroll bar */
    .scroll, .scroll-x, .scroll-y {
        -webkit-overflow-scrolling: auto;
    }

    ::-webkit-scrollbar {
        width: 6px;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-track {
        background: none;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(216, 216, 216, 0.8);
        border-radius: 10px;
    }


    .user-avatar {
        position: absolute;
        left: 19%;
        bottom: 20px;
    }


    .tm-search-bar {
        color: #c8cae3;
        font-size: 1.4rem;
        background-color: #EBEBF6;
        padding: 10px 15px;
        border-radius: 3px;
        margin: 10px 10px 15px;
    }

    .tm-search-bar input {
        border: none;
        outline: none;
        background-color: transparent;
        /*color: darken(#E0E1EF, 7%);*/
        color: black;
    }

    .tm-search-bar span {
        float: right;
    }

    .mail-row-col {
        height: 100vh;
        min-width: 20%;
        max-height: 100vh;
        overflow-y: auto;
        background: linear-gradient(to bottom, #313a5a 0%, #424a6b 100%);
    }

    #mail-list {
        margin-right: 0px;
        position: inherit;
    }

    .Email {
        box-sizing: border-box;
        border-radius: 3px;
        background: rgba(255, 255, 255, 0.11);
        padding: 5px;
        width: 100%;
        max-width: 90%;
        max-height: 100px;
        overflow: hidden;
        margin: 3px auto;
        transition: all .3s;
        display: flex;
        flex-wrap: wrap;
        cursor: pointer;
        position: relative;
        opacity: 1;
        height: 70px;
    }

    .Email:hover{
        background: rgba(255, 255, 255, 0.15);
    }

    .EmailSenderName{
        color: white;
    }
    .EmailSubject{
        color: white;
    }

    .NoDataMail {
        background: rgba(255, 255, 255, .4);
    }

    .Email.active {
        /*margin-top: -76px;
        padding: 10px 0px;*/
        background: #21294a;
        color: #fff;
        z-index: 15;
        max-width: 100%;
        cursor: initial;
        border-radius: 0px;
    }

    .Email.deactive {
        max-height: 0px;
        padding: 0px;
        margin: 0px auto;
        opacity: 0;
    }

    .Email .ImgWrapper {
        width: 20%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .Email .img {
        width: 40px;
        height: 40px;
        border-radius: 100%;
        position: relative;
    }

    .Email .img.notif:before {
        content: " ";
        display: block;
        width: 12px;
        height: 12px;
        background: #5bc3e4;
        border-radius: 100%;
        border: 2px solid #868b9d;
        position: absolute;
        top: -2px;
        left: -2px;
        opacity: 1;
        transition: all .3s;
    }

    .Email.active .img.notif:before {
        opacity: 0;
    }

    .EmailTitle {
        width: 80%;
        position: relative;
        color: #fff;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
    }

    .EmailTitle .EmailTime {
        position: absolute;
        top: 0px;
        right: 0px;
        font-size: 12px;
        font-weight: 100;
        margin: 0px;
        padding: 5px;
    }

    .EmailTitle h1 {
        margin: 0px;
        padding: 0px;
        font-size: 15px;
        line-height: 1em;
        font-weight: 500;
        width: 100%;
    }

    .EmailTitle h2 {
        margin: 0px;
        padding: 3px 0px;
        font-size: 12px;
        line-height: 1em;
        font-weight: 300;
    }

    .EmailTitle p.EmailPreview {
        margin: 5px 0px;
        max-height: 25px;
        padding: 0px;
        font-size: 12px;
        font-weight: 100;
        opacity: .8;
        overflow: hidden;
        transition: all .3s;
    }

    .Email.active .EmailTitle p.EmailPreview {
        max-height: 0px;
    }

    .mail-body-container {
        height: 100vh;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .tm-wrapper {
        height: 100vh;
        background-color: #EEF1F6;
        max-height: 100%;
        overflow-y: auto;
        background-image: url("//");
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
        margin: 15px;
        background: #F8F9F9;
        /*margin-left: 32px;*/
        border-radius: 10px;
        z-index: 1;
        overflow-y: auto;
        overflow-x: hidden;
    }

    #mail-detail #overlap {
        height: 150px;
        border-radius: 10px 10px 0px 0px;
        background: #001f3f;
        border-color: #001f3f;
        z-index: 2;
        width-min: 100%;
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
        background: rgba(244, 91, 80, 0.88);
    }

    #mail-detail #overlap #mail-actions div:nth-child(2) > .btn {
        margin-right: 16px;
    }

    #mail-detail #mail-content {
        z-index: 3;
        margin: 0 6px;
        position: relative;
        top: -40px;
        background: #F8F9F9;
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

    .el-menu-vertical-demo {
        width: 100%;
        margin-right: 0;
        border-right: rgba(216, 216, 216, 0.6);
    }


</style>
