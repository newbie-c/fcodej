function logOut(event) {
  let tee = {token: event.data.token};
  $.ajax({
    method: 'POST',
    url: '/api/logout',
    data: tee,
    success: function(data) {
      if (data.result) {
        window.localStorage.removeItem('token');
        $('.navbar-brand')[0].click();
      }
    },
    dataType: 'json'
  });
}
