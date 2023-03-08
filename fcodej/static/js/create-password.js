function createPassword(token, auth) {
  $.ajax({
    method: 'GET',
    url: '/api/create-password',
    headers: {
      'x-reg-token': token,
      'x-auth-token': auth
    },
    success: function(data) {
      if (data.cu) {
        let html = '<div id="ealert" ' +
                     '   class="alert alert-danger to-be-hidden"</div>' +
                     '  Вы авторизованы, действие невозможно, ' +
                     '  нужно выйти повторить переход по ссылке.' +
                     '</div>';
        $('#main-container').append(html);
        $('#ealert').siblings().each(function() {
          $(this).slideUp('slow', function() { $(this).remove(); });
        });
        $('#ealert').slideDown('slow');
      } else {
        if (!data.aid) {
          let html = '<div id="ealert" ' +
                     '     class="alert alert-danger to-be-hidden"</div>' +
                     data.message +
                     '</div>';
          $('#main-container').append(html);
          $('#ealert').siblings().each(function() {
            $(this).slideUp('slow', function() { $(this).remove(); });
          });
          $('#ealert').slideDown('slow');
        } else {
          let html = Mustache.render($('#crpt').html(), data);
          $('#main-container').append(html);
          $('#crpf').siblings().each(function() {
            $(this).slideUp('slow', function() { $(this).remove(); });
          });
          $('#crpf').slideDown('slow');
        }
      }
    },
    dataType: 'json'
  });
}
