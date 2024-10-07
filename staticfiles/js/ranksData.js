
const gameRanks = {
    "LoL": [
        ("Iron", "Iron"),
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Master", "Master"),
        ("Grandmaster", "Grandmaster"),
        ("Challenger", "Challenger"),
    ],
    "D2": [
        ("Herald", "Herald"),
        ("Guardian", "Guardian"),
        ("Crusader", "Crusader"),
        ("Archon", "Archon"),
        ("Legend", "Legend"),
        ("Ancient", "Ancient"),
        ("Divine", "Divine"),
        ("Immortal", "Immortal"),
    ],
    "CSGO": [
        ("Silver I", "Silver I"),
        ("Silver II", "Silver II"),
        ("Silver III", "Silver III"),
        ("Silver IV", "Silver IV"),
        ("Silver Elite", "Silver Elite"),
        ("Silver Elite Master", "Silver Elite Master"),
        ("Gold Nova I", "Gold Nova I"),
        ("Gold Nova II", "Gold Nova II"),
        ("Gold Nova III", "Gold Nova III"),
        ("Gold Nova Master", "Gold Nova Master"),
        ("Master Guardian I", "Master Guardian I"),
        ("Master Guardian II", "Master Guardian II"),
        ("Master Guardian Elite", "Master Guardian Elite"),
        ("Distinguished Master Guardian", "Distinguished Master Guardian"),
        ("Legendary Eagle", "Legendary Eagle"),
        ("Legendary Eagle Master", "Legendary Eagle Master"),
        ("Supreme Master First Class", "Supreme Master First Class"),
        ("Global Elite", "Global Elite"),
    ],
    "VAL": [
        ("Iron", "Iron"),
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Immortal", "Immortal"),
        ("Radiant", "Radiant"),
    ],
    "OW": [
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Master", "Master"),
        ("Grandmaster", "Grandmaster"),
        ("Top 500", "Top 500"),
    ],
    "PUBG": [
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Master", "Master"),
        ("Grandmaster", "Grandmaster"),
    ],
    "FORT": [
        ("Open", "Open"),
        ("Contender", "Contender"),
        ("Champion", "Champion"),
        ("Unreal", "Unreal"),
    ],
    "Apex": [
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Master", "Master"),
        ("Apex Predator", "Apex Predator"),
    ],
    "R6": [
        ("Copper", "Copper"),
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Champion", "Champion"),
    ],
    "RL": [
        ("Bronze", "Bronze"),
        ("Silver", "Silver"),
        ("Gold", "Gold"),
        ("Platinum", "Platinum"),
        ("Diamond", "Diamond"),
        ("Champion", "Champion"),
        ("Grand Champion", "Grand Champion"),
        ("Supersonic Legend", "Supersonic Legend"),
    ],
}

const gameSelect = document.getElementById("id_game");
const rankSelect = document.getElementById("rank");

function updateRankOptions(game) {
    rankSelect.innerHTML = ""; // Limpiar las opciones actuales

    if (game in gameRanks) {
        gameRanks[game].forEach(function (rank) {
            const option = document.createElement("option");
            option.value = rank;
            option.textContent = rank;
            rankSelect.appendChild(option);
        });
    }
}

gameSelect.addEventListener('change', function () {
    updateRankOptions(this.value);
});

// Inicializa con las opciones correctas cuando se carga la página
updateRankOptions(gameSelect.value);
