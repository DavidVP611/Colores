$(document).ready(function() {
    // $(document).on("click", ".closeModalNoti", function() {
    //     let modal = $(this).attr("id");
    //     let id =modal.substr(5,modal.length)

    //     $(`#${id}`).addClass("fade")
    //     $(`#${id}`).css("display","none")

    // });

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

    $("#create").click(() => {
        if ($("#take-code").html() == "") {
            let code_id = "<input type='text' name='code-id' id='code-id' placeholder='ID Código' required>";
            let code_name = "<input type='text' name='code-name' id='code-name' placeholder='Nombre del código'>";
            let code_quantity = "<input type='text' name='code-quantity' id='code-quantity' placeholder='Cantidad del color'>";

            $("#take-code").html(`${code_id} ${code_name} ${code_quantity}`);
            $("#create").after("<span id='close_create'>[ X ]</span>");
        } else if (($("#code-id").val()).length > 0 ) {
            $("#create").attr("type","submit");
        }
    });

    $(document).on("click", "#close_create", () => {
        $("#take-code").html("");
        $("#close_create").remove();
    });    
})