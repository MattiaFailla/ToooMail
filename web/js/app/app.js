// disabling right click on the page
document.addEventListener('contextmenu', event => event.preventDefault());


eel.

 eel.expose(say_hello_js);               // Expose this function to Python
 function say_hello_js(x) {
     console.log("Hello from " + x);
 }
 
 say_hello_js("Javascript World!");
 eel.say_hello_py("Javascript World!");  // Call a Python function

 var email_pack = null;

 //icon pack name dictionary
 var iconset = [
  "amazon",
  "android",
  "apple",
  "app-store",
  "behance",
  "blogger",
  "chrome",
  "delicious",
  "devuantart",
  "dribbble",
  "drive",
  "dropbox",
  "edge",
  "facebook",
  "firefox",
  "flickr",
  "forrst",
  "github",
  "google-play",
  "google-plus",
  "html5",
  "instagram",
  "lastfm",
  "linkedin",
  "microsoft",
  "myspace",
  "opera",
  "pinterest",
  "rss",
  "safari",
  "skype",
  "soundcloud",
  "tumblr",
  "twitter",
  "vimeo",
  "wordpress",
  "yahoo",
  "youtube"
]; 


function getImage(name) {
    var included = iconset.includes(name.toLowerCase(),0);
    var iconposition = "";
    if (included) {
        iconposition = "img/logoset/"+name.toLowerCase()+".svg";
    }else{
        iconposition = "img/logoset/cape.svg";
    }
    return iconposition;
};

async function setNumberUnread(){
  let NumberUnread = await eel.get_number_unread()();
  var NumberUnreadSpan = document.getElementById("NumberUnread");
  NumberUnreadSpan.innerHTML = NumberUnread;
};

setNumberUnread();

 async function getEmails() {
    console.log("Waiting the backend");


    // Let's take the data from the backend
    let emails = await eel.get_mails()(2019,08,21);
    console.log("emails: \n");
    console.log(emails); // we need to itarate this in order to display

    email_pack = emails;

    // delete the loading gif - loading-image
    var loading_img = document.getElementById("loading-image");
    loading_img.parentNode.removeChild(loading_img);



    for (var i = 0; i < emails.length; i++) {


      const li = document.createElement('li');
      li.className = 'inbox-item';

      li.onclick = `show_mail(${i})`
      li.setAttribute("onclick",`show_mail(${i});`);

      let summary_special = emails[i]['Body_plain'].replace(/</g, "&lt;").replace(/>/g, "&gt;");
      summary_special = summary_special.substring(0, 150)

      let label = '<div class="message-labels-item blue" id="LabelId'+i+'"></div>';
      if (emails[i]['readed'] == true) {
          label = '<div class="message-labels-item"></div>';
      }

      li.innerHTML = `
        <div class="inbox-sender" message-id="${i}">
           <div class="sender-name"> <a href="#">${emails[i]['From_name']} </a></div>
           <div class="sender-date"><i class="sender-label fa fa-paperclip"></i><span>${emails[i]['Date']}</span></div>
        </div>
        <div class="inbox-title">
           ${label}
           <h4><img src="${getImage(emails[i]['From_name'])}" height="20" width="20"> ${emails[i]['Subject']}</h4>
        </div>
        <!--<p class="inbox-short">${summary_special}...</p> -->
      `;

      document.getElementById('inbox').appendChild(li);
    }

};

getEmails();

// When the user click the mail 
// we show the content on the right and check the mail as read
function show_mail(mailID) {
  eel.mark_as_seen(email_pack[mailID]['UID']);  // Mark the mail as seen
  try {
    document.getElementById("LabelId"+mailID).className = "message-labels-item"; 
  }catch(err) {
	  true;
  }

  var body_message = email_pack[mailID]['Body'];
  body_message = body_message.replace("['\\r\\n", "&lt;");
  body_message = body_message.replace("\\r\\n", "</br>");
  body_message = body_message.replace("\\n", "");

  var message_sender = document.getElementById('message');
  message_sender.innerHTML = `
      <div class="message-info">
          <div class="message-from">
             <img src="${getImage(email_pack[mailID]['From_name'])}" alt="img" />
             <div class="message-sender">
                <h5>${email_pack[mailID]['From_name']}, <a href="">${email_pack[mailID]['From_mail']}</a></h5>
                <span>To: <a href="${email_pack[mailID]['To_mail']}">${email_pack[mailID]['To_mail']}</a></span>
             </div>
          </div>
          <div class="message-tools"><i class="fa fa-reply"></i><i class="fa fa-star-o"></i><i class="fa fa-trash-o"></i> |<i class="fa fa-times-circle-o"></i></div>
       </div>
       <h2 class="message-title">${email_pack[mailID]['Subject']}</h2>

       ${body_message}
       
       <p class="message-body">
       </p>
    </div>
    `;

};

async function sendmail(account, to, subject, body, attach) {
    // pass arguments to python
    //eel.sendmail(account, to, subject,body,attach);

    Swal.fire({
      type: 'success',
      title: 'Yeah',
      text: 'Your email has been sent!',
      footer: '<a href>Would you like to view this discussion?</a>'
    })
}


// CHECK THE SERVER EVERY 10 SECONDS FOR INCOMING MAILS
window.setInterval(function(){
  eel.checkMails();
}, 5000);
 