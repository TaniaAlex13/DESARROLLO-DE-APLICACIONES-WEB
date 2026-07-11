const formulario = document.getElementById("formServicio");

const nombre = document.getElementById("nombre");
const descripcion = document.getElementById("descripcion");
const categoria = document.getElementById("categoria");

const lista = document.getElementById("listaServicios");
const mensaje = document.getElementById("mensaje");
const total = document.getElementById("total");

let contador = 0;

// Arreglo donde se almacenarán los servicios
let servicios = [];

// VALIDAR NOMBRE

function validarNombre(){

    if(nombre.value.trim()===""){

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        document.getElementById("errorNombre").textContent="El nombre es obligatorio.";

        return false;
    }

    if(nombre.value.trim().length<4){

        nombre.classList.add("is-invalid");
        nombre.classList.remove("is-valid");

        document.getElementById("errorNombre").textContent="Debe tener mínimo 4 caracteres.";

        return false;
    }

    nombre.classList.remove("is-invalid");
    nombre.classList.add("is-valid");

    return true;

}



// VALIDAR DESCRIPCION

function validarDescripcion(){

    if(descripcion.value.trim().length<10){

        descripcion.classList.add("is-invalid");
        descripcion.classList.remove("is-valid");

        document.getElementById("errorDescripcion").textContent="Ingrese al menos 10 caracteres.";

        return false;
    }

    descripcion.classList.remove("is-invalid");
    descripcion.classList.add("is-valid");

    return true;

}



// VALIDAR CATEGORIA

function validarCategoria(){

    if(categoria.value===""){

        categoria.classList.add("is-invalid");
        categoria.classList.remove("is-valid");

        document.getElementById("errorCategoria").textContent="Seleccione una categoría.";

        return false;

    }

    categoria.classList.remove("is-invalid");
    categoria.classList.add("is-valid");

    return true;

}



// EVENTOS

nombre.addEventListener("input", validarNombre);

descripcion.addEventListener("blur", validarDescripcion);

categoria.addEventListener("change", validarCategoria);



// ENVIAR FORMULARIO

formulario.addEventListener("submit",function(e){

    e.preventDefault();

    const okNombre=validarNombre();
    const okDescripcion=validarDescripcion();
    const okCategoria=validarCategoria();

    if(!(okNombre && okDescripcion && okCategoria)){

        mensaje.innerHTML=`
        <div class="alert alert-danger">
            Corrija los errores antes de registrar.
        </div>
        `;

        return;

    }

    const servicio = {
        nombre: nombre.value,
        descripcion: descripcion.value,
        categoria: categoria.value
    };

    servicios.push(servicio);

    contador++;

    total.textContent=contador;

    mostrarServicios();

    mensaje.innerHTML=`

        <div class="alert alert-success">

            Registro agregado correctamente.

        </div>

    `;

    formulario.reset();

    nombre.classList.remove("is-valid");
    descripcion.classList.remove("is-valid");
    categoria.classList.remove("is-valid");

});



// ELIMINAR

lista.addEventListener("click",function(e){

    if(e.target.classList.contains("btnEliminar")){

        e.target.closest(".card").remove();

        contador--;

        total.textContent=contador;

    }

});

function mostrarServicios(){

    lista.innerHTML="";
    servicios.forEach(function(servicio){

        const tarjeta=document.createElement("div");

        tarjeta.className="card registro";

        tarjeta.innerHTML=`

            <div class="card-body">

                <h5>${servicio.nombre}</h5>

                <p>${servicio.descripcion}</p>

                <span class="badge bg-primary">${servicio.categoria}</span>

                <br><br>

                <button class="btn btn-danger btnEliminar">
                    Eliminar
                </button>

            </div>

        `;

        lista.appendChild(tarjeta);

});

        
}