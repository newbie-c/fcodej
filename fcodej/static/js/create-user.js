function createUser() {
  $(this).blur();
  console.log('yep');
  let tee = {
    username: $('#username').val(),
    passwd: $('#crpassword').val(),
    confirma: $('#confirmation').val(),
    aid: $(this).data().aid
  };
  if (tee.username && tee.passwd && tee.confirma && tee.aid) {
    console.log(tee);
    $.ajax({
      method: 'POST',
      url: '/api/create-password',
      data: tee,
      success: function(data) {
        if (data.done) {
          $('.navbar-brand')[0].click();
        } else {
          let html = Mustache.render($('#ealertt').html(), data);
          $('#ealert').remove();
          $('#crpf').before(html);
          $('#ealert').slideDown('slow', function() {
            $('#crpf').addClass('next-block');
          });
        }
      },
      dataType: 'json'
    });
  }
}
