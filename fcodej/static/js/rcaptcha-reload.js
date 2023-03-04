function rcaptchaReload() {
  $(this).blur();
  $.ajax({
    method: 'GET',
    url: '/api/captcha',
    success: function(data) {
      $('#rcaptcha-field')
        .attr({"style": 'background:url(' + data.url +')'});
      $('#rsuffix').val(data.captcha);
      $('#rcaptcha').focus();
    },
    dataType: 'json'
  });
}
