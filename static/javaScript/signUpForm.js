$(document).ready(function() {
    $('#form').on('submit', function(event) {
		$.ajax({
			data : {
				userID : $('#userID').val(),
			},
			type : 'POST',
			url : '/createuser',
            success: function(response){
			    alert(response);
			    $("#titlebox").text(response);
            }
		});
		event.preventDefault(); // HTML automatically tries to post the form, we therefore manually stop this
		// $("html").load("/view");
	});
});