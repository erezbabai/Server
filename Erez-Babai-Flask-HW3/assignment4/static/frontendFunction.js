function frontendFunction() {
    var frontend_form = document.getElementById("frontend");
    var idInput = frontend_form.elements[0].value
    let element = document.createElement('a');
    element.href = 'https://reqres.in/api/users';
    element.pathname = element.pathname + '/' + idInput;
    fetch(element.href).then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    );
}



function createUsersList(response){
    const currMain = document.querySelector("main")
    const section = document.createElement('section')
    section.innerHTML = `
            <div class="userData">
            <img id="pic"  src="${response.avatar}" alt="pic"/>
             <div  >
            <h2> ${response.first_name} ${response.last_name}</h2>
                <h4> email: ${response.email} </h4>
              </div>
            </div>
        `
        currMain.appendChild(section)
        currMain.replaceChild(section, currMain.childNodes[0]);
}
