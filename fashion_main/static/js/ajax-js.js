$(document).on('submit', '#save_setting_form', function(e) {
  e.preventDefault();
  // var business = $('#id_business').val();
  var site_title = $('#id_site_title').val();
  var site_logo = $('#id_site_logo').val();
  var copyright = $('#id_copyright').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    type: 'POST',
    url: '/business/site-settings/',
    data: {
      // business : business,
      site_title: site_title,
      site_logo: site_logo,
      copyright: copyright,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      // $('#site_settings').addClass('alert alert-success alert-dismissible fade show');
      // $("#site_settings").html(data);
      alert(data);
    },
    error: function(data) {
      alert(data);
    }
  });
});


function updCart(id) {

  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()
  var form = $('#qtyForm' + id)
  alert(csrfmiddlewaretoken)

  $.ajax({
    url: '/cart/add_cart_ajax/' + id + '/',
    type: 'POST',
    data: {
      form: form,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },
    success: function(data) {
      alert(data);
    },
  });
}


// Newsletters
$(document).on('submit', '#newsletterForm', function(e) {
  e.preventDefault();
  var email = $('#email').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val();
  var url = $('#url').val();
  
  $.ajax({
    url: url,
    type: "POST",
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


//Created / Generates the captcha function
function DrawCaptcha()
{
   var a = Math.ceil(Math.random() * 9)+ '';
   var b = Math.ceil(Math.random() * 9)+ '';
   var c = Math.ceil(Math.random() * 9)+ '';
   var d = Math.ceil(Math.random() * 9)+ '';
   var code = a + ' ' + b + ' ' + ' ' + c + ' ' + d;
   document.getElementById("txtCaptcha").value = code
}

// Validate the Entered input aganist the generated security code function
function ValidCaptcha(){
   var str1 = removeSpaces(document.getElementById('txtCaptcha').value);
   var str2 = removeSpaces(document.getElementById('txtInput').value);

   if (str1 == str2)
   {
    $("#invalidCode").html('');
    $("#blankCaptchaError").html('');
     // pass
   }
   else if(str2 == ''){
    $("#invalidCode").html('');
    $("#blankCaptchaError").html('Please enter Captcha!');
    return false;
   }
   else{
     $("#blankCaptchaError").html('');
     $("#invalidCode").html('Invalid verification code. Please enter the correct code to be able to submit.');
    
     DrawCaptcha();
     return false;
   }
}


// Captcha verification inquiry
function DrawCaptchaInq()
{
   var a = Math.ceil(Math.random() * 9)+ '';
   var b = Math.ceil(Math.random() * 9)+ '';
   var c = Math.ceil(Math.random() * 9)+ '';
   var d = Math.ceil(Math.random() * 9)+ '';
   var code = a + ' ' + b + ' ' + ' ' + c + ' ' + d;
   document.getElementById("txtCaptchaInq").value = code
}

// Validate the Entered input aganist the generated security code function
function ValidCaptchaInq(){
   var str1 = removeSpaces(document.getElementById('txtCaptchaInq').value);
   var str2 = removeSpaces(document.getElementById('txtInputInq').value);

   if (str1 == str2)
   {
    $("#invalidCodeInq").html('');
    $("#blankCaptchaErrorInq").html('');
     // pass
   }
   else if(str2 == ''){
    $("#invalidCodeInq").html('');
    $("#blankCaptchaErrorInq").html('Please enter Captcha!');
    return false;
   }
   else{
     $("#blankCaptchaErrorInq").html('');
     $("#invalidCodeInq").html('Invalid verification code. Please enter the correct code to be able to submit.');
    
     DrawCaptchaInq();
     return false;
   }
}


// Captcha verification rating
function DrawCaptchaRating()
{
   var a = Math.ceil(Math.random() * 9)+ '';
   var b = Math.ceil(Math.random() * 9)+ '';
   var c = Math.ceil(Math.random() * 9)+ '';
   var d = Math.ceil(Math.random() * 9)+ '';
   var code = a + ' ' + b + ' ' + ' ' + c + ' ' + d;
   document.getElementById("txtCaptchaRating").value = code
}

// Validate the Entered input aganist the generated security code function
function ValidCaptchaRating(){
   var str1 = removeSpaces(document.getElementById('txtCaptchaRating').value);
   var str2 = removeSpaces(document.getElementById('txtInputRating').value);

   if (str1 == str2)
   {
    $("#invalidCodeRating").html('');
    $("#blankCaptchaErrorRating").html('');
     // pass
   }
   else if(str2 == ''){
    $("#invalidCodeRating").html('');
    $("#blankCaptchaErrorRating").html('Please enter Captcha!');
    return false;
   }
   else{
     $("#blankCaptchaErrorRating").html('');
     $("#invalidCodeRating").html('Invalid verification code. Please enter the correct code to be able to submit.');
    
     DrawCaptchaRating();
     return false;
   }
}


// Remove the spaces from the entered and generated code
function removeSpaces(string)
{
   return string.split(' ').join('');
}





// Send an inquiry
$(document).on('submit', '#inquiry-modal', function(e) {
  e.preventDefault();
  $("#submit").val('Please wait...');
  var business_id = $('#business_id').val();
  var user_id = $('#user_id').val();
  var product_id = $('#product_id').val();
  var product_name = $('#product_name').val();
  var first_name = $('#first_name').val();
  var last_name = $('#last_name').val();
  var email = $('#email').val();
  var phone = $('#phone').val();
  var inq_message = $('#inq_message').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()
  var url = $('#url').val();

  $.ajax({
    method: 'POST',
    url: url,
    data: {
      business_id: business_id,
      user_id: user_id,
      product_id: product_id,
      product_name: product_name,
      first_name: first_name,
      last_name: last_name,
      email: email,
      phone: phone,
      inq_message: inq_message,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      if (data == 'already-inquired') {
        $('#inquiry_success').addClass('alert alert-warning alert-dismissible fade show');
        $("#inquiry_success").html('You have already made an inquiry about this product. Please wait until we get back to you.');
        $("#submit").val('Send Inquiry');
        $("#submit").attr("disabled", true);
      } else {
        $('#inquiry_success').addClass('alert alert-success alert-dismissible fade show');
        $("#inquiry_success").html(data);
        $("#submit").val('Sent');
        $("#submit").attr("disabled", true);
        $('#inquiry_success').delay(4000).fadeOut('slow');
      }
    },
    error: function(data) {
      $('#inquiry_success').addClass('alert alert-danger alert-dismissible fade show');
      $("#inquiry_success").html("Something went wrong, please try again.");

    }
  });
  this.reset();
});


// Contact Form
$(document).on('submit', '#contact_form', function(e) {
  e.preventDefault();
  $("#submit").val('Please wait...');
  var business_id = $('#business_id').val();
  var user_id = $('#user_id').val();
  var name = $('#name').val();
  var email = $('#email').val();
  var phone = $('#phone').val();
  var subject = $('#subject').val();
  var contact_message = $('#contact_message').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()


  $.ajax({
    type: 'POST',
    url: '/contact/',
    data: {
      business_id: business_id,
      user_id: user_id,
      name: name,
      email: email,
      phone: phone,
      subject: subject,
      contact_message: contact_message,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      if (data == 'otp sent') {
        $('.otp_form').slideDown();
        $('#contactMessage').addClass('alert alert-success');
        $("#contactMessage").html('OTP has been sent to your email address. Please verify it.');
        $("#submit").val('Verification Required');
        $('#contactMessage').delay(4000).fadeOut('slow');
        // return count_down_otp();
      }
    },
    error: function(data) {
      $('#contactMessage').addClass('alert alert-danger');
      $("#contactMessage").html("Something went wrong, please try again.");
    }
  });
  this.reset();
});



// Contact OTP Form
$(document).on('submit', '#contact_otp_form', function(e) {
  e.preventDefault();
  $("#otpsubmit").val('Verifying...');
  var otp = $('#otp').val();
  var csrfmiddlewaretoken = $('input[name=csrfmiddlewaretoken]').val()

  $.ajax({
    type: 'POST',
    url: '/verify_otp/',
    data: {
      otp: otp,
      csrfmiddlewaretoken: csrfmiddlewaretoken,
    },

    success: function(data) {
      if (data == 'verified') {
        $('#OTPsuccess').addClass('alert alert-success');
        $("#OTPsuccess").html('OTP Verified. Your message has been submitted successfully.');
        $("#otpsubmit").val('OTP Verified');
        $("#otpsubmit").css("backgroundColor", "green");
        $("#otpsubmit").prop('disabled', true);
        $("#resendotp").css("display", "none");
        $('#OTPsuccess').delay(7000).fadeOut('slow');
      } else if (data == 'wrong-otp') {
        $('#OTPfailed').addClass('alert alert-danger');
        $("#OTPfailed").html('Invalid OTP');
        $("#otpsubmit").val('Verify');
        $('#OTPfailed').delay(5000).fadeOut('slow');
      }
      else{
        alert(data);
        $("#otpsubmit").val('Verify');
      }
    },
    error: function(data) {
      $('#OTPmessage').addClass('alert alert-danger');
      $("#OTPmessage").html("Something went wrong, please try again.");
    }
  });
  this.reset();
});


function resendOTP(){
  // $("#countdown").css("display", "none");
  document.getElementById("resendotp").innerHTML = "Please wait...";
  $.ajax({
    type: 'GET',
    url: '/resend_otp/',
    data: {
      // otp: 'resend-otp',
    },

    success: function(data) {
      if (data == 'otp sent') {
        document.getElementById("resendotp").innerHTML = "Resend OTP";
        $('#contactMessage').addClass('alert alert-success');
        alert('OTP has been sent to your email address. Please verify it.');
        $("#submit").val('Verification Required');
      }
      else{
        document.getElementById("resendotp").innerHTML = "Resend OTP";
        alert(data);
      }
    },
    error: function(data) {
      document.getElementById("resendotp").innerHTML = "Resend OTP";
      $('#OTPmessage').addClass('alert alert-danger');
      $("#OTPmessage").html("Something went wrong, please try again.");
    }
  });

}


// function count_down_otp(){
//   var timeleft = 90;
//   var downloadTimer = setInterval(function(){
//     if(timeleft <= 0){
//       clearInterval(downloadTimer);
//       document.getElementById("countdown").innerHTML = "Your OTP has been expired.";
//       $("#countdown").css("color", "red");
//     } else {
//       document.getElementById("countdown").innerHTML =  "Your OTP will be expired in <b>" + timeleft + "</b> seconds.";
//     }
//     timeleft -= 1;
//   }, 1000);
// }



$('#id_state').change(function(){
    var state_id = $(this).val();
    var url = "/fetchTax/taxByState/"
$.ajax({
    type: "GET",
    url: url,
    data: {
      state_id: state_id,
      dataType: "json",
    },
    success: function( data ) {
        document.getElementById("tax_percent").innerHTML = data.tax_percent;
        document.getElementById("tax_amount").innerHTML = data.tx_amount;
        document.getElementById("grand_total").innerHTML = data.grand_total;
        document.getElementById("grand_total_hidden").value = data.grand_total;
        document.getElementById("tax_hidden").value = data.tx_amount;
    }
});
});
document.getElementById('id_country').required = true
document.getElementById('id_state').required = true


function saveDDPayment(){
  var url = $('#url').val();
  var paymentData = new FormData();
  paymentData.append('amount', $("#id_amount").val());
  paymentData.append('payment_id', $("#id_payment_id").val());
  paymentData.append('date_of_payment', $("#id_date_of_dd_payment").val());
  paymentData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
  paymentData.append('img', $("#is_dd_attachment")[0].files[0]);
  
  
  $.ajax({
    url: url,
    type:"post",
    cache : false,
    contentType : false,
    processType : false,
    data: paymentData,
    success: function(data) {
      alert(data);
      return false;
    }
});
  
}


// B L O G  R E P L Y  C A P T C H A
function DrawReplyCaptcha(comment_id)
{
   var a = Math.ceil(Math.random() * 9)+ '';
   var b = Math.ceil(Math.random() * 9)+ '';
   var c = Math.ceil(Math.random() * 9)+ '';
   var d = Math.ceil(Math.random() * 9)+ '';
   var code = a + ' ' + b + ' ' + ' ' + c + ' ' + d;
   txtCaptchaReply = 'txtCaptchaReply'+comment_id
   document.getElementById(txtCaptchaReply).value = code
}

// Validate the Entered input aganist the generated security code function
function ValidCaptchaReply(comment_id){
   txtCaptchaReply = 'txtCaptchaReply'+comment_id
   txtInputReply = 'txtInputReply'+comment_id
   var str1 = removeSpaces(document.getElementById(txtCaptchaReply).value);
   var str2 = removeSpaces(document.getElementById(txtInputReply).value);

   var invalidCode_r = '#invalidCode_r'+comment_id
   var blankCaptchaError_r = '#blankCaptchaError_r'+comment_id
   if (str1 == str2)
   {
    $(invalidCode_r).html('');
    $(blankCaptchaError_r).html('');
     // pass
   }
   else if(str2 == ''){
    $(invalidCode_r).html('');
    $(blankCaptchaError_r).html('Please enter Captcha!');
    return false;
   }
   else{
     $(invalidCode_r).html('');
     $(blankCaptchaError_r).html('Invalid verification code. Please enter the correct code to be able to submit.');
    
     DrawReplyCaptcha(comment_id);
     return false;
   }
}



// Captcha verification contact
function DrawCaptchaContact()
{
   var a = Math.ceil(Math.random() * 9)+ '';
   var b = Math.ceil(Math.random() * 9)+ '';
   var c = Math.ceil(Math.random() * 9)+ '';
   var d = Math.ceil(Math.random() * 9)+ '';
   var code = a + ' ' + b + ' ' + ' ' + c + ' ' + d;
   document.getElementById("txtCaptchaContact").value = code
}

// Validate the Entered input aganist the generated security code function
function ValidCaptchaContact(){
   var str1 = removeSpaces(document.getElementById('txtCaptchaContact').value);
   var str2 = removeSpaces(document.getElementById('txtInputContact').value);

   if (str1 == str2)
   {
    $("#invalidCodeContact").html('');
    $("#blankCaptchaErrorContact").html('');
     // pass
   }
   else if(str2 == ''){
    $("#invalidCodeContact").html('');
    $("#blankCaptchaErrorContact").html('Please enter Captcha!');
    return false;
   }
   else{
     $("#blankCaptchaErrorContact").html('');
     $("#invalidCodeContact").html('Invalid verification code. Please enter the correct code to be able to submit.');
    
     DrawCaptchaContact();
     return false;
   }
}
