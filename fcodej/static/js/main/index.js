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
  }
  $(window).bind('hashchange', function() {
    let crt = parseHash(window.location.hash, '#create-password');
    if (crt) window.location.reload();
    let rst = parseHash(window.location.hash, '#reset-password');
    if (rst) window.location.reload();
  });
  let crt = parseHash(window.location.hash, '#create-password');
  if (crt) createPassword(crt, token);
  let rst = parseHash(window.location.hash, '#reset-password');
  if (rst) resetPassword(rst, token);
});
