
(function (){
    const btnComprarLibros = document.querySelectorAll('.btnComprarLibro')
    let isbnLibroSeleccionado=null
    btnComprarLibros.forEach((btn)=>{
        btn.addEventListener('click',function(){
            isbnLibroSeleccionado=this.id
            confirmarCompra()
    })
})

const confirmarCompra = () => {
    Swal.fire({
        title: '¿Confirma la compra del libro seleccionado?',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Comprar',
        showLoaderOnConfirm: true,
        preConfirm: async () => {
            // console.log(window.origin);
            return await fetch(`${window.origin}/comprarLibro`, {
                method: 'POST',
                mode: 'same-origin',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    
                },
                body: JSON.stringify({
                    'isbn': isbnLibroSeleccionado
                })
            }).then(response => {
                if (!response.ok) {
                    notificacionSwal('Error', response.statusText, 'error', 'Cerrar');
                }
                return response.json();
            }).then(data => {
                if (data.exito) {
                    notificacionSwal('¡Éxito!', 'Libro Comprado', 'success', '¡Ok!');
                } else {
                    notificacionSwal('¡Alerta!', data.mensaje, 'warning', 'Ok');
                }
            }).catch(error => {
                notificacionSwal('Error', error, 'error', 'Cerrar');
            });
        },
        allowOutsideClick: () => false,
        allowEscapeKey: () => false
    });
};

})();
 