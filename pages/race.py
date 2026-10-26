
import streamlit as st
import streamlit.components.v1 as components

st.title("💧 구름 탐험대: 물방울 레이스")
st.write(
    "물방울 하나를 직접 조종해 AI 물방울 3마리와 경주하세요! "
    "아이템 없이 실력으로 우승에 도전해요."
)

game_html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 12px;
    font-family: Arial, sans-serif;
    color: #18334b;
    background: transparent;
}

.game { max-width: 1000px; margin: auto; }

.hero {
    padding: 22px 14px;
    border-radius: 22px;
    text-align: center;
    color: white;
    background: linear-gradient(135deg, #48b7ef, #8176e9);
}

.hero h1 { margin: 0 0 8px; font-size: 27px; }
.hero p { margin: 0; font-size: 14px; }

.panel {
    background: white;
    border: 1px solid #e0eaf2;
    border-radius: 18px;
    padding: 15px;
    margin-top: 14px;
}

.controls {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}

select, button {
    border-radius: 11px;
    padding: 10px 13px;
    font-size: 14px;
    border: 1px solid #d7e3ee;
}

select {
    background: white;
    color: #18334b;
    flex: 1;
    min-width: 145px;
}

button { cursor: pointer; font-weight: bold; }
button:disabled { opacity: .45; cursor: not-allowed; }

.primary { background: #267fe0; color: white; border: none; }
.secondary { background: #eef6ff; color: #23588a; }

.weather-note {
    font-size: 13px;
    color: #53718a;
    margin-top: 10px;
}

.track {
    border-radius: 17px;
    padding: 10px;
    overflow: hidden;
    transition: background .3s;
}

.track.sunny { background: linear-gradient(#a9e5ff, #fff6ce); }
.track.rainy { background: linear-gradient(#9fb7ce, #e0eaf3); }
.track.snowy { background: linear-gradient(#dceeff, #ffffff); }
.track.stormy { background: linear-gradient(#6d769d, #bac8e8); }

.lane {
    position: relative;
    min-height: 76px;
    margin: 5px 0;
    border-radius: 12px;
    background: #ffffffb8;
    border: 1px dashed #b8d2e7;
    overflow: hidden;
}

.lane-label {
    position: absolute;
    left: 8px;
    top: 6px;
    z-index: 2;
    font-size: 11px;
    font-weight: bold;
    color: #41647e;
}

.runner {
    position: absolute;
    left: 0%;
    top: 25px;
    font-size: 32px;
    transform: translateX(-50%);
    transition: left .12s linear;
    z-index: 3;
    filter: drop-shadow(0 2px 1px #5b728855);
}

.runner.selected {
    outline: 2px solid #267fe0;
    outline-offset: 3px;
    border-radius: 50%;
}

.finish {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 5px;
    width: 15px;
    background: repeating-linear-gradient(
        0deg, #243448 0 7px, white 7px 14px
    );
    opacity: .85;
}

.lane-meta {
    position: absolute;
    right: 25px;
    bottom: 5px;
    font-size: 11px;
    color: #496980;
    z-index: 2;
}

.event {
    min-height: 55px;
    border-radius: 13px;
    padding: 12px;
    background: #fff8df;
    border: 1px solid #f5e3a0;
    font-size: 14px;
    line-height: 1.5;
}

.stats {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.stat {
    background: #f3f8ff;
    border-radius: 12px;
    padding: 12px;
}

.stat b {
    display: block;
    font-size: 18px;
    margin-top: 5px;
}

.small {
    color: #5e7890;
    font-size: 12px;
    line-height: 1.6;
}

.rank-row {
    display: flex;
    align-items: center;
    gap: 9px;
    padding: 9px;
    border-radius: 10px;
    background: #f6f9fc;
    margin-top: 7px;
}

.rank-number { font-size: 19px; width: 30px; text-align: center; }
.rank-name { flex: 1; font-weight: bold; }

.winner {
    display: none;
    text-align: center;
    padding: 22px 12px;
    margin-top: 12px;
    border-radius: 17px;
    color: #80520b;
    background: linear-gradient(135deg, #fff3b4, #ffe0ec);
    animation: pop .5s ease;
}

.winner h2 { font-size: 25px; margin: 6px 0; }

.trophy {
    font-size: 52px;
    animation: bounce .7s infinite alternate;
}

.confetti {
    position: fixed;
    top: -20px;
    z-index: 99;
    pointer-events: none;
    animation: fall 2.5s linear forwards;
}

@keyframes pop {
    from { transform: scale(.85); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

@keyframes bounce {
    from { transform: translateY(0); }
    to { transform: translateY(-8px); }
}

@keyframes fall {
    to { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}

@media (max-width: 520px) {
    .hero h1 { font-size: 22px; }
    .panel { padding: 11px; }
    .runner { font-size: 27px; }
    .lane { min-height: 72px; }
}
</style>
</head>

<body>
<div class="game">

    <div class="hero">
        <h1>💧 RAIN DROP RACE 🏁</h1>
        <p>아이템 없이 직접 달려서 AI 물방울 3마리를 이겨 보세요!</p>
    </div>

    <div class="panel">
        <div class="controls">
            <select id="playerChoice">
                <option value="0">💧 번개 물방울로 플레이</option>
                <option value="1">🩵 무지개 물방울로 플레이</option>
                <option value="2">💦 얼음 물방울로 플레이</option>
                <option value="3">🌧️ 구름 물방울로 플레이</option>
            </select>

            <select id="weather">
                <option value="sunny">☀️ 맑은 날</option>
                <option value="rainy">🌧️ 비 오는 날</option>
                <option value="snowy">❄️ 눈 오는 날</option>
                <option value="stormy">⛈️ 번개 치는 날</option>
            </select>

            <button class="primary" id="start">🏁 레이스 시작!</button>
            <button class="primary" id="movePlayer" disabled>
                ⬆️ 전진! (스페이스바)
            </button>
            <button class="secondary" id="restart">🔄 다시 하기</button>
        </div>

        <div class="weather-note" id="weatherNote"></div>
    </div>

    <div class="panel">
        <h3>🏃 레이스 트랙</h3>

        <div class="track sunny" id="track">
            <div class="lane">
                <div class="lane-label">⚡ 번개 물방울</div>
                <div class="runner" id="runner0">💧</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta0">출발 대기</div>
            </div>

            <div class="lane">
                <div class="lane-label">🌈 무지개 물방울</div>
                <div class="runner" id="runner1">🩵</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta1">출발 대기</div>
            </div>

            <div class="lane">
                <div class="lane-label">❄️ 얼음 물방울</div>
                <div class="runner" id="runner2">💦</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta2">출발 대기</div>
            </div>

            <div class="lane">
                <div class="lane-label">☁️ 구름 물방울</div>
                <div class="runner" id="runner3">🌧️</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta3">출발 대기</div>
            </div>
        </div>

        <div class="event" id="event" style="margin-top:12px">
            🌤️ 물방울을 선택하고 레이스를 시작하세요!
        </div>
    </div>

    <div class="panel">
        <h3>🎮 조작 방법</h3>
        <p>1. 내가 조종할 물방울과 날씨를 선택하세요.</p>
        <p>2. 레이스 시작 후 전진 버튼을 반복해서 누르세요.</p>
        <p>3. 또는 스페이스바를 눌러 물방울을 움직이세요.</p>
        <p class="small">
            난이도: 보통보다 약간 어려움 · AI 물방울은 가끔 순간 가속합니다.
            스페이스바가 반응하지 않으면 게임 화면을 클릭한 뒤 눌러 보세요.
        </p>
    </div>

    <div class="panel">
        <h3>📊 현재 순위</h3>
        <div class="stats">
            <div class="stat">
                <span class="small">레이스 상태</span>
                <b id="status">출발 대기</b>
            </div>
            <div class="stat">
                <span class="small">경과 시간</span>
                <b id="clock">0.0초</b>
            </div>
        </div>
        <div id="ranking" style="margin-top:12px"></div>
    </div>

    <div class="winner" id="winner">
        <div class="trophy">🏆</div>
        <h2 id="winnerText">우승!</h2>
        <p id="winnerDetail">축하합니다!</p>
        <button class="primary" id="playAgain">🎉 다시 도전하기</button>
    </div>

</div>

<script>
const racers = [
    {name:"번개 물방울", emoji:"💧"},
    {name:"무지개 물방울", emoji:"🩵"},
    {name:"얼음 물방울", emoji:"💦"},
    {name:"구름 물방울", emoji:"🌧️"}
];

const weatherInfo = {
    sunny: {
        note:"☀️ 맑은 날: 밝은 트랙에서 달려요.",
        event:"☀️ 햇살이 비칩니다! 준비하세요!"
    },
    rainy: {
        note:"🌧️ 비 오는 날: 미끄러운 트랙에서 속도가 조금 줄어요.",
        event:"🌧️ 빗방울이 떨어집니다!"
    },
    snowy: {
        note:"❄️ 눈 오는 날: 눈길 때문에 속도가 조금 줄어요.",
        event:"❄️ 눈이 내립니다!"
    },
    stormy: {
        note:"⛈️ 번개 치는 날: 가끔 강한 돌풍이 발생해요.",
        event:"⛈️ 천둥 번개가 칩니다!"
    }
};

let positions = [0, 0, 0, 0];
let finished = [];
let running = false;
let interval = null;
let elapsed = 0;
let selectedWeather = "sunny";
let playerIndex = 0;
let playerMoveCooldown = false;

const $ = id => document.getElementById(id);

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function showEvent(message) {
    $("event").textContent = message;
}

function updateWeather() {
    selectedWeather = $("weather").value;
    $("track").className = "track " + selectedWeather;
    $("weatherNote").textContent = weatherInfo[selectedWeather].note;
    showEvent(weatherInfo[selectedWeather].event);
}

function render() {
    racers.forEach((r, i) => {
        $("runner" + i).style.left =
            Math.min(96, positions[i]) + "%";

        $("runner" + i).classList.toggle(
            "selected", i === playerIndex
        );

        $("meta" + i).textContent =
            positions[i] >= 100
                ? "🏁 완주!"
                : Math.floor(positions[i]) + "%";
    });

    const order = [0, 1, 2, 3].sort(
        (a, b) => positions[b] - positions[a] || a - b
    );

    $("ranking").innerHTML = order.map((i, rank) => `
        <div class="rank-row">
            <div class="rank-number">
                ${["🥇","🥈","🥉","🏅"][rank]}
            </div>
            <div>${racers[i].emoji}</div>
            <div class="rank-name">
                ${racers[i].name}${i === playerIndex ? " (나)" : " (AI)"}
            </div>
            <div><b>${Math.floor(positions[i])}%</b></div>
        </div>
    `).join("");

    $("clock").textContent = elapsed.toFixed(1) + "초";
}

function makeConfetti() {
    const pieces = ["🎉","✨","🌈","💧","⭐","🏆"];

    for (let i = 0; i < 35; i++) {
        const item = document.createElement("div");
        item.className = "confetti";
        item.textContent = pieces[randomInt(0, pieces.length - 1)];
        item.style.left = randomInt(0, 100) + "vw";
        item.style.fontSize = randomInt(16, 27) + "px";
        item.style.animationDelay = (Math.random() * 0.8) + "s";

        document.body.appendChild(item);
        setTimeout(() => item.remove(), 3500);
    }
}

function finishRace() {
    running = false;
    clearInterval(interval);
    interval = null;

    $("start").disabled = true;
    $("movePlayer").disabled = true;
    $("status").textContent = "레이스 종료";

    const order = [0, 1, 2, 3].sort((a, b) => {
        const af = finished.indexOf(a);
        const bf = finished.indexOf(b);

        if (af !== -1 && bf !== -1) return af - bf;
        if (af !== -1) return -1;
        if (bf !== -1) return 1;

        return positions[b] - positions[a];
    });

    const winner = order[0];
    const playerRank = order.indexOf(playerIndex) + 1;

    $("winner").style.display = "block";

    if (winner === playerIndex) {
        $("winnerText").textContent =
            "🏆 성공! " + racers[playerIndex].name + " 우승!";

        $("winnerDetail").textContent =
            "AI 물방울을 모두 이겼어요! 총 " +
            elapsed.toFixed(1) + "초";

        showEvent("🎉 축하해요! 내가 조종한 물방울이 우승했어요!");
    } else {
        $("winnerText").textContent =
            racers[winner].emoji + " " + racers[winner].name + " 우승!";

        $("winnerDetail").textContent =
            "내 물방울은 " + playerRank +
            "등이에요. 더 빠르게 조작해 다시 도전해 보세요!";

        showEvent("🏁 레이스 종료! 다시 도전해 보세요!");
    }

    makeConfetti();
}

function tick() {
    elapsed += 0.2;

    for (let i = 0; i < 4; i++) {
        // 내가 조종하는 물방울은 자동으로 움직이지 않아요.
        if (i === playerIndex || positions[i] >= 100) {
            continue;
        }

        // AI의 기본 속도를 이전보다 낮춤
        let speed = 1.4 + Math.random() * 0.9;

        // 캐릭터별 순간 가속: 빈도와 세기를 완화
        if (i === 0 && Math.random() < 0.15) {
            speed += 1.8;
            showEvent("⚡ 번개 물방울이 순간 가속합니다!");
        }

        if (i === 1 && Math.random() < 0.14) {
            speed += 1.6;
            showEvent("🌈 무지개 물방울이 보너스 길을 발견했어요!");
        }

        if (i === 2 && Math.random() < 0.10) {
            speed += 1.4;
            showEvent("❄️ 얼음 물방울이 치고 나갑니다!");
        }

        if (i === 3 && Math.random() < 0.15) {
            speed += 1.7;
            showEvent("☁️ 구름 물방울에게 행운의 바람이 불어요!");
        }

        // 날씨에 따른 속도 변화
        if (selectedWeather === "rainy") speed *= 0.93;
        if (selectedWeather === "snowy") speed *= 0.86;
        if (selectedWeather === "stormy") speed *= 0.96;

        // 가끔 발생하는 작은 돌발 상황
        if (Math.random() < 0.02) {
            speed = Math.max(0.6, speed - 0.8);
            showEvent("🌧️ 갑작스러운 바람으로 속도가 줄었어요!");
        }

        positions[i] = Math.min(100, positions[i] + speed);

        if (positions[i] >= 100 && !finished.includes(i)) {
            finished.push(i);
            showEvent(
                "🏁 " + racers[i].name +
                " 완주! " + finished.length + "번째 도착!"
            );
        }
    }

    render();

    if (finished.length === 4) {
        finishRace();
    }
}

function updatePlayerChoice() {
    if (running) return;

    playerIndex = Number($("playerChoice").value);
    render();

    showEvent(
        "🎮 " + racers[playerIndex].name +
        "을(를) 선택했어요! 버튼이나 스페이스바로 달리세요."
    );
}

function movePlayer() {
    if (!running || positions[playerIndex] >= 100 ||
        playerMoveCooldown) {
        return;
    }

    playerMoveCooldown = true;

    // 직접 조종하는 물방울은 이전보다 조금 더 이동
    let step = 2.8;

    if (selectedWeather === "rainy") step *= 0.93;
    if (selectedWeather === "snowy") step *= 0.86;
    if (selectedWeather === "stormy") step *= 0.96;

    positions[playerIndex] = Math.min(
        100, positions[playerIndex] + step
    );

    if (positions[playerIndex] >= 100 &&
        !finished.includes(playerIndex)) {
        finished.push(playerIndex);
        showEvent("🏁 내가 조종한 물방울이 완주했어요!");
    } else {
        showEvent(
            "⬆️ " + racers[playerIndex].name +
            " 전진! 계속 눌러 보세요!"
        );
    }

    render();

    if (finished.length === 4) {
        finishRace();
    }

    setTimeout(() => {
        playerMoveCooldown = false;
    }, 235);
}

function startRace() {
    if (running) return;

    if (finished.length === 4) {
        resetRace();
    }

    running = true;
    $("start").disabled = true;
    $("weather").disabled = true;
    $("playerChoice").disabled = true;
    $("movePlayer").disabled = false;
    $("status").textContent = "레이스 진행 중";

    showEvent(
        "🚦 출발! 버튼이나 스페이스바를 반복해서 눌러 달리세요!"
    );

    interval = setInterval(tick, 200);
}

function resetRace() {
    clearInterval(interval);
    interval = null;

    positions = [0, 0, 0, 0];
    finished = [];
    running = false;
    elapsed = 0;
    playerMoveCooldown = false;

    $("winner").style.display = "none";
    $("start").disabled = false;
    $("weather").disabled = false;
    $("playerChoice").disabled = false;
    $("movePlayer").disabled = true;
    $("status").textContent = "출발 대기";

    updateWeather();
    render();
}

$("weather").addEventListener("change", updateWeather);
$("playerChoice").addEventListener("change", updatePlayerChoice);
$("movePlayer").addEventListener("click", movePlayer);
$("start").addEventListener("click", startRace);
$("restart").addEventListener("click", resetRace);
$("playAgain").addEventListener("click", resetRace);

// 스페이스바로 직접 조종
document.addEventListener("keydown", event => {
    if (event.code === "Space" && !event.repeat) {
        event.preventDefault();
        movePlayer();
    }
});

updateWeather();
updatePlayerChoice();
render();
</script>
</body>
</html>
"""

components.html(game_html, height=1180, scrolling=True)
