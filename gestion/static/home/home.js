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
        if (tic == true) {
            tic = false;
           let message = "Pausar lectura";
        } else {
            tic = true;
            let message = "Leer códigos";
        }
        $.ajax({
            type: "POST",
            url : '/readQR/',
            data: {'action': tic, csrfmiddlewaretoken: csrftoken},

            success: function(dato) {
                $("#read").html(message);
                $(".data").html(`El dato: ${dato}`);
            }
        })
    });

    $("#create").click(() => {
        if ($("#take-code").html() == "") {
            let code_id = "<input type='text' name='code-id' id='code-id' placeholder='ID Código' required>"
            let code_name = "<input type='text' name='code-name' id='code-name' placeholder='Nombre del código' required>"
            let code_quantity = "<input type='text' name='code-quantity' id='code-quantity' placeholder='Cantidad del color' required>"
            $("#take-code").html(`${code_id} ${code_name} ${code_quantity}`);
        } else {
            $("#create").attr("type","submit");
        }
    })
})