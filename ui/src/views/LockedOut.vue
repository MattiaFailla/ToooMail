<template>
    <div id="locked">
        <nav class='tbar'>
            <span class='percent'>ToooMail</span>
            <i class="fas fa-envelope">
            </i>
            <span class=time id="time">7:21 PM</span>
            <i class="fas fa-clock">
            </i>
        </nav>
        <div class='content'>
            <div class='input-wrap'>
                <div class='pic'></div>
                <div class='wrap'>
                    <h3 class='name' id="username">...</h3>
                </div>
                <input type='password' id='password' placeholder='Enter Password' autocomplete='off'>
                <button class='arrow'><i class="fas fa-arrow-right"></i>
                </button>
            </div>
        </div>
        <p style="text-align: center;">Photo by NASA on Unsplash</p>
    </div>
</template>

<script>
    export default {
        name: "LockedOut"
    }
</script>

<style scoped>
    @import url("https://use.fontawesome.com/releases/v5.7.2/css/all.css");
    @import url("https://fonts.googleapis.com/css?family=Heebo:300");

    #locked {
        margin: 0;
        padding: 0;
        font-family: 'Heebo', sans-serif;
        height: 100%;
        width: 100%;
        background-image: url(../assets/img/nasa-locked.jpg);
        background-position: center center;
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        box-shadow: inset 0 0 0 1000px rgba(0,0,0,0.5);
        color: white;
    }

    .tbar {
        color: white;
        font-size: 12px;
        display: flex;
        padding: 5px;
        justify-content: flex-end;
        place-items: center;
    }

    .tbar > i, .tbar > .time{
        padding-right: 8px;
    }

    .percent {
        padding-right: 5px;
    }

    .content {
        width: 100%;
        height: 90vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }


    .pic {
        margin: 0 auto;
        width: 80px;
        height: 80px;
        border-radius: 100%;
        background-image: url(../assets/img/iconToooMail.png);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-color: grey;
    }

    /* had to do this to center the username */
    .wrap {
        display: flex;
        font-weight: lighter;
        font-size: 18px;
    }

    .name {
        margin: 20px auto;
        font-family: 'Heebo', sans-serif;
        letter-spacing: 1px;
    }

    #password {
        font-size: 17px;
        color: white;
        background-color: hsla(0, 0%, 45%, 0.7);
        border: none;
        border-radius: 10px;
        height: 30px;
        padding: 0 5px;

    }

    #password::placeholder {
        font-size: 14px;
        vertical-align: center;
        color: rgb(170,170,170);
    }

    input:focus {
        outline: none;
    }

    .arrow {
        width: 25px;
        height: 25px;
        font-size: 14px;
        border-radius: 100%;
        display: none;
        justify-content: center;
        align-items: center;
        background-color: rgb(170,170,170);
        border: none;
        color: rgba(0,0,0,0.7);
        padding: 3px;
        margin-left: 5px;
        margin-right: -35px;
    }

    button:focus {
        outline: none;
    }

    button:active {
        border: none;
        background-color: hsla(0, 0%, 75%, 0.7);
    }

    .toolbar > div > i {
        font-size: 12px;
        padding: 1px;
    }

    .pointers > i {
        color: grey;
        padding: 0 5px;
        font-size: 12px;
    }

    main {
        width: 80%;
        text-align: center;
        margin: 20px auto 0;
        color: black;
    }
</style>