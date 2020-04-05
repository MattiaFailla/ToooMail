<template>
  <div class="home">
    <section class="tm-sidebar">



      <div class="wapper">
        <img src="../assets/img/logo_transparent.png" class="tm-logo" style="z-index: 310;">


        <a href="#write" class="tm-btn-compose tm-text-center shadow-lg" data-toggle="modal" data-target="#composeEmail">
          <span class="tm-iconn"><i class="fas fa-edit"></i></span>
        </a>
        <div class="navigation">
          <nav class="primary-navigation">
            <ul>
              <li class="active" title="Inbox">
                <a href="#">
                  <span class="tm-iconn"><i class="far fa-envelope"></i></span>
                </a>
              </li>
              <li title="Flagged">
                <a href="#">
                  <span class="tm-iconn"><i class="far fa-flag"></i></span>
                </a>
              </li>
              <li title="Draft">
                <a href="#">
                  <span class="tm-iconn"><i class="far fa-file-alt"></i></span>
                </a>
              </li>
              <li title="Sent">
                <a href="#">
                  <span class="tm-iconn"><i class="far fa-paper-plane"></i></span>
                </a>
              </li>
              <li title="Bin">
                <a href="#">
                  <span class="tm-iconn"><i class="far fa-trash-alt"></i></span>
                </a>
              </li>
            </ul>
          </nav>
          <nav class="secondary-navigation">
            <ul>
              <li>
                <span class="tm-iconn tm-text-blue"><i class="far fa-square"></i></span>
              </li>
              <li>
                <span class="tm-iconn tm-text-green"><i class="far fa-square"></i></span>
              </li>
              <li>
                <span class="tm-iconn tm-text-yellow"><i class="far fa-square"></i></span>
              </li>
              <li>
                <span class="tm-iconn tm-text-red"><i class="far fa-square"></i></span>
              </li>
            </ul>
          </nav>
        </div>

        <div class="settings">


          <a data-toggle="modal" data-target="#viewProfile">
            <i class="fas fa-user"></i>
          </a>

          <a data-toggle="modal" data-target="#viewProfile">
            <i class="fas fa-lock"></i>
          </a>

          <a data-toggle="modal" data-target="#viewProfile">
            <i class="fas fa-store"></i>
          </a>

          <a href="#">
            <i class="fas fa-cog"></i>
          </a>


        </div>

        <!--<div class="container settings" style="padding-right: 1px; padding-left: 1px">
          <div class="row">
            <div class="col-sm-1">
              <a href="#">
                <i class="fas fa-cog"></i>
              </a>
            </div>
            <div class="col-sm-1">
              <a data-toggle="modal" data-target="#viewProfile">
                <i class="fas fa-user"></i>
              </a>
            </div>
            <div class="col-sm-1">
              <a data-toggle="modal" data-target="#viewProfile">
                <i class="fas fa-lock"></i>
              </a>
            </div>
            <div class="col-sm-1">
              <a data-toggle="modal" data-target="#viewProfile">
                <i class="fas fa-store"></i>
              </a>
            </div>
          </div>
        </div>-->


      </div>
    </section>

    <section class="tm-mails">

      <nav class="navbar navbar-dark bg-dark tm-mobile-navbar sticky-top">
        <!-- Navbar content -->
        <a class="navbar-brand" href="#">ToooMail</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Features</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Pricing</a>
            </li>
            <li class="nav-item">
              <a class="nav-link disabled" href="#">Disabled</a>
            </li>
          </ul>
        </div>
      </nav>
      <div class="tm-search-bar shadow-sm">
        <input type="text" id="search_bar" placeholder="Search...">
        <span><i class="fas fa-search"></i></span>
      </div>

      <div class="mail-list" id="mail-list">

        <!--<div class="tm-message shadow active-message">
          <div class="tm-message-status tm-hidden">
            <i class="fas fa-circle"></i>
          </div>
          <div class="tm-message-info">
            <div class="tm-message-sender-img">
              <img src="https://images.unsplash.com/photo-1504911539020-cfb0f7887a5e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="">
            </div>
            <div class="message-sender">
              <h4 class="tm-sender-name">Nicole Randall</h4>
              <p class="message-subject">
                The best travel destinations
              </p>
            </div>
            <div class="tm-message-timestamp">
              <small>2:05 PM</small>
            </div>
          </div>
          <p class="tm-message-preview">
            Hi Chriss! Towards the end of every year we look at the year ahead through a ...
          </p>
          <div class="tm-message-folder-indicator tm-bg-blue"></div>
        </div>

        <div class="tm-message shadow">
          <div class="tm-message-status tm-text-red">
            <i class="fas fa-circle"></i>
          </div>
          <div class="tm-message-info">
            <div class="tm-message-sender-img">
              <img src="https://images.unsplash.com/photo-1520466809213-7b9a56adcd45?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="">
            </div>
            <div class="message-sender">
              <h4 class="tm-sender-name">Jane Roberts</h4>
              <p class="message-subject">
                Pro Account
              </p>
            </div>
            <div class="tm-message-timestamp">
              <small>8:56 AM</small>
            </div>
          </div>
          <p class="tm-message-preview">
            Hi there, when you upgrade to Pro Business, the cost will be prorated ...
          </p>
          <div class="tm-message-folder-indicator tm-bg-yellow"></div>
        </div> -->


        <div class="d-flex justify-content-center" id="mail-row-loader-cont">
          <div class="spinner-border text-primary" style="width: 3rem; height: 3rem; margin-top: 20px;" role="status" id="mail-row-loader">
            <span class="sr-only">Loading...</span>
          </div>
        </div>




      </div>
    </section>
    <section class="tm-mail-viewer">





      <!--<div class="tm-controls">
        <div class="back-btns">
          <button class="back-btn">
            <i class="fas fa-arrow-left"></i>
          </button>
          <button class="back-btn">
            <i class="fas fa-angle-double-left"></i>
          </button>
        </div>
        <button class="delete-btn">
          <i class="far fa-star" aria-hidden="true"></i>
        </button>
        <button class="delete-btn">
          <i class="far fa-trash-alt" aria-hidden="true"></i>
          <i class="far fa-flag" aria-hidden="true"></i>
        </button>
      </div>-->


      <div class="tm-wrapper">



        <div class="tm-open-message shadow-lg">




          <div class="container ">


            <div class="row">

              <div class="col-lg-8">
                <!--<button type="button" class="close close-mail-body" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>-->



                <div class="tm-mail-content ">

                  <div class="tm-message-info sticky-top">
                    <div class="tm-message-sender-img">
                      <img src="https://images.unsplash.com/photo-1504911539020-cfb0f7887a5e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" id="sender-profile-pic">
                    </div>
                    <div class="message-sender">
                      <h4 class="tm-sender-name" id="sender-name" >Nicole Randall</h4>
                      <h4 class="tm-sender-name" id="" >mattia@nextblu.com</h4>
                    </div>

                    <div class="tm-message-timestamp" id="message-timestamp">
                      <small>2:05 PM</small>
                    </div>

                    <div class="btn-group header-buttons" role="group" aria-label="Mail actions">
                      <button type="button" class="btn btn-light"><i class="fa fa-reply"></i></button>
                      <button type="button" class="btn btn-light"><i class="fa fa-reply-all"></i></button>
                      <button type="button" class="btn btn-light"><i class="fa fa-arrow-right"></i></button>
                    </div>

                  </div>
                  <p class="tm-message-subject" id="message-subject">
                    The best travel destinations
                  </p>
                  <div class="tm-message-content" id="message-content">
                    <p>Hi Chris!</p>
                    <p>
                      Towards the end of every year we look at the year ahead through a cultural lens, with a focus on
                      major events and trends the world - in 2020, for example, the Olympics will take place in Japan.
                    </p>
                    <p>
                      We know about Japan more than all travel agents. We will be happy to share with you all the
                      advantages of this destination:)
                    </p>
                    <div class="tm-image-gallery">
                      <div class="tm-gallery-row">
                        <img src="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=80" alt="">
                        <img src="https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=60" alt="">
                      </div>
                      <div class="tm-gallery-row">
                        <img src="https://images.unsplash.com/photo-1520312501384-dbdb83a1cb11?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60" alt="" class="tm-w-100">
                      </div>
                    </div>
                  </div>

                </div>

                <button type="button" class="btn btn-primary reply-to-message btn-lg "><i class="fa fa-reply"></i>   Reply</button>
                <button type="button" class="btn btn-light forward-message btn-lg"><i class="fa fa-arrow-right"></i>     Forward</button>



              </div>

              <div class="col-lg-4">


                <div class="tm-mail-lateral">
                  <div class="container">
                    <h4>Quick actions</h4>
                    <div class="btn-group header-buttons" role="group" aria-label="Mail actions" style="width: 100%; margin-bottom: 20px">
                      <button type="button" class="btn btn-light"><i class="fa fa-flag"></i>  Flag</button>
                      <button type="button" class="btn btn-light"><i class="fa fa-trash"></i>  Delete</button>
                      <button type="button" class="btn btn-light"><i class="fa fa-ellipsis-h"></i>  Other</button>
                    </div>

                    <div class="tm-attachements">

                      <h4>Attachements</h4>
                      <div class="tm-lateral-image-gallery">
                        <div class="tm-gallery-row">
                          <img src="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=80" alt="">
                          <img src="https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=60" alt="">
                          <img src="https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=60" alt="">
                          <img src="https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=80" alt="">
                          <img src="https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=60" alt="">
                          <img src="https://images.unsplash.com/photo-1524413840807-0c3cb6fa808d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=350&q=60" alt="">

                        </div>
                      </div>

                      <div class="tm-file-summary">
                        <p>6 files <strong>24.8 Mb</strong></p>
                      </div>


                    </div>

                    <div class="tm-people-in-conversation">
                      <h4>People in conversation</h4>
                      <br>

                      <div class="one-match">
                        <div class="one-match-content">
                          <img src="https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80">
                          <div class="match-info">
                            <h4>Mattia</h4>
                            <h5 class="online">Online</h5>
                          </div>
                        </div>
                      </div>
                      <div class="one-match">
                        <div class="one-match-content">
                          <img src="https://images.unsplash.com/photo-1492633423870-43d1cd2775eb?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80">
                          <div class="match-info">
                            <h4>Basic_ph</h4>
                            <h5 class="online">Online</h5>
                          </div>
                        </div>
                      </div>


                    </div>

                    <div class="tm-mail-notes">
                      <h4>Notes</h4> <button type="button" class="btn btn-light tm-text-center">Add a note</button>

                      <div class="postit yellow">
                        <div class="tape">My simple note</div>
                        <div class="widget-content">
                          <p>Now i can insert incredible notes here!</p>
                          <p>What a cool feature!.</p>
                        </div>
                      </div>


                    </div>

                  </div>
                </div>

              </div>


            </div>


          </div>


        </div>



      </div>
    </section>

    <!-- Full screen search -->
    <div id="tm-full_search">
      <button type="button" class="close">×</button>
      <form>
        <input type="search" value="" placeholder="type keyword(s) here" />
        <button type="submit" class="btn btn-primary">Search</button>
      </form>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="composeEmail" tabindex="-1" role="dialog" aria-labelledby="composeEmailLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="composeEmailLabel">New message</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="recipient-name" class="col-form-label">Recipient:</label>
                <input type="text" class="form-control" id="recipient-name">
              </div>
              <div class="form-group">
                <label for="message-text" class="col-form-label">Message:</label>
                <div id="message-text" class="form-control">
                  My message
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary"  data-dismiss="modal">Send message</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="viewProfile" tabindex="-1" role="dialog" aria-labelledby="viewProfileLabel" aria-hidden="true">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewProfileLabel">My profile</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">

            <div class="container emp-profile">
              <form method="post">
                <div class="row">
                  <div class="col-md-4">
                    <div class="tm-profile-img">
                      <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS52y5aInsxSm31CvHOFHWujqUx_wWTS9iM6s7BAm21oEN_RiGoog" alt=""/>
                      <div class="tm-file btn btn-lg btn-primary">
                        Change Photo
                        <input type="file" name="file"/>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-6">
                    <div class="tm-profile-head">
                      <h5>
                        USER NAME HERE
                      </h5>
                      <h6>
                        USER BIO HERE
                      </h6>
                      <p class="tm-proile-rating">Total emails: <span>890</span></p>
                      <ul class="nav nav-tabs" id="myTab" role="tablist">
                        <li class="nav-item">
                          <a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="true">About</a>
                        </li>
                        <li class="nav-item">
                          <a class="nav-link" id="profile-tab" data-toggle="tab" href="#profile" role="tab" aria-controls="profile" aria-selected="false">Password</a>
                        </li>
                      </ul>
                    </div>
                  </div>
                  <div class="col-md-2">
                    <input type="submit" class="tm-profile-edit-btn" name="btnAddMore" value="Edit Profile"/>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-4">
                    <div class="tm-profile-work">
                      <p>PROFILE ACTION / APP ACTION</p>
                      <a href="">Manage apps</a><br/>
                      <a href="">Connect to NextBlu</a><br/>
                      <a href="">Delete profile</a>
                    </div>
                  </div>
                  <div class="col-md-8">
                    <div class="tab-content tm-profile-tab" id="myTabContent">
                      <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                        <div class="row">
                          <div class="col-md-6">
                            <label>User Id</label>
                          </div>
                          <div class="col-md-6">
                            <p>userid546</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Name</label>
                          </div>
                          <div class="col-md-6">
                            <p>Incredible Name</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Email</label>
                          </div>
                          <div class="col-md-6">
                            <p>myname@nextblu.com</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Phone</label>
                          </div>
                          <div class="col-md-6">
                            <p>123 456 7890</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Profession</label>
                          </div>
                          <div class="col-md-6">
                            <p>Mail sender</p>
                          </div>
                        </div>
                      </div>
                      <div class="tab-pane fade" id="profile" role="tabpanel" aria-labelledby="profile-tab">
                        <div class="row">
                          <div class="col-md-6">
                            <label>Experience</label>
                          </div>
                          <div class="col-md-6">
                            <p>Expert</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Hourly Rate</label>
                          </div>
                          <div class="col-md-6">
                            <p>10$/hr</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Total Projects</label>
                          </div>
                          <div class="col-md-6">
                            <p>230</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>English Level</label>
                          </div>
                          <div class="col-md-6">
                            <p>Expert</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-6">
                            <label>Availability</label>
                          </div>
                          <div class="col-md-6">
                            <p>6 months</p>
                          </div>
                        </div>
                        <div class="row">
                          <div class="col-md-12">
                            <label>Your Bio</label><br/>
                            <p>Your detail description</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </form>
            </div>





          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary"  data-dismiss="modal">Save settings</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
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

<style scoped>
  /*@import "../assets/css/main.css";*/
  @import "//cdnjs.cloudflare.com/ajax/libs/animate.css/3.2.0/animate.min.css";
  @import "https://fonts.googleapis.com/css?family=Roboto:300,400&amp;display=swap";
  @import "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css";
  @import "https://cdn.quilljs.com/1.3.6/quill.snow.css";

  /*#home {
    display: grid;
    /*grid-template-rows: 3;*/
    /*grid-template-columns: 400px 1fr !important;
    height: 100vh;
    /*grid-template-columns: 300px 1fr;*/
    /*box-sizing: border-box;
    margin: 0;
    padding: 0;

  }*/

  /* MANUAL INTEGRATION */

  /*@import "../assets/css/app.css";*/


</style>
