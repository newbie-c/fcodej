function showProfile(username, token) {
  let tee = token ? {'x-auth-token': token} : {};
  $.ajax({
    method: 'GET',
    url: '/api/profile',
    data: {
      username: username
    },
    headers: tee,
    success: function(data) {
      console.log(data);
      if (!data.user) {
        let html = Mustache.render($('#ealertt').html(), data);
        $('#main-container').append(html);
        slidePage('#ealert');
      } else {
        if ($('#profile').length) {
          $('#profile').slideUp('slow', function() {
            $('#profile').remove();
            let html = Mustache.render($('#profilet').html(), data);
            $('#main-container').append(html);
            formatDateTime($('#profile .date-field'));
            renderLastSeen($('#profile .last-seen'));
            $('#profile').slideDown('slow');
          });
        } else {
          let html = Mustache.render($('#profilet').html(), data);
          $('#main-container').append(html);
          formatDateTime($('#profile .date-field'));
          renderLastSeen($('#profile .last-seen'));
          slidePage('#profile');
        }
      }
    },
    dataType: 'json'
  });
  let col = $(this).parents('.navbar-collapse');
  if (col.hasClass('in')) col.removeClass('in');
}
