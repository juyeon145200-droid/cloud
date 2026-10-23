
import streamlit as st
import streamlit.components.v1 as components

st.title("💧 구름 탐험대: 물방울 레이스")
st.write(
    "4마리의 물방울이 날씨와 돌발 이벤트를 뚫고 결승선까지 달려가요!"
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

.game {
    max-width: 1000px;
    margin: auto;
}

.hero {
    padding: 22px 14px;
    border-radius: 22px;
    text-align: center;
    color: white;
    background: linear-gradient(135deg, #48b7ef, #8176e9);
    box-shadow: 0 8px 20px #6d91bc30;
}

.hero h1 {
    margin: 0 0 8px;
    font-size: 27px;
}

.hero p {
    margin: 0;
    font-size: 14px;
}

.panel {
    background: white;
    border: 1px solid #e0eaf2;
    border-radius: 18px;
    padding: 15px;
    margin-top: 14px;
    box-shadow: 0 5px 16px #3155740c;
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

button {
    cursor: pointer;
    font-weight: bold;
    transition: transform .15s, opacity .15s;
}

button:hover { transform: translateY(-1px); }
button:disabled { opacity: .45; cursor: not-allowed; }

.primary {
    background: #267fe0;
    color: white;
    border: none;
}

.secondary {
    background: #eef6ff;
    color: #23588a;
}

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
    background: linear-gradient(#dff4ff, #f5fbff);
}

.track.sunny {
    background: linear-gradient(#a9e5ff, #fff6ce);
}

.track.rainy {
    background: linear-gradient(#9fb7ce, #e0eaf3);
}

.track.snowy {
    background: linear-gradient(#dceeff, #ffffff);
}

.track.stormy {
    background: linear-gradient(#6d769d, #bac8e8);
}

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
    transition: left .16s linear;
    z-index: 3;
    filter: drop-shadow(0 2px 1px #5b728855);
}

.runner.boost {
    filter: drop-shadow(0 0 8px #ffb52e);
}

.runner.selected {
    outline: 2px solid #267fe0;
    outline-offset: 3px;
    border-radius: 50%;
}

.runner.slowed {
    filter: grayscale(0.8) drop-shadow(0 0 5px #7b8794);
}

.runner.shielded::after {
    content: "🛡️";
    position: absolute;
    font-size: 15px;
    top: -7px;
    right: -13px;
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

.rank-row:first-child { margin-top: 0; }

.rank-number {
    font-size: 19px;
    width: 30px;
    text-align: center;
}

.rank-name {
    flex: 1;
    font-weight: bold;
}

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

.winner h2 {
    font-size: 25px;
    margin: 6px 0;
}

.trophy {
    font-size: 52px;
    animation: bounce .7s infinite alternate;
}

@keyframes pop {
    from { transform: scale(.85); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

@keyframes bounce {
    from { transform: translateY(0); }
    to { transform: translateY(-8px); }
}

.confetti {
    position: fixed;
    top: -20px;
    z-index: 99;
    pointer-events: none;
    animation: fall 2.5s linear forwards;
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
        <p>능력을 활용하고 날씨 이벤트를 뚫어 우승을 차지하세요!</p>
    </div>

    <div class="panel">
        <div class="controls">
            <select id="playerChoice" aria-label="내가 조종할 물방울 선택">
                <option value="0">💧 번개 물방울로 플레이</option>
                <option value="1">🩵 무지개 물방울로 플레이</option>
                <option value="2">💦 얼음 물방울로 플레이</option>
                <option value="3">🌧️ 구름 물방울로 플레이</option>
            </select>
            <select id="weather" aria-label="날씨 선택">
                <option value="sunny">☀️ 맑은 날</option>
                <option value="rainy">🌧️ 비 오는 날</option>
                <option value="snowy">❄️ 눈 오는 날</option>
                <option value="stormy">⛈️ 번개 치는 날</option>
            </select>

            <button class="primary" id="start">🏁 레이스 시작!</button>
            <button class="primary" id="movePlayer" disabled>⬆️ 내 물방울 전진! (스페이스바)</button>
            <button class="secondary" id="restart">🔄 다시 하기</button>
        </div>
        <div class="weather-note" id="weatherNote">
            ☀️ 맑은 날: 특별한 방해 없이 기본 속도로 달려요.
        </div>
    </div>

    <div class="panel">
        <h3 style="margin:0 0 12px">🏃 레이스 트랙</h3>
        <div class="track sunny" id="track">
            <div class="lane" id="lane0">
                <div class="lane-label">⚡ 번개 물방울 · 순간 가속</div>
                <div class="runner" id="runner0">💧</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta0">출발 대기</div>
            </div>
            <div class="lane" id="lane1">
                <div class="lane-label">🌈 무지개 물방울 · 보너스 이동</div>
                <div class="runner" id="runner1">🩵</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta1">출발 대기</div>
            </div>
            <div class="lane" id="lane2">
                <div class="lane-label">❄️ 얼음 물방울 · 보호막</div>
                <div class="runner" id="runner2">💦</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta2">출발 대기</div>
            </div>
            <div class="lane" id="lane3">
                <div class="lane-label">☁️ 구름 물방울 · 행운 이동</div>
                <div class="runner" id="runner3">🌧️</div>
                <div class="finish"></div>
                <div class="lane-meta" id="meta3">출발 대기</div>
            </div>
        </div>

        <div class="event" id="event" style="margin-top:12px">
            🌤️ 준비 완료! 물방울을 선택한 뒤 레이스를 시작하세요. 내 물방울은 전진 버튼 또는 스페이스바로 조종해요!
        </div>
    </div>

    <div class="panel">
        <h3 style="margin:0 0 12px">🎒 아이템 사용</h3>
        <div class="controls">
            <select id="target" aria-label="아이템을 사용할 물방울">
                <option value="0">⚡ 번개 물방울</option>
                <option value="1">🌈 무지개 물방울</option>
                <option value="2">❄️ 얼음 물방울</option>
                <option value="3">☁️ 구름 물방울</option>
            </select>
            <button class="primary" id="useItem" disabled>🚀 부스터 사용</button>
            <button class="secondary" id="shield" disabled>🛡️ 보호막 사용</button>
            <button class="secondary" id="attack" disabled>🌪️ 방해 아이템 사용</button>
        </div>
        <p class="small" id="inventory" style="margin-bottom:0">
            부스터·보호막은 선택한 물방울에 사용할 수 있고, 방해 아이템은 다른 물방울의 속도를 늦춰요. AI 물방울도 아이템을 자동으로 사용합니다.
        </p>
    </div>

    <div class="panel">
        <h3 style="margin:0 0 12px">📊 현재 순위</h3>
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
    {name:"번개 물방울", emoji:"💧", ability:"순간 가속", color:"#38a9ef"},
    {name:"무지개 물방울", emoji:"🩵", ability:"보너스 이동", color:"#e69bd5"},
    {name:"얼음 물방울", emoji:"💦", ability:"보호막", color:"#76c8ed"},
    {name:"구름 물방울", emoji:"🌧️", ability:"행운 이동", color:"#7cc9aa"}
];

const weatherInfo = {
    sunny: {
        note:"☀️ 맑은 날: 트랙이 밝고 기본 속도로 달려요.",
        event:"☀️ 햇살이 비칩니다! 모두 힘차게 출발해요!"
    },
    rainy: {
        note:"🌧️ 비 오는 날: 미끄러운 트랙에서 속도가 조금 줄 수 있어요.",
        event:"🌧️ 빗방울이 떨어집니다! 발밑을 조심하세요."
    },
    snowy: {
        note:"❄️ 눈 오는 날: 눈길 때문에 이동 속도가 불규칙해요.",
        event:"❄️ 눈이 내립니다! 조심스럽게 달려요."
    },
    stormy: {
        note:"⛈️ 번개 치는 날: 가속 이벤트가 강해지지만 돌발 상황도 있어요.",
        event:"⛈️ 천둥 번개가 칩니다! 역전의 기회가 올까요?"
    }
};

let positions = [0, 0, 0, 0];
let finished = [];
let shields = [false, false, false, false];
let boosts = [0, 0, 0, 0];
let slowdowns = [0, 0, 0, 0];
let running = false;
let interval = null;
let elapsed = 0;
let lastEvent = 0;
let lastItem = 0;
let selectedWeather = "sunny";
let playerIndex = 0;
let playerMoveCooldown = false;
let lastPlayerAttack = -10;

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
        const runner = $("runner" + i);
        runner.style.left = Math.min(96, positions[i]) + "%";
        runner.classList.toggle("boost", boosts[i] > 0);
        runner.classList.toggle("selected", i === playerIndex);
        runner.classList.toggle("shielded", shields[i]);
        runner.classList.toggle("slowed", slowdowns[i] > 0);
        $("meta" + i).textContent =
            positions[i] >= 100 ? "🏁 완주!" : Math.floor(positions[i]) + "%";
    });

    const order = [0, 1, 2, 3].sort((a, b) => {
        if (positions[b] !== positions[a]) return positions[b] - positions[a];
        return a - b;
    });

    $("ranking").innerHTML = order.map((i, rank) => `
        <div class="rank-row">
            <div class="rank-number">${["🥇","🥈","🥉","🏅"][rank]}</div>
            <div>${racers[i].emoji}</div>
            <div class="rank-name">${racers[i].name}</div>
            <div><b>${Math.floor(positions[i])}%</b></div>
        </div>
    `).join("");

    $("clock").textContent = elapsed.toFixed(1) + "초";
    $("inventory").textContent =
        "🚀 부스터: 전진을 더 빠르게 · 🛡️ 보호막: 방해 1회 방어 · 🌪️ 방해: 다른 물방울의 속도를 잠시 늦춤";
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
    $("useItem").disabled = true;
    $("shield").disabled = true;
    $("attack").disabled = true;
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
        $("winnerText").textContent = "🏆 성공! " + racers[playerIndex].name + " 우승!";
        $("winnerDetail").textContent = "네가 조종한 물방울이 1등으로 도착했어요! 총 " + elapsed.toFixed(1) + "초";
        showEvent("🎉 축하해요! 내가 조종한 " + racers[playerIndex].name + "이(가) 우승했어요!");
    } else {
        $("winnerText").textContent = racers[winner].emoji + " " + racers[winner].name + " 우승!";
        $("winnerDetail").textContent = "내 물방울은 " + playerRank + "등이에요. 다시 도전해 보세요! 총 " + elapsed.toFixed(1) + "초";
        showEvent("🏁 레이스 종료! 우승자는 " + racers[winner].name + "입니다. 내 물방울은 " + playerRank + "등이에요!");
    }
    makeConfetti();
}

function useAttack(attackerIndex, targetIndex, isPlayer = false) {
    if (targetIndex === attackerIndex) return false;

    if (shields[targetIndex]) {
        shields[targetIndex] = false;
        showEvent("🛡️ " + racers[targetIndex].name + "의 보호막이 방해 아이템을 막았어요!");
        return true;
    }

    slowdowns[targetIndex] = Math.max(slowdowns[targetIndex], 8);
    showEvent(
        (isPlayer ? "🌪️ 내가 사용한 방해 아이템! " : "💥 AI 물방울의 방해 아이템! ") +
        racers[attackerIndex].name + "이(가) " + racers[targetIndex].name + "의 속도를 늦췄어요!"
    );
    return true;
}

function tick() {
    elapsed += 0.2;

    for (let i = 0; i < 4; i++) {
        if (positions[i] >= 100) continue;

        // 내가 선택한 물방울은 직접 조종하고, 나머지 3마리만 AI가 달려요.
        if (i === playerIndex) continue;

        let speed = 1.0 + Math.random() * 1.2;

        // 캐릭터별 능력
        if (i === 0 && Math.random() < 0.13) {
            speed += 2.2;
            showEvent("⚡ 번개 물방울의 순간 가속! 빠르게 치고 나갑니다!");
        }

        if (i === 1 && Math.random() < 0.10) {
            speed += 1.8;
            showEvent("🌈 무지개 물방울이 보너스 길을 발견했어요!");
        }

        if (i === 3 && Math.random() < 0.12) {
            speed += 2.0;
            showEvent("☁️ 구름 물방울에게 행운이 찾아왔어요!");
        }

        // 날씨에 따른 기본 속도 변화
        if (selectedWeather === "rainy") speed *= 0.92;
        if (selectedWeather === "snowy") speed *= 0.82;
        if (selectedWeather === "stormy") speed *= 0.96;

        // 방해 아이템에 맞으면 잠시 속도가 느려져요.
        if (slowdowns[i] > 0) {
            speed *= 0.45;
            slowdowns[i]--;
        }

        // 사용한 부스터
        if (boosts[i] > 0) {
            speed += 3.2;
            boosts[i]--;
        }

        // 무작위 기상 이벤트
        if (Math.random() < 0.035) {
            const eventType = randomInt(0, 3);

            if (eventType === 0) {
                speed += 3.0;
                showEvent("🌬️ 순풍 발생! " + racers[i].name + "이(가) 앞으로 나아갑니다!");
            } else if (eventType === 1) {
                if (shields[i]) {
                    shields[i] = false;
                    showEvent("🛡️ 보호막 발동! " + racers[i].name + "이(가) 악천후를 막았어요!");
                } else {
                    speed = Math.max(0.3, speed - 1.0);
                    showEvent("🌧️ 갑작스러운 폭우! " + racers[i].name + "의 속도가 줄었어요!");
                }
            } else if (eventType === 2) {
                speed += 2.4;
                showEvent("🌈 무지개 길 등장! " + racers[i].name + "이(가) 보너스를 얻었어요!");
            } else {
                if (selectedWeather === "stormy") {
                    speed += 3.5;
                    showEvent("⚡ 번개 부스트! " + racers[i].name + "이(가) 번개처럼 질주합니다!");
                } else {
                    speed += 1.2;
                    showEvent("💨 시원한 바람! " + racers[i].name + "이(가) 속도를 올렸어요!");
                }
            }
        }

        positions[i] = Math.min(100, positions[i] + speed);

        if (positions[i] >= 100 && !finished.includes(i)) {
            finished.push(i);
            showEvent("🏁 " + racers[i].name + " 완주! 현재 " + finished.length + "번째 도착!");
        }
    }

    // 아이템 상자가 주기적으로 등장해요. AI 물방울은 아이템을 자동으로 사용해요.
    if (elapsed - lastItem > 3.0 && Math.random() < 0.55) {
        lastItem = elapsed;
        const holder = randomInt(0, 3);
        const action = randomInt(0, 2); // 0: 부스터, 1: 보호막, 2: 방해

        if (action === 0) {
            boosts[holder] = Math.max(boosts[holder], 5);
            showEvent("🎁 " + racers[holder].name + "이(가) 🚀 부스터를 얻었어요!");
        } else if (action === 1) {
            shields[holder] = true;
            showEvent("🎁 " + racers[holder].name + "이(가) 🛡️ 보호막을 얻었어요!");
        } else if (holder !== playerIndex) {
            // AI가 방해 아이템을 얻으면 다른 물방울을 골라 자동 공격해요.
            const targets = [0, 1, 2, 3].filter(j => j !== holder && positions[j] < 100);
            if (targets.length > 0) {
                const target = targets[randomInt(0, targets.length - 1)];
                useAttack(holder, target, false);
            }
        } else {
            // 플레이어가 방해 아이템을 얻으면 버튼으로 상대에게 사용할 수 있어요.
            showEvent("🎁 방해 아이템 획득! 아래에서 상대 물방울을 선택하고 🌪️ 방해 아이템을 사용하세요!");
        }
    }

    render();

    if (finished.length === 4) finishRace();
}

function updatePlayerChoice() {
    if (running) return;
    playerIndex = Number($("playerChoice").value);
    $("target").value = String(playerIndex);
    render();
    showEvent("🎮 " + racers[playerIndex].name + "을(를) 선택했어요! 레이스를 시작하고 전진 버튼 또는 스페이스바를 눌러 보세요.");
}

function movePlayer() {
    if (!running || positions[playerIndex] >= 100 || playerMoveCooldown) return;
    playerMoveCooldown = true;
    let playerStep = 3.2;
    if (slowdowns[playerIndex] > 0) {
        playerStep *= 0.45;
        slowdowns[playerIndex]--;
        showEvent("🌪️ 방해 아이템 효과로 내 물방울의 속도가 잠시 느려졌어요!");
    }
    if (boosts[playerIndex] > 0) {
        playerStep += 2.5;
        boosts[playerIndex]--;
        showEvent("🚀 부스터 효과! " + racers[playerIndex].name + "이(가) 더 멀리 전진했어요!");
    }
    positions[playerIndex] = Math.min(100, positions[playerIndex] + playerStep);
    if (positions[playerIndex] >= 100 && !finished.includes(playerIndex)) {
        finished.push(playerIndex);
        showEvent("🏁 내가 조종한 " + racers[playerIndex].name + " 완주!");
    } else {
        showEvent("⬆️ " + racers[playerIndex].name + " 전진! 계속 눌러 결승선까지 달려요!");
    }
    render();
    if (finished.length === 4) finishRace();
    setTimeout(() => { playerMoveCooldown = false; }, 180);
}

function startRace() {
    if (running) return;

    if (finished.length === 4) resetRace();

    running = true;
    $("start").disabled = true;
    $("weather").disabled = true;
    $("playerChoice").disabled = true;
    $("movePlayer").disabled = false;
    $("useItem").disabled = false;
    $("shield").disabled = false;
    $("attack").disabled = false;
    $("status").textContent = "레이스 진행 중";
    showEvent("🚦 출발! 물방울들이 달리기 시작했어요!");

    interval = setInterval(tick, 200);
}

function resetRace() {
    clearInterval(interval);
    interval = null;
    positions = [0, 0, 0, 0];
    finished = [];
    shields = [false, false, false, false];
    boosts = [0, 0, 0, 0];
    slowdowns = [0, 0, 0, 0];
    running = false;
    elapsed = 0;
    lastEvent = 0;
    lastItem = 0;
    lastPlayerAttack = -10;

    $("winner").style.display = "none";
    $("start").disabled = false;
    $("weather").disabled = false;
    $("playerChoice").disabled = false;
    $("movePlayer").disabled = true;
    playerMoveCooldown = false;
    $("useItem").disabled = true;
    $("shield").disabled = true;
    $("attack").disabled = true;
    $("status").textContent = "출발 대기";

    updateWeather();
    render();
}

$("weather").addEventListener("change", updateWeather);
$("playerChoice").addEventListener("change", updatePlayerChoice);
$("movePlayer").addEventListener("click", movePlayer);
document.addEventListener("keydown", (event) => {
    if (event.code === "Space") {
        event.preventDefault();
        movePlayer();
    }
});
$("start").addEventListener("click", startRace);
$("restart").addEventListener("click", resetRace);
$("playAgain").addEventListener("click", resetRace);

$("useItem").addEventListener("click", () => {
    if (!running) return;
    const i = Number($("target").value);
    boosts[i] = Math.max(boosts[i], 10);
    showEvent("🚀 " + racers[i].name + "에게 부스터를 사용했어요!");
});

$("shield").addEventListener("click", () => {
    if (!running) return;
    const i = Number($("target").value);
    shields[i] = true;
    showEvent("🛡️ " + racers[i].name + "에게 보호막을 씌웠어요!");
});

$("attack").addEventListener("click", () => {
    if (!running) return;

    const targetIndex = Number($("target").value);
    if (targetIndex === playerIndex) {
        showEvent("⚠️ 내 물방울이 아닌 상대 물방울을 선택해 주세요!");
        return;
    }

    if (elapsed - lastPlayerAttack < 2.5) {
        showEvent("⏳ 방해 아이템은 2.5초마다 한 번 사용할 수 있어요!");
        return;
    }

    if (positions[targetIndex] >= 100) {
        showEvent("🏁 이미 완주한 물방울에게는 사용할 수 없어요!");
        return;
    }

    lastPlayerAttack = elapsed;
    useAttack(playerIndex, targetIndex, true);
});

updateWeather();
updatePlayerChoice();
render();
</script>
</body>
</html>
"""

components.html(game_html, height=1250, scrolling=True)
