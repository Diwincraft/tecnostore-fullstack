const contenedor = document.getElementById("contenedor-productos");
const buscador = document.getElementById("buscador");

function mostrarProductos(lista){

    contenedor.innerHTML = "";

    lista.forEach(producto => {

        contenedor.innerHTML += `

            <div class="col-md-3">

                <div class="card shadow-sm h-100">

                    <img 
                        src="${producto.imagen}"
                        class="card-img-top"
                        alt="${producto.nombre}">

                    <div class="card-body text-center">

                        <h5 class="card-title">

                            ${producto.nombre}

                        </h5>

                        <p class="text-primary fw-bold">

                            $${producto.precio} MXN

                        </p>

                        <p class="text-muted">

                            ${producto.categoria}

                        </p>

                        <button 
                            class="btn btn-dark"
                            onclick="agregarAlCarrito(${producto.id})">

                            Agregar al carrito

                        </button>

                    </div>

                </div>

            </div>

        `;

    });

}

mostrarProductos(productos);

buscador.addEventListener("keyup", () => {

    const texto = buscador.value.toLowerCase();

    const filtrados = productos.filter(producto =>
        producto.nombre.toLowerCase().includes(texto)
    );

    mostrarProductos(filtrados);

});

function verProducto(nombre){

    alert("Producto seleccionado: " + nombre);

}