const formulario = document.getElementById("formServicio");
const lista = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");

let contador = 0;

formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const descripcion = document.getElementById("descripcion").value;
    const categoria = document.getElementById("categoria").value;

    if (
        nombre.trim() === "" ||
        descripcion.trim() === "" ||
        categoria.trim() === ""
    ) {

        mensaje.innerHTML = `
            <div class="alert alert-danger">
                Todos los campos son obligatorios.
            </div>
        `;

        return;
    }

    mensaje.innerHTML = `
        <div class="alert alert-success">
            Servicio registrado correctamente.
        </div>
    `;

    const tarjeta = document.createElement("div");

    tarjeta.className = "card p-3 mb-3 shadow";

    tarjeta.innerHTML = `
        <h5>${nombre}</h5>
        <p>${descripcion}</p>
        <span class="badge bg-primary mb-2">
            ${categoria}
        </span>
        <br>
        <button class="btn btn-danger eliminar">
            Eliminar
        </button>
    `;

    const botonEliminar = tarjeta.querySelector(".eliminar");

    botonEliminar.addEventListener("click", function () {

        tarjeta.remove();

        contador--;

        total.textContent = contador;
    });

    lista.appendChild(tarjeta);

    contador++;

    total.textContent = contador;

    formulario.reset();
});