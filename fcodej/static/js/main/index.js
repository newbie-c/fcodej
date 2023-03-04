$(function() {
  let token = showWindow();
  if (token) {
    $('body').on('click', '#logout', {'token': token}, logOut);
  } else {
    $('body').on('click', '#rcaptcha-reload', rcaptchaReload);
    $('body').on('click', '#lcaptcha-reload', lcaptchaReload);
    $('body').on('click', '#login-submit', {token: token}, loginSubmit);
    $('body').on('click', '#login-reg', loginReg);
    $('body').on('click', '#reg', reg);
    $('body').on('click', '#login', login);
  }
});
