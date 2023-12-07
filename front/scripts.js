/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/acoes';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      data.acoes.forEach(item => insertList(
        item.id,
        item.open,
        item.high,
        item.low,
        item.adjclose,
        item.volume,
      ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
getList()




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputOpen, inputHigh, inputLow, inputClose, inputAdjClose) => {

  const formData = new FormData();
  formData.append('open', inputOpen);
  formData.append('high', inputHigh);
  formData.append('low', inputLow);
  formData.append('close', inputClose);
  formData.append('adjclose', inputAdjClose);

  let url = 'http://127.0.0.1:5000/acao';
  fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const idItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(idItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/acao?id=' + item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async () => {
  let inputOpen = document.getElementById("newOpen").value;
  let inputHigh = document.getElementById("newHigh").value;
  let inputLow = document.getElementById("newLow").value;
  let inputClose = document.getElementById("newClose").value;
  let inputAdjClose = document.getElementById("newAdjClose").value;

  // Verifica se os campos são numéricos
  if (
    isNaN(inputOpen) ||
    isNaN(inputHigh) ||
    isNaN(inputLow) ||
    isNaN(inputAdjClose) ||
    isNaN(inputClose)
  ) {
    alert("Esses campos precisam ser números!");
  } else {
    // Se todos os campos são números, continua com a inserção do item
    insertList(inputOpen, inputHigh, inputLow, inputAdjClose, inputClose);
    postItem(inputOpen, inputHigh, inputLow, inputAdjClose, inputClose);
    alert("Item adicionado!");
  }
};



/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (Id, Open, High, Low, AdjClose, Volume) => {
  var item = [Id, Open, High, Low, AdjClose, Volume];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);


  document.getElementById("newOpen").value = "";
  document.getElementById("newHigh").value = "";
  document.getElementById("newLow").value = "";
  document.getElementById("newClose").value = "";
  document.getElementById("newAdjClose").value = "";
  removeElement();
}