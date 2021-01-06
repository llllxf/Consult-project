var $messages = $('.map-content-9'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    //fakeMessage();
  }, 100);
});





function insertMessage() {
  msg = $('.message').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message').val(null);

	interact(msg);
  setTimeout(function() {

  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
})


function interact(message){
	// loading message
  $('<div class="message loading new"><figure class="avatar"><img src="/static/res/easybot.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
	// make a POST request [ajax call]
	$.post('/message', {
		msg: message,
	}).done(function(reply) {
		// Message Received
		// 	remove loading meassage
    $('.message.loading').remove();
		// Add message to chatbox
    $('<div class="message new"><figure class="avatar"><img src="/static/res/easybot.png" /></figure>' + reply['text'] + '</div>').appendTo($('.mCSB_container')).addClass('new');
    setDate();
    updateScrollbar();

		}).fail(function() {
				alert('error calling function');
				});
}
