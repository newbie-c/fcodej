function regSubmit(event) {
  $(this).blur();
  let tee = {
    address: $('#raddress').val(),
    cache: $('#rsuffix').val(),
    captcha: $('#rcaptcha').val(),
    token: event.data.token
  };
  if (tee.address && tee.cache && tee.captcha) {
    $.ajax({
      method: 'POST',
      url: '/api/get-password',
      data: tee,
      success: function(data) {
        $('.navbar-brand')[0].click();
      },
      dataType: 'json'
    });
  }
}
