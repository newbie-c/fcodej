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
        let html = Mustache.render($('#ealertt').html(), data);
        $('#main-container').append(html);
        slidePage('#ealert');
      } else {
        if (!data.aid) {
          let html = Mustache.render($('#ealertt').html(), data);
          $('#main-container').append(html);
          slidePage('#ealert');
        } else {
          let html = Mustache.render($('#crpt').html(), data);
          $('#main-container').append(html);
          slidePage('#crpf');
        }
      }
    },
    dataType: 'json'
  });
}
