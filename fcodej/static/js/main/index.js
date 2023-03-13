$(function() {
  let token = showWindow();
  if (token) {
    $('body').on('click', '#logout', {'token': token}, logOut);
  } else {
    $('body').on('click', '#rcaptcha-reload', rcaptchaReload);
    $('body').on('click', '#lcaptcha-reload', lcaptchaReload);
    $('body').on('click', '#login-submit', {token: token}, loginSubmit);
    $('body').on('click', '#reg-submit', {token: token }, regSubmit);
    $('body').on('click', '#login-reg', loginReg);
    $('body').on('click', '#reg', reg);
    $('body').on('click', '#login', login);
    $('body').on('click', '#crp-submit', createUser);
    $('body').on('click', '#rsp-submit', restorePassword);
  }
  $(window).bind('hashchange', {token: token}, function(event) {
    let crt = parseHash(window.location.hash, '#create-password');
    if (crt) {
      createPassword(crt, event.data.token);
    }
    let rst = parseHash(window.location.hash, '#reset-password');
    if (rst) {
      resetPassword(rst, event.data.token);
    }
    let prof = parseHash(window.location.hash, '#profile');
    if (prof) {
      showProfile(prof, event.data.token);
    }
  });
  let crt = parseHash(window.location.hash, '#create-password');
  if (crt) {
    createPassword(crt, token);
  }
  let rst = parseHash(window.location.hash, '#reset-password');
  if (rst) {
    resetPassword(rst, token);
  }
  let prof = parseHash(window.location.hash, '#profile');
  if (prof) {
    showProfile(prof, token);
  }
});
