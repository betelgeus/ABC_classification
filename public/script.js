const canvas = document.getElementById("canvas");
canvas.width = 320;
canvas.height = 320;
const context = canvas.getContext("2d");
const backgroundColor = "white";
context.fillStyle = backgroundColor;
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
let letterIndex;

const audio1 = document.getElementById("audio1");
const audio2 = document.getElementById("audio2");
const audio3 = document.getElementById("audio3");
const audio4 = document.getElementById("audio4");
const audioSource1 = "/public/sounds/hi.wav";
const audioSource3 = "/public/sounds/good.wav";
const audioSource4 = "/public/sounds/bad.wav";
let audioSource2;

const loader = document.querySelector(".loader");
const buttonLoader = document.querySelector(".button-loader");


// Обработчик события "DOMContentLoaded" для отображения случайной буквы при загрузке страницы
document.addEventListener("DOMContentLoaded", () => {
    const { letter: randomLetter, index: letterIndex } = getRandomRussianLetter();
    taskIntro.textContent = 'Напиши букву'
    letterTask.textContent = `${randomLetter}`;
    audioSource2 = `/public/sounds/${letterIndex}.wav`;
    audio1.src = audioSource1;
    audio2.src = audioSource2;
    audio1.play().catch((error) => {
    console.error("Ошибка воспроизведения первого звука:", error);
  });
    // Прослушиваем событие 'ended' на первом аудиоэлементе, чтобы начать воспроизведение второго звука после окончания первого
    audio1.addEventListener("ended", () => {
        // Запускаем воспроизведение второго звука
        audio2.play().catch((error) => {
        console.error("Ошибка воспроизведения второго звука:", error);
        });
    });
});


// Функции для рисования
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
// Функция для отмены действия
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


// Функция для очистки canvas
function Clear() {
    context.fillStyle = backgroundColor;
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
    letterIndex = Math.floor(Math.random() * russianAlphabet.length);
    randomLetter = russianAlphabet[letterIndex]
    return {letter: randomLetter, index: letterIndex};
}

// Основная логика приложения, сохраняет картинку,
// асинхронно отправляет ее на сервер, получает и отображает результат работы модели
saveImg.addEventListener("click", () => {
    taskIntro.style.display = "none";
    letterTask.style.display = "none";

    loader.style.display = "block";
    buttonLoader.style.display = "block";

    // Получаем данные из canvas в формате base64
    let imageData = canvas.toDataURL();

    // Создаем объект Blob из данных base64
    let blob = dataURItoBlob(imageData);

    // Создаем объект FormData для отправки файла на сервер
    let formData = new FormData();
    // const LetterIndex = '25';
    formData.append("file", blob, `${Date.now()}.png`);
    formData.append("letter_index", letterIndex);


    // Отправляем данные на сервер с помощью Fetch API
    // http://127.0.0.1:8000/upload
    fetch("/upload", {
        method: "POST",
        body: formData,
    })
        .then(response => response.json())
        .then(data => {
            // Обработка ответа от сервера
            if (data.result === true) {
                const { letter: randomLetter, index: letterIndex }  = getRandomRussianLetter();
                taskIntro.style.display = "block";
                letterTask.style.display = "block";
                buttonLoader.style.display = "none";
                taskIntro.innerHTML = 'Молодец! Теперь напиши букву';
                letterTask.innerHTML = `${randomLetter}`;
                audioSource2 = `/public/sounds/${letterIndex}.wav`;
                audio3.src = audioSource3;
                audio2.src = audioSource2;
                audio3.play().catch((error) => {
                    console.error("Ошибка воспроизведения первого звука:", error);
                  });
                    audio3.addEventListener("ended", () => {
                        audio2.play().catch((error) => {
                        console.error("Ошибка воспроизведения второго звука:", error);
                        });
                    });
            } else if (data.result === false) {
                taskIntro.style.display = "block";
                letterTask.style.display = "block";
                buttonLoader.style.display = "none";
                taskIntro.innerHTML = 'Попробуй еще раз! Напиши букву'
                letterTask.innerHTML = `${randomLetter}`;
                audioSource2 = `/public/sounds/${letterIndex}.wav`;
                audio4.src = audioSource4;
                audio2.src = audioSource2;
                audio4.play().catch((error) => {
                    console.error("Ошибка воспроизведения первого звука:", error);
                  });
                    audio4.addEventListener("ended", () => {
                        audio2.play().catch((error) => {
                        console.error("Ошибка воспроизведения второго звука:", error);
                        });
                    });

            } else {
                taskIntro.style.display = "block";
                letterTask.style.display = "block";
                buttonLoader.style.display = "none";
                letterTask.innerHTML = "Неизвестный результат. Попробуй еще раз!";
            }
            Clear();
            loader.style.display = "none";
            buttonLoader.style.display = "none";
        })
        .catch(error => {
            taskIntro.style.display = "block";
            letterTask.style.display = "block";
            taskIntro.innerHTML = error;
            letterTask.innerHTML = "";
            console.error(error);
            loader.style.display = "none";
            buttonLoader.style.display = "none";
    });
});
