let carrito = JSON.parse(
    localStorage.getItem("carrito")
) || [];

document.addEventListener("DOMContentLoaded", () => {

    actualizarCarrito();

});

function obtenerElementos() {

    return {

        contador: document.getElementById(
            "contador-carrito"
        ),

        listaCarrito: document.getElementById(
            "lista-carrito"
        ),

        totalCarrito: document.getElementById(
            "total-carrito"
        )

    };

}

function agregarAlCarrito(id) {

    const producto = productos.find(
        p => p.id === id
    );

    if (!producto) return;

    carrito.push(producto);

    guardarCarrito();

    actualizarCarrito();

}

function guardarCarrito() {

    localStorage.setItem(
        "carrito",
        JSON.stringify(carrito)
    );

}

function actualizarCarrito() {

    const {
        contador,
        listaCarrito,
        totalCarrito
    } = obtenerElementos();

    if (
        !contador ||
        !listaCarrito ||
        !totalCarrito
    ) {
        return;
    }

    contador.innerText = carrito.length;

    listaCarrito.innerHTML = "";

    let total = 0;

    carrito.forEach((producto, index) => {

        total += producto.precio;

        listaCarrito.innerHTML += `

            <div class="d-flex justify-content-between align-items-center border-bottom py-3">

                <div>

                    <h5>
                        ${producto.nombre}
                    </h5>

                    <p>
                        $${producto.precio} MXN
                    </p>

                </div>

                <button
                    class="btn btn-danger btn-sm"
                    onclick="eliminarProducto(${index})">

                    <i class="bi bi-trash"></i>

                </button>

            </div>

        `;

    });

    totalCarrito.innerText = total;

}

function eliminarProducto(index) {

    carrito.splice(index, 1);

    guardarCarrito();

    actualizarCarrito();

}

function vaciarCarrito() {

    carrito = [];

    guardarCarrito();

    actualizarCarrito();

}

function abrirCarrito() {

    const modalElemento = document.getElementById(
        "modalCarrito"
    );

    if (!modalElemento) return;

    const modal = new bootstrap.Modal(
        modalElemento
    );

    modal.show();

}