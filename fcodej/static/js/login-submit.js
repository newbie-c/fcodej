function loginSubmit(event) {
  $(this).blur();
  let tee = {
    login: $('#logininput').val(),
    passwd: $('#password').val(),
    rme: $('#remember_me').is(':checked') ? 1 : 0,
    cache: $('#lsuffix').val(),
    captcha: $('#lcaptcha').val(),
    token: event.data.token
  };
  if (tee.login && tee.passwd && tee.captcha && tee.cache) {
    $.ajax({
      method: 'POST',
      url: '/api/login',
      data: tee,
      success: function(data) {
        if (data.token) {
          window.localStorage.setItem('token', data.token);
        }
        $('.navbar-brand')[0].click();
      },
      dataType: 'json'
    });
  }
}
