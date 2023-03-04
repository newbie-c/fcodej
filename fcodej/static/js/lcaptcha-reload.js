function lcaptchaReload() {
  $(this).blur();
  $.ajax({
    method: 'GET',
    url: '/api/captcha',
    success: function(data) {
      $('#lcaptcha-field')
        .attr({"style": 'background:url(' + data.url +')'});
      $('#lsuffix').val(data.captcha);
      $('#lcaptcha').focus();
    },
    dataType: 'json'
  });
}
