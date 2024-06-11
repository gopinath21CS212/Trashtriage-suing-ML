async function startWebcam() {
    const constraints = {
        video: {
            width: {
                min: 300,
                ideal: 450,
                max: 600,
            },
            height: {
                min: 300,
                ideal: 450,
                max: 600,
            }
        },
        audio: false,
    };

    try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        const webcam = document.getElementById('camera');
        webcam.srcObject = stream;
    } catch (error) {
        console.error('Error accessing the webcam:', error);
    }
}

function captureImage() {
    const webcam = document.getElementById('camera');
    const canvas = document.getElementById('canvas');

    const context = canvas.getContext('2d');
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    context.drawImage(webcam, 0, 0, canvas.width, canvas.height);
}

function getResponse() {
    captureImage();
    const webcam = document.getElementById('camera');
    const canvas = document.getElementById('canvas');

    const context = canvas.getContext('2d');
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    context.drawImage(webcam, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/jpeg');
    const formData = new FormData();
    formData.append("image", imageData);

    $.ajax({
        type: "POST",
        url: "/classify",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
            console.log(response.prediction);
            const res = response.prediction;
            if (res != null) {
                const temp = res.split('$');
                const newEle = document.createElement("tr");
                temp.forEach(element => {
                    const t = element.split("#")[1];
                    const s = document.createElement("td");
                    s.textContent = t;
                    newEle.appendChild(s);
                });

                document.getElementById("result").appendChild(newEle);
                document.getElementById("result").style.display = "block";
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    startWebcam();
    setInterval(getResponse, 3000);
});