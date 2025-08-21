
	$(document).ready(function(){
        $('#login_form').submit(function(e){
            e.preventDefault()
            debugger
            var username = $('#id_username').val()
            var password = $('#id_password').val()
            if (username && password){
            $.ajax({
                url:"loginview/",
                type:'POST',
                data:{
                    'username':username,
                    'password':password,
                    csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                },
                success:function(response){
                    console.log(response.message)
                    if (response.status == '200 OK' && response.message=='Login Successfully'){
                        swal(response.message, {
                            buttons: {
                                confirm: {
                                className: "btn btn-success",
                                },
                            },
                            });

                            window.location.href = "/home/";
                        }
                    },
					error: function(xhr) {
                        let response = xhr.responseJSON || {message: 'An error occurred'};
                        swal(response.message, {
                            buttons: {
                                confirm: {
                                className: "btn btn-danger",
                                },
                            },
                            });
                        if (response.attempts && response.attempts >= 3) {
                            setTimeout(() => {
                                window.location.href = "{% url 'url_403' %}";
                            }, 2000);
                        }
                    }
            });
            }else{swal("Enter your username and password!!!", {
              buttons: {
                confirm: {
                  className: "btn btn-danger",
                },
              },
            });}
        });
     });


