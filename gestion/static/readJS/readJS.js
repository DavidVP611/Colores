$(document).ready(function() {

    const csrftoken =  window.CSRF_TOKEN;
    let tic = false;
    $("#read").click(()=> {
        $("#read").html( "Lectura de códigos activada");
        if (tic == false) {
            tic = true;
            $(".mark_error").remove();
           $.ajax({
                type: "POST",
                url : '/readQR/',
                data: {'action': tic, csrfmiddlewaretoken: csrftoken},
                complete: function(dato) {
                    console.log(dato.responseJSON)
                    if (dato.responseJSON) {
                        $(".div").after("<div class='mark_error'></div>");
                        $.each(dato.responseJSON, (num, val) => {
                            $(".mark_error").append(`<p><b>${val.title}</b><span style='display:block'>${val.body}</span></p>`);
                        })
                    }                
                    $("#read").html("Leer códigos");
                    tic = false;
                }
            })
        }       
    });
})