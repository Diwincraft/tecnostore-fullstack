let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

document.addEventListener("DOMContentLoaded", () => {
    actualizarCarrito();
});

// ===============================
// ELEMENTOS DOM
// ===============================
function obtenerElementos() {
    return {
        contador: document.getElementById("contador-carrito"),
        listaCarrito: document.getElementById("lista-carrito"),
        totalCarrito: document.getElementById("total-carrito")
    };
}

// ===============================
// AGREGAR PRODUCTO
// ===============================
function agregarAlCarrito(id, nombre, precio, imagen) {

    const existente = carrito.find(p => p.id === id);

    if (existente) {
        existente.cantidad += 1;
    } else {
        carrito.push({
            id,
            nombre,
            precio: parseFloat(precio),
            imagen,
            cantidad: 1
        });
    }

    guardarCarrito();
    actualizarCarrito();
}

// ===============================
// GUARDAR EN LOCALSTORAGE
// ===============================
function guardarCarrito() {
    localStorage.setItem("carrito", JSON.stringify(carrito));
}

// ===============================
// ACTUALIZAR UI
// ===============================
function actualizarCarrito() {

    const { contador, listaCarrito, totalCarrito } = obtenerElementos();

    if (!contador || !listaCarrito || !totalCarrito) return;

    // contador = cantidad total de unidades
    const totalItems = carrito.reduce((acc, p) => acc + p.cantidad, 0);
    contador.innerText = totalItems;

    listaCarrito.innerHTML = "";

    let total = 0;

    carrito.forEach((producto) => {

        const subtotal = producto.precio * producto.cantidad;
        total += subtotal;

        listaCarrito.innerHTML += `
            <div class="d-flex justify-content-between align-items-center border-bottom py-3">

                <div>
                    <h5>${producto.nombre}</h5>

                    <p class="mb-1">
                        $${producto.precio} MXN x ${producto.cantidad}
                    </p>

                    <small class="text-muted">
                        Subtotal: $${subtotal.toFixed(2)}
                    </small>
                </div>

                <div class="d-flex gap-2 align-items-center">

                    <button class="btn btn-sm btn-secondary"
                        onclick="restarCantidad('${producto.id}')">
                        -
                    </button>

                    <span>${producto.cantidad}</span>

                    <button class="btn btn-sm btn-primary"
                        onclick="sumarCantidad('${producto.id}')">
                        +
                    </button>

                    <button class="btn btn-danger btn-sm"
                        onclick="eliminarProducto('${producto.id}')">
                        <i class="bi bi-trash"></i>
                    </button>

                </div>

            </div>
        `;
    });

    totalCarrito.innerText = total.toFixed(2);
}

// ===============================
// RESTAR CANTIDAD
// ===============================
function restarCantidad(id) {

    const producto = carrito.find(p => p.id === id);

    if (!producto) return;

    producto.cantidad -= 1;

    if (producto.cantidad <= 0) {
        carrito = carrito.filter(p => p.id !== id);
    }

    guardarCarrito();
    actualizarCarrito();
}

// ===============================
// SUMAR CANTIDAD
// ===============================
function sumarCantidad(id) {

    const producto = carrito.find(p => p.id === id);

    if (!producto) return;

    producto.cantidad += 1;

    guardarCarrito();
    actualizarCarrito();
}

// ===============================
// ELIMINAR PRODUCTO COMPLETO
// ===============================
function eliminarProducto(id) {

    carrito = carrito.filter(p => p.id !== id);

    guardarCarrito();
    actualizarCarrito();
}

// ===============================
// VACÍO TOTAL
// ===============================
function vaciarCarrito() {

    carrito = [];

    guardarCarrito();
    actualizarCarrito();
}

// ===============================
// ABRIR MODAL
// ===============================
function abrirCarrito() {

    const modalElemento = document.getElementById("modalCarrito");

    if (!modalElemento) return;

    const modal = new bootstrap.Modal(modalElemento);

    modal.show();
}