<template>
    <div id="login">
        <div class="login container">
            <div class="container" id="container">
                <div class="form-container sign-up-container">
                    <div class="form-element">
                        <h1>Provider details</h1>
                        <span>Use your personal mail</span>
                        <input id="name" v-bind="username" placeholder="Name" type="text"/>
                        <input id="email" v-bind="usermail" placeholder="Email" type="email"/>
                        <input id="password" v-bind="password" placeholder="Password" type="password"/>
                        <br>
                        <input id="imap" v-bind="imapserver" placeholder="Server IMAP" type="text"/>
                        <input id="smtp" v-bind="smtpserver" placeholder="Server SMTP" type="text"/>
                        <div v-if="mustShowAdvanced">
                        <span>Set server configuration</span>
                        <select id="platform_selector" name="platform_selector" onchange="setServerSettings()">
                            <option value="-1">--- Custom platform ---</option>
                        </select>

                        <div class="inline">
                            <input id="ssl" type="checkbox" value="ssl">SSL
                            <input id="starttls" type="checkbox" value="starttls">starttls
                        </div>
                        <div class="inline">
                            <input id="ssl_context" type="checkbox" value="ssl_context">SSL_CONTEXT
                        </div>
                        </div>

                        <button type="submit" @click="providerSignin()">Sign Up</button>
                    </div>
                </div>
                <div class="form-container sign-in-container">
                        <div class="form-element">
                        <h1>Sign in with NextBlu</h1>
                        <span>One account: multiple apps.</span>
                        <input placeholder="username@nextblu.com" id="nextblu-username" type="email"
                        v-bind="next_username"/>
                        <input placeholder="MyIncrediblePassword1" id="nextblu-password" type="password"
                        v-bind="next_password"/>
                        <a href="#">Forgot your password?</a>
                        <button @click="nextSigning()">Sign In</button>
                        </div>
                </div>

                <div class="overlay-container">
                    <div class="overlay">
                        <div class="overlay-panel overlay-left">
                            <h1>NextBlu?</h1>
                            <p>With NextBlu your informations are synced. One account: multiple apps.</p>
                            <button class="ghost" id="signIn">Sign In With NextBlu</button>
                        </div>
                        <div class="overlay-panel overlay-right">
                            <h1>First Time here?</h1>
                            <p>You can log-in with your provider by clicking here</p>
                            <button class="ghost" id="signUp">Sign Up With a Provider</button>
                        </div>
                    </div>
                </div>


            </div>


            <footer>
                <p>
                    This is an ALPHA version. <i class="fa fa-heart"></i> Read more about NextBlu login system <a>here</a>.
                </p>
            </footer>
        </div>
    </div>
</template>

<script scoped>
    export default {
        name: "Login",
        data() {
            return {
                hasPermissions: true,
                serverErrorCode: 999,
                serverErrorMessage: "",

                next_username: '',
                next_password: '',

                username: '',
                usermail: '',
                password: '',
                imapserver: '',
                smtpserver: '',

                mustShowAdvanced: false
            };
        },
        methods: {
            nextSigning(){
                let username = this.next_username;
                let password = this.next_password;
                try {
                    let verification_imap = eel.check_imap_connection(username, password, "mail.nextblu.com", false, null, true)();
                    let verification_smtp = eel.check_smtp_connection(username, password, "mail.nextblu.com")();
                    if (verification_imap && verification_smtp) {
                        eel.user_registration(username, username, password, "mail.nextblu.com", "mail.nextblu.com", "1");
                        //this.$router.push('Home')

                        // @todo: VALIDATE THE COOKIE

                        this.$router.push({ name: 'Home', params: {firstLogin: 'yep' }})
                    } else {
                        //toastr.error("We can't login into your inbox. Please verify your password or email address.", "Incorrect informations");
                        this.$toasted.error("We can't login into your inbox. Please verify your password or email address.");
                        console.log("User informations incorrect");
                    }
                }catch (e) {
                    this.$toasted.error("Something bad happened: "+e);
                }
            },
            providerSignin(){
                let username = this.username;
                let usermail = this.usermail;
                let password = this.password;
                let imap_address = this.imapserver;
                let smtp_address = this.smtpserver;

                try {


                    if (eel.custom_user_registration(username, usermail, password, imap_address, smtp_address)) {
                        // @todo: Redirect to home
                        // @todo: validate the cookie
                    } else {
                        // We can't find any settings -> showing the user an advanced tab with an error toast.
                        this.$toasted.info("It seems that we have some difficulties loggin in your inbox. Please " +
                            "review your settings! ");
                    }
                }catch (e) {
                    this.$toasted.error("Something bad happened: "+e);
                }

            }
        },
        created() {
            this.$toasted.success("Welcome on board!", {type: "success",
                position: "top-right", duration: 3000});
        },
        mounted() {


            // Importing Jquery
            let jQuery = document.createElement('script')
            jQuery.setAttribute('src', 'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js')
            document.head.appendChild(jQuery);

            // Some Jquery transition magic
            const signUpButton = document.getElementById('signUp');
            const signInButton = document.getElementById('signIn');
            const container = document.getElementById('container');

            signUpButton.addEventListener('click', () => {
                container.classList.add("right-panel-active");
            });

            signInButton.addEventListener('click', () => {
                container.classList.remove("right-panel-active");
            });
        },
    }
</script>

<style scoped>
    @import "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.7.2/css/all.min.css";
    @import url('https://fonts.googleapis.com/css?family=Montserrat:400,800');



    * {
        box-sizing: border-box;
    }

    #login {
        width: 100%;
        background: #f6f5f7 url("../assets/img/daniel-olah.jpg") no-repeat center;
        background-size: cover; /* Resize the background image to cover the entire container */
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        font-family: 'Montserrat', sans-serif;
        height: 100vh;
        overflow-y: hidden;
        /*margin: -20px 0 50px;*/
    }

    .login {
        width: 100%;
    }

    .body {
        background: #f6f5f7 url("../assets/img/daniel-olah.jpg") no-repeat center;
        background-size: cover; /* Resize the background image to cover the entire container */
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        font-family: 'Montserrat', sans-serif;
        height: 90vh;
        margin: -20px 0 50px;
    }

    h1 {
        /*font-weight: bold;*/
        margin: 0;
    }

    /*h2 {
        text-align: center;
    }*/

    p {
        font-size: 14px;
        font-weight: 100;
        line-height: 20px;
        letter-spacing: 0.5px;
        margin: 20px 0 30px;
    }

    span {
        font-size: 12px;
    }

    a {
        color: #333;
        font-size: 14px;
        text-decoration: none;
        margin: 15px 0;
    }

    button {
        border-radius: 20px;
        border: 1px solid #FF4B2B;
        background-color: #FF4B2B;
        color: #FFFFFF;
        font-size: 12px;
        font-weight: bold;
        padding: 12px 45px;
        letter-spacing: 1px;
        text-transform: uppercase;
        transition: transform 80ms ease-in;
    }

    button:active {
        transform: scale(0.95);
    }

    button:focus {
        outline: none;
    }

    button.ghost {
        background-color: transparent;
        border-color: #FFFFFF;
    }

    form {
        background-color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0 50px;
        height: 100%;
        text-align: center;
    }


    .form-element {
        background-color: #FFFFFF;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0 50px;
        height: 100%;
        text-align: center;
    }

    input {
        background-color: #eee;
        border: none;
        padding: 12px 15px;
        margin: 8px 0;
        width: 100%;
    }

    select {
        background-color: #eee;
        border: none;
        padding: 12px 15px;
        margin: 8px 0;
        width: 100%;
    }

    .inline {
        display: inline;
        left: 0px;
    }

    .container {
        background-color: #fff;
        border-radius: 10px;
        box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25),
        0 10px 10px rgba(0, 0, 0, 0.22);
        position: relative;
        overflow: hidden;
        width: 868px;
        max-width: 100%;
        min-height: 700px;
    }

    .form-container {
        position: absolute;
        top: 0;
        height: 100%;
        transition: all 0.6s ease-in-out;
    }

    .sign-in-container {
        left: 0;
        width: 50%;
        z-index: 2;
    }

    .container.right-panel-active .sign-in-container {
        transform: translateX(100%);
    }

    .sign-up-container {
        left: 0;
        width: 50%;
        opacity: 0;
        z-index: 1;
    }

    .container.right-panel-active .sign-up-container {
        transform: translateX(100%);
        opacity: 1;
        z-index: 5;
        animation: show 0.6s;
    }

    @keyframes show {
        0%, 49.99% {
            opacity: 0;
            z-index: 1;
        }

        50%, 100% {
            opacity: 1;
            z-index: 5;
        }
    }

    .overlay-container {
        position: absolute;
        top: 0;
        left: 50%;
        width: 50%;
        height: 100%;
        overflow: hidden;
        transition: transform 0.6s ease-in-out;
        z-index: 100;
    }

    .container.right-panel-active .overlay-container {
        transform: translateX(-100%);
    }

    .overlay {
        background: #001f3f;
        background: -webkit-linear-gradient(to right, #001f3f, #002d87);
        background: linear-gradient(to right, #001f3f, #003686);
        background-repeat: no-repeat;
        background-size: cover;
        background-position: 0 0;
        color: #FFFFFF;
        position: relative;
        left: -100%;
        height: 100%;
        width: 200%;
        transform: translateX(0);
        transition: transform 0.6s ease-in-out;
    }

    .container.right-panel-active .overlay {
        transform: translateX(50%);
    }

    .overlay-panel {
        position: absolute;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        padding: 0 40px;
        text-align: center;
        top: 0;
        height: 100%;
        width: 50%;
        transform: translateX(0);
        transition: transform 0.6s ease-in-out;
    }

    .overlay-left {
        transform: translateX(-20%);
    }

    .container.right-panel-active .overlay-left {
        transform: translateX(0);
    }

    .overlay-right {
        right: 0;
        transform: translateX(0);
    }

    .container.right-panel-active .overlay-right {
        transform: translateX(20%);
    }

    .social-container {
        margin: 20px 0;
    }

    .social-container a {
        border: 1px solid #DDDDDD;
        border-radius: 50%;
        display: inline-flex;
        justify-content: center;
        align-items: center;
        margin: 0 5px;
        height: 40px;
        width: 40px;
    }

    footer {
        background-color: #222;
        color: #fff;
        font-size: 14px;
        bottom: 0;
        position: fixed;
        left: 0;
        right: 0;
        text-align: center;
        z-index: 999;
    }

    footer p {
        margin: 10px 0;
    }

    footer i {
        color: red;
    }

    footer a {
        color: #3c97bf;
        text-decoration: none;
    }
</style>