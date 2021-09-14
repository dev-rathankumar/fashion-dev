// Regional Manager Change Password Form
$(document).on('submit', '#changePassword', function(e) {
  e.preventDefault();
  document.getElementById("submit").innerHTML = "Please wait...";
  var current_password = $('#current_password').val();
  var password = $('#password').val();
  var confirm_password = $('#confirm_password').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()


  $.ajax({
    type: 'POST',
    url: '/regional_managers/changePassword/',
    data: {
      current_password: current_password,
      password: password,
      confirm_password: confirm_password,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      if (data == 'success') {
        document.getElementById("submit").innerHTML = "Change";
        $('#result').delay(10000).fadeOut('slow');
        $(location).attr('href', '/userLogin/')
      }
      else{
        $('#result').addClass('alert alert-danger');
        $("#result").html(data);
        document.getElementById("submit").innerHTML = "Change";
        $('#result').delay(5000).fadeOut('slow');
      }
    },
    error: function(data) {
      $('#result').addClass('alert alert-danger');
      $("#result").html(data);
      document.getElementById("submit").innerHTML = "Change";
      $('#result').delay(5000).fadeOut('slow');
    }
  });
  this.reset();
});


// Business Account Change Password Form
$(document).on('submit', '#biz_changePassword', function(e) {
  e.preventDefault();
  document.getElementById("submit").innerHTML = "Please wait...";
  var current_password = $('#current_password').val();
  var password = $('#password').val();
  var confirm_password = $('#confirm_password').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()


  $.ajax({
    type: 'POST',
    url: '/business/changePassword/',
    data: {
      current_password: current_password,
      password: password,
      confirm_password: confirm_password,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      if (data == 'success') {
        document.getElementById("submit").innerHTML = "Change";
        $('#result').delay(10000).fadeOut('slow');
        $(location).attr('href', 'userLogin')
      }
      else{
        $('#result').addClass('alert alert-danger');
        $("#result").html(data);
        document.getElementById("submit").innerHTML = "Change";
        $('#result').delay(5000).fadeOut('slow');
      }
    },
    error: function(data) {
      $('#result').addClass('alert alert-danger');
      $("#result").html(data);
      document.getElementById("submit").innerHTML = "Change";
      $('#result').delay(5000).fadeOut('slow');
    }
  });
  this.reset();
});



// Ordered Products
$(document).on('submit', '#ordered_products_form', function(e) {
  e.preventDefault();
  var order_number = $('#order_number').val();
  console.log(order_number);
  exit();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    type: 'POST',
    url: '/subscribe/',
    data: {
      email: email,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      // $('#site_settings').addClass('alert alert-success alert-dismissible fade show');
      $("#subscriptionMessage").html(data);
    },
    error: function(data) {
      $("#subscriptionMessage").html("Something went wrong, please try again.");
    }
  });
});

function goBack() {
  window.history.back();
}


// Approval Switch
function approvalSwitch(rating_id) {
  var approvalSwitch = 'approvalSwitch-' + rating_id;
  var approvalSwitch = document.getElementById(approvalSwitch);
  var status = document.getElementById("status");
  // var id =

  if (approvalSwitch.checked == true){
    var event = Boolean(true);
    toggleApproval(event, rating_id);
    // status.style.display = "block";
  } else {
    var event = Boolean(false);
    toggleApproval(event, rating_id);
     // status.style.display = "none";
  }
}


function toggleApproval(event, rating_id){
  $.ajax({
    type: 'GET',
    url: '/business/review-ratings/toggleApproval/'+rating_id,
    data: {
      event:event,
    },

    success: function(data) {
      if (data == 'true') {
        var reviewstatus = 'reviewstatus-'+rating_id;
        document.getElementById(reviewstatus).innerHTML = "Approved";
      }
      else{
        var reviewstatus = 'reviewstatus-'+rating_id;
        document.getElementById(reviewstatus).innerHTML = "Pending";
      }
    },
    error: function(data) {
      alert(data)
    }
  });
}


// Topbar Switch
function topbarSwitch() {
  var topbarSwitch = document.getElementById('topbarSwitch');

  var status = document.getElementById("status");

  if (topbarSwitch.checked == true){
    var event = Boolean(true);
    topbarToggleEnable(event);
    document.getElementById("topbarForm").style.display = "block";
  } else {
    var event = Boolean(false);
    topbarToggleEnable(event);
    document.getElementById("topbarForm").style.display = "none";
  }
}

function topbarToggleEnable(event){
  $.ajax({
    type: 'GET',
    url: '/business/site_settings/topbarEdit/topbarToggleEnable/',
    data: {
      event:event,
    },

    success: function(data) {
      if (data == 'enabled') {
        document.getElementById('topbarStatus').innerHTML = "Enabled";
      }
      else{
        document.getElementById('topbarStatus').innerHTML = "Disabled";
      }
    },
    error: function(data) {
      alert(data)
    }
  });
}




// $(document).on('submit', '#add_more_about1', function(e) {
//   e.preventDefault();
//   var url = $('#url').val();
//   var formData = new FormData(this);
//   $.ajax({
//       type: 'POST',
//       url: url,
//       data: formData,
//       processData: false,
//       contentType: false,
//       success: function (response) {
//         alert(response.msg)
//       },

//   });
// });


// Approval Swtich
function approvalSwitch(comment_id) {
  var approvalSwitch = 'approvalSwitch-' + comment_id;
  var approvalSwitch = document.getElementById(approvalSwitch);

  if (approvalSwitch.checked == true){
    var event = Boolean(true);
    commentApproval(event, comment_id);
  } else {
    var event = Boolean(false);
    commentApproval(event, comment_id);
  }
}

function commentApproval(event, comment_id){
  $.ajax({
    type: 'GET',
    url: '/business/blogs/comments/commentApproval/'+comment_id,
    data: {
      event:event,
    },
    success: function(data) {
      if (data == 'true') {
        var commentstatus = 'commentstatus-'+comment_id;
        document.getElementById(commentstatus).innerHTML = "Approved";
      }
      else{
        var commentstatus = 'commentstatus-'+comment_id;
        document.getElementById(commentstatus).innerHTML = "Pending";
      }
    },
    error: function(data) {
      alert(data)
    }
  });
}


// Direct Deposit Switch
function ddSwitch() {
  var ddSwitch = document.getElementById('ddSwitch');
  var url = $('#ddurl').val();
  if (ddSwitch.checked == true){
    var event = Boolean(true);
    ddToggleEnable(event, url);
    document.getElementById("ddForm").style.display = "block";
  } else {
    var event = Boolean(false);
    ddToggleEnable(event, url);
    document.getElementById("ddForm").style.display = "none";
  }
}

function ddToggleEnable(event, url){
  $.ajax({
    type: 'GET',
    url: url,
    data: {
      event:event,
    },

    success: function(data) {
      if (data == 'enabled') {
        document.getElementById('ddStatus').innerHTML = "Enabled";
      }
      else{
        document.getElementById('ddStatus').innerHTML = "Disabled";
      }
    },
    error: function(data) {
      alert(data)
    }
  });
}


// PayPal Config Switch
function ppSwitch() {
  var ppSwitch = document.getElementById('ppSwitch');
  var url = $('#ppurl').val();
  if (ppSwitch.checked == true){
    var event = Boolean(true);
    ppToggleEnable(event, url);
    document.getElementById("ppForm").style.display = "block";
  } else {
    var event = Boolean(false);
    ppToggleEnable(event, url);
    document.getElementById("ppForm").style.display = "none";
  }
}

function ppToggleEnable(event, url){
  $.ajax({
    type: 'GET',
    url: url,
    data: {
      event:event,
    },

    success: function(data) {
      if (data == 'enabled') {
        
        document.getElementById('ppStatus').innerHTML = "Enabled";
      }
      else{
        document.getElementById('ppStatus').innerHTML = "Disabled";
      }
    },
    error: function(data) {
      alert(data)
    }
  });
}