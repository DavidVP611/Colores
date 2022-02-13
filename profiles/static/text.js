$(document).ready(function() {    
    $("#text_container").on("submit", function(event) {
        event.preventDefault();
        $(".readed").html("");
        let formulario = new FormData(this);
        // let formulario = $("#imagen_container").serial ize()
        $.ajax({
            type: "POST",
            url: '/read_text/',
            data: formulario,
            processData: false,
            contentType: false,
            complete: function(dato) {
                if (dato.responseJSON) {
                    $.each(dato.responseJSON, (num, val) => {
                        $(".readed").append(`<p><b>${val}</b></p>`);
                    })   
                }
                console.log(dato.responseJSON);
            }
        })
    });
})