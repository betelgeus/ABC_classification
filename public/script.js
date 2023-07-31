const canvas = document.getElementById("canvas");
canvas.width = 400;
canvas.height = 400;
const context = canvas.getContext("2d");
context.fillStyle = "white";
context.fillRect(0, 0, canvas.width, canvas.height);
let restore_array = [];
let start_index = -1;
let stroke_color = 'black';
let stroke_width = "15";
let is_drawing = false;
const saveImg = document.querySelector("#save-img");
const taskIntro = document.getElementById("task-intro");
const letterTask = document.getElementById("letter-task");
const russianAlphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ';
let randomLetter;

// Обработчик события "DOMContentLoaded" для отображения случайной буквы при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
    randomLetter = getRandomRussianLetter();
    taskIntro.textContent = 'Напиши букву'
    letterTask.textContent = `${randomLetter}`; // Отображаем случайную букву на странице
});


function start(event) {
  is_drawing = true;
  context.beginPath();
  context.moveTo(getX(event), getY(event));
  event.preventDefault();
}

function draw(event) {
  if (is_drawing) {
    context.lineTo(getX(event), getY(event));
    context.strokeStyle = stroke_color;
    context.lineWidth = stroke_width;
    context.lineCap = "round";
    context.lineJoin = "round";
    context.stroke();
  }
  event.preventDefault();
}

function stop(event) {
  if (is_drawing) {
    context.stroke();
    context.closePath();
    is_drawing = false;
  }
  event.preventDefault();
  restore_array.push(context.getImageData(0, 0, canvas.width, canvas.height));
  start_index += 1;
}

function getX(event) {
  if (event.pageX == undefined) {return event.targetTouches[0].pageX - canvas.offsetLeft}
  else {return event.pageX - canvas.offsetLeft}
  }


function getY(event) {
  if (event.pageY == undefined) {return event.targetTouches[0].pageY - canvas.offsetTop}
  else {return event.pageY - canvas.offsetTop}
}

canvas.addEventListener("touchstart", start, false);
canvas.addEventListener("touchmove", draw, false);
canvas.addEventListener("touchend", stop, false);
canvas.addEventListener("mousedown", start, false);
canvas.addEventListener("mousemove", draw, false);
canvas.addEventListener("mouseup", stop, false);
canvas.addEventListener("mouseout", stop, false);


// TODO: пофиксить багу с двумя кликами для очистки. Наигрывается на MAC OS с активированной функцией "Касание для имитации нажатия".
function Restore() {
  if (start_index <= 0) {
    Clear()
  } else {
    start_index += -1;
    restore_array.pop();
    if ( event.type != 'mouseout' ) {
      context.putImageData(restore_array[start_index], 0, 0);
    }
  }
}


function Clear() {
    context.fillStyle = "white";
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillRect(0, 0, canvas.width, canvas.height);
    restore_array = [];
    start_index = -1;
}

// Функция для преобразования данных base64 в объект Blob
function dataURItoBlob(dataURI) {
    const byteString = atob(dataURI.split(',')[1]);
    const mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];
    const arrayBuffer = new ArrayBuffer(byteString.length);
    const intArray = new Uint8Array(arrayBuffer);
    for (let i = 0; i < byteString.length; i++) {
        intArray[i] = byteString.charCodeAt(i);
    }
    return new Blob([arrayBuffer], { type: mimeString });
}


// Функция для генерации случайной буквы русского алфавита
function getRandomRussianLetter() {
    let randomIndex = Math.floor(Math.random() * russianAlphabet.length);
    return russianAlphabet[randomIndex];
}


saveImg.addEventListener("click", () => {
    // Получаем данные из canvas в формате base64
    let imageData = canvas.toDataURL();

    // Создаем объект Blob из данных base64
    let blob = dataURItoBlob(imageData);

    // Создаем объект FormData для отправки файла на сервер
    let formData = new FormData();
    let Letter = randomLetter;
    let LetterIndex = russianAlphabet.indexOf(Letter);
    // const LetterIndex = '25';
    formData.append("file", blob, `${Date.now()}.png`);
    formData.append("letter_index", LetterIndex);


    // Отправляем данные на сервер с помощью Fetch API
    fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            const loader = document.querySelector(".loader");
            if (loader) {
                loader.remove();
            }
            // Обработка ответа от сервера
            if (data.result === true) {
                randomLetter = getRandomRussianLetter();
                taskIntro.innerHTML = 'Молодец! Теперь напиши букву'
                letterTask.innerHTML = `${randomLetter}`;
            } else if (data.result === false) {
                taskIntro.innerHTML = 'Попробуй еще раз! Напиши букву'
                letterTask.innerHTML = `${randomLetter}`;
            } else {
                letterTask.innerHTML = "Неизвестный результат. Попробуй еще раз!";
            }
            Clear();
        })
        .catch(error => {
            taskIntro.innerHTML = error;
            console.error(error);
    });
});
