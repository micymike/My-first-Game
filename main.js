// Initialize canvas and context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Load background music
const backgroundMusic = new Audio('Sia - Unstoppable (Official Video - Live from the Nostalgic For The Present Tour)-160.mp3');
backgroundMusic.loop = true;

// Define colors
const colors = {
    black: '#000000',
    white: '#FFFFFF',
    red: '#FF0000',
    green: '#00FF00',
    blue: '#0000FF',
    gray: '#888888',
    darkGray: '#444444'
};

// Set display dimensions
const displayWidth = canvas.width;
const displayHeight = canvas.height;

// Road properties
const roadWidth = 300;
const roadLeftEdge = (displayWidth - roadWidth) / 2;
const roadRightEdge = roadLeftEdge + roadWidth;

// Load and resize car image
const carImg = new Image();
carImg.src = 'car2.png';
const carWidth = 50;
const carHeight = 100;

// Load and resize background image
const backgroundImg = new Image();
backgroundImg.src = 'background.jpg';

// State variables
let isPaused = false;
let isGameOver = false;
let score = 0;
let x = (displayWidth * 0.45);
let y = (displayHeight * 0.8);
let xChange = 0;
let tiltAngle = 0; // Tilt angle for car rotation

const obstaclesArray = [];
const obsWidth = 50;
const obsHeight = 50;
let obsSpeed = 2;

// Road lane lines for scrolling effect
const laneLineHeight = 40;
const laneLineGap = 20;
const laneLines = [];

for (let i = 0; i < displayHeight; i += laneLineHeight + laneLineGap) {
    laneLines.push(i);
}

// Function to display car with tilting effect
function drawCar(x, y, angle) {
    ctx.save();
    ctx.translate(x + carWidth / 2, y + carHeight / 2); // Move to the center of the car
    ctx.rotate(angle * Math.PI / 180); // Convert degrees to radians
    ctx.drawImage(carImg, -carWidth / 2, -carHeight / 2, carWidth, carHeight);
    ctx.restore();
}

// Function to display obstacles
function drawObstacles() {
    ctx.fillStyle = colors.black;
    obstaclesArray.forEach(obs => {
        ctx.fillRect(obs.x, obs.y, obs.width, obs.height);
        obs.y += obsSpeed;
    });

    // Remove passed obstacles and increase score
    obstaclesArray.forEach((obs, index) => {
        if (obs.y > displayHeight) {
            obstaclesArray.splice(index, 1);
            score++;
        }
    });
}

// Function to create new obstacle
function createObstacle() {
    const obsX = Math.random() * (roadRightEdge - roadLeftEdge - obsWidth) + roadLeftEdge;
    obstaclesArray.push({ x: obsX, y: -obsHeight, width: obsWidth, height: obsHeight });
}

// Function to display text on screen
function displayText(text, font, x, y) {
    ctx.fillStyle = colors.black;
    ctx.font = font;
    ctx.textAlign = 'center';
    ctx.fillText(text, x, y);
}

function showContinueButton() {
    const continueEl = document.getElementById('continue-el');
    if (continueEl) {
        continueEl.style.display = 'block';
    }
}

// Function to display crash message and score
function displayCrashMessage() {
    isGameOver = true;
    ctx.fillStyle = colors.white;
    ctx.fillRect(0, 0, displayWidth, displayHeight);
    displayText('Oops!! You Crashed', '75px sans-serif', displayWidth / 2, displayHeight / 3);
    displayText('Score: ' + score, '50px sans-serif', displayWidth / 2, displayHeight / 2);
    showContinueButton();
}

// Function to handle collision detection
function checkCollision() {
    for (const obs of obstaclesArray) {
        if (y < obs.y + obs.height && y + carHeight > obs.y &&
            x < obs.x + obs.width && x + carWidth > obs.x) {
            displayCrashMessage();
            return;
        }
    }
}

// Function to handle pause
function togglePause() {
    isPaused = !isPaused;
    if (isPaused) {
        backgroundMusic.pause();
        displayText('Game Paused', '75px sans-serif', displayWidth / 2, displayHeight / 2);
    } else {
        backgroundMusic.play();
        gameLoop();
    }
}

// Function to create buttons
function createButton(msg, x, y, w, h, ic, ac, action) {
    ctx.fillStyle = ic;
    ctx.fillRect(x, y, w, h);
    ctx.fillStyle = colors.black;
    ctx.font = '20px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(msg, x + w / 2, y + h / 2 + 7);

    function handleClick(event) {
        const rect = canvas.getBoundingClientRect();
        const mouseX = event.clientX - rect.left;
        const mouseY = event.clientY - rect.top;
        if (mouseX > x && mouseX < x + w && mouseY > y && mouseY < y + h) {
            action();
        }
    }

    canvas.addEventListener('click', handleClick);

    // To remove the event listener after action, ensure it is removed within the action if needed
}

// Function to start game intro
function gameIntro() {
    ctx.clearRect(0, 0, displayWidth, displayHeight);
    ctx.fillStyle = colors.white;
    ctx.fillRect(0, 0, displayWidth, displayHeight);
    displayText('Car Racing Game', '50px sans-serif', displayWidth / 2, displayHeight / 3);
    createButton('Play', displayWidth / 2 - 50, displayHeight / 2, 100, 50, colors.green, colors.darkGray, startGame);
    displayText('Use the left arrow or the write arrow. Press P to pause the game')
}

// Function to start the game
function startGame() {
    backgroundMusic.play();
    isGameOver = false;
    isPaused = false;
    score = 0;
    x = (displayWidth * 0.45);
    y = (displayHeight * 0.8);
    obstaclesArray.length = 0;
    gameLoop();
}

// Main game loop
function gameLoop() {
    if (isPaused || isGameOver) return;

    ctx.clearRect(0, 0, displayWidth, displayHeight);

    // Draw background
    ctx.drawImage(backgroundImg, roadLeftEdge, 0, roadWidth, displayHeight);

    // Draw road and lines
    ctx.fillStyle = colors.gray;
    ctx.fillRect(roadLeftEdge, 0, roadWidth, displayHeight);
    ctx.strokeStyle = colors.white;
    ctx.lineWidth = 5;
    ctx.beginPath();
    ctx.moveTo(roadLeftEdge, 0);
    ctx.lineTo(roadLeftEdge, displayHeight);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(roadRightEdge, 0);
    ctx.lineTo(roadRightEdge, displayHeight);
    ctx.stroke();

    laneLines.forEach((line, index) => {
        ctx.fillStyle = colors.white;
        ctx.fillRect(displayWidth / 2 - 2, line, 4, laneLineHeight);
        laneLines[index] += obsSpeed;
        if (laneLines[index] > displayHeight) laneLines[index] = -laneLineHeight;
    });

    // Draw obstacles
    if (Math.random() < 0.005) createObstacle();
    drawObstacles();

    // Draw car
    drawCar(x, y, tiltAngle);

    // Display score
    displayText("Score: " + score, '30px sans-serif', 70, 40);

    checkCollision();

    requestAnimationFrame(gameLoop);
}

// Event listeners for controls
window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
        xChange = -7;
        tiltAngle = -15; // Tilt car to the left
    }
    if (e.key === 'ArrowRight') {
        xChange = 7;
        tiltAngle = 15; // Tilt car to the right
    }
    if (e.key === 'ArrowUp') {
        obsSpeed += 1; // Increase speed
        tiltAngle = 0
    }
    if (e.key === 'ArrowDown') {
        obsSpeed = Math.max(1, obsSpeed - 1); // Reduce speed but keep it minimum 1
    }
    if (e.key === 'p') togglePause();
});


window.addEventListener('keydown', (e) => {
    x += xChange;
    x = Math.max(roadLeftEdge, Math.min(x, roadRightEdge - carWidth));
});

// Start the game intro screen
gameIntro();
